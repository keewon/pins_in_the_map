/**
 * Pins in the Map - Application Logic
 */

// Available colors for pin lists
const COLORS = [
    { name: 'gold', value: '#d4a853' },
    { name: 'copper', value: '#c47d4e' },
    { name: 'teal', value: '#4a9d8e' },
    { name: 'coral', value: '#e07a5f' },
    { name: 'indigo', value: '#5c6bc0' },
    { name: 'rose', value: '#d4648a' },
    { name: 'emerald', value: '#4caf50' },
    { name: 'amber', value: '#ffa726' },
];

// Cookie names for storing state
const COOKIE_VISIBILITY = 'pins_visibility';
const COOKIE_COLORS = 'pins_colors';
const COOKIE_EXPIRY_DAYS = 365;

/**
 * Cookie utility functions
 */
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${encodeURIComponent(JSON.stringify(value))};expires=${expires.toUTCString()};path=/;SameSite=Lax`;
}

function getCookie(name) {
    const nameEQ = name + '=';
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(nameEQ) === 0) {
            try {
                return JSON.parse(decodeURIComponent(c.substring(nameEQ.length)));
            } catch (e) {
                return null;
            }
        }
    }
    return null;
}

function saveVisibilityToCookie() {
    setCookie(COOKIE_VISIBILITY, state.listVisibility, COOKIE_EXPIRY_DAYS);
}

function loadVisibilityFromCookie() {
    return getCookie(COOKIE_VISIBILITY) || {};
}

function saveColorsToCookie() {
    setCookie(COOKIE_COLORS, state.listColors, COOKIE_EXPIRY_DAYS);
}

function loadColorsFromCookie() {
    return getCookie(COOKIE_COLORS) || {};
}

// Application State
const state = {
    map: null,
    pinLists: [],
    markers: {}, // Grouped by list id
    listColors: {}, // Store selected colors per list
    listVisibility: {}, // Store visibility state per list
};

// DOM Elements
const elements = {
    sidebar: null,
    mobileToggle: null,
    overlay: null,
    listContainer: null,
    map: null,
};

/**
 * Initialize the application
 */
async function init() {
    // Cache DOM elements
    elements.sidebar = document.getElementById('sidebar');
    elements.mobileToggle = document.getElementById('mobileToggle');
    elements.overlay = document.getElementById('overlay');
    elements.listContainer = document.getElementById('listContainer');
    elements.map = document.getElementById('map');

    // Setup event listeners
    setupEventListeners();

    // Initialize map
    initMap();

    // Load pin data
    await loadPinData();
}

/**
 * Initialize Leaflet map
 */
function initMap() {
    // Create map centered on South Korea
    state.map = L.map('map', {
        center: [36.5, 127.5],
        zoom: 7,
        zoomControl: true,
    });

    // Add tile layer (CartoDB dark matter for dark theme)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19,
    }).addTo(state.map);

    // Position zoom control
    state.map.zoomControl.setPosition('topright');
}

/**
 * Load pin data from JSON files
 */
async function loadPinData() {
    showLoading();

    try {
        // First, load the lists metadata
        const listsResponse = await fetch('data/lists.json');
        if (!listsResponse.ok) throw new Error('Failed to load lists data');
        
        const listsData = await listsResponse.json();
        
        // Load saved state from cookies
        const savedVisibility = loadVisibilityFromCookie();
        const savedColors = loadColorsFromCookie();

        // Load pins for each list from individual files
        const listPromises = listsData.lists.map(async (listMeta) => {
            try {
                const pinsResponse = await fetch(`data/${listMeta.id}.json`);
                if (!pinsResponse.ok) throw new Error(`Failed to load pins for list ${listMeta.id}`);
                const pinsData = await pinsResponse.json();
                
                return {
                    ...listMeta,
                    pins: pinsData.pins || []
                };
            } catch (error) {
                console.error(`Error loading pins for list ${listMeta.id}:`, error);
                return {
                    ...listMeta,
                    pins: []
                };
            }
        });

        state.pinLists = await Promise.all(listPromises);

        // Initialize colors and visibility for each list
        state.pinLists.forEach((list, index) => {
            // Use saved color if exists, otherwise use default from data or fallback
            state.listColors[list.id] = savedColors.hasOwnProperty(list.id)
                ? savedColors[list.id]
                : (list.color || COLORS[index % COLORS.length].value);
            // Use saved visibility if exists, otherwise default to true
            state.listVisibility[list.id] = savedVisibility.hasOwnProperty(list.id) 
                ? savedVisibility[list.id] 
                : true;
        });

        renderPinLists();
        renderAllMarkers();

    } catch (error) {
        console.error('Error loading pin data:', error);
        showError('데이터를 불러오는데 실패했습니다.');
    }
}

/**
 * Render pin lists in sidebar
 */
function renderPinLists() {
    const container = elements.listContainer;
    container.innerHTML = '';

    state.pinLists.forEach((list) => {
        const color = state.listColors[list.id];
        const isActive = state.listVisibility[list.id];
        
        const listElement = document.createElement('div');
        listElement.className = `pin-list-item ${isActive ? 'active' : ''}`;
        listElement.style.setProperty('--list-color', color);
        listElement.dataset.listId = list.id;

        listElement.innerHTML = `
            <div class="list-header">
                <label class="checkbox-wrapper">
                    <input type="checkbox" ${isActive ? 'checked' : ''} data-list-id="${list.id}">
                    <span class="checkmark">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    </span>
                </label>
                <div class="list-info">
                    <div class="list-title">
                        ${list.title}
                        <span class="pin-count" style="background: ${color}">${list.pins.length}</span>
                    </div>
                    <div class="list-description">${list.description}</div>
                </div>
            </div>
            <div class="color-picker-wrapper">
                <span class="color-picker-label">색상:</span>
                <div class="color-options">
                    ${COLORS.map(c => `
                        <button 
                            class="color-option ${c.value === color ? 'selected' : ''}" 
                            style="background: ${c.value}"
                            data-color="${c.value}"
                            data-list-id="${list.id}"
                            aria-label="색상 ${c.name}"
                        ></button>
                    `).join('')}
                </div>
            </div>
        `;

        // Event: Toggle visibility
        const checkbox = listElement.querySelector('input[type="checkbox"]');
        checkbox.addEventListener('change', (e) => {
            e.stopPropagation();
            toggleListVisibility(list.id);
        });

        // Event: Color selection
        const colorOptions = listElement.querySelectorAll('.color-option');
        colorOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                e.stopPropagation();
                const newColor = option.dataset.color;
                changeListColor(list.id, newColor);
            });
        });

        // Event: Click on list item (toggle visibility)
        listElement.addEventListener('click', (e) => {
            if (e.target.closest('.checkbox-wrapper') || e.target.closest('.color-option')) return;
            checkbox.checked = !checkbox.checked;
            toggleListVisibility(list.id);
        });

        container.appendChild(listElement);
    });
}

/**
 * Toggle visibility of a pin list
 */
function toggleListVisibility(listId) {
    state.listVisibility[listId] = !state.listVisibility[listId];
    const isVisible = state.listVisibility[listId];

    // Save to cookie
    saveVisibilityToCookie();

    // Update UI
    const listElement = document.querySelector(`.pin-list-item[data-list-id="${listId}"]`);
    if (listElement) {
        listElement.classList.toggle('active', isVisible);
    }

    // Update markers
    if (isVisible) {
        showMarkers(listId);
    } else {
        hideMarkers(listId);
    }
}

/**
 * Change color of a pin list
 */
function changeListColor(listId, newColor) {
    state.listColors[listId] = newColor;

    // Save to cookie
    saveColorsToCookie();

    // Update list item UI
    const listElement = document.querySelector(`.pin-list-item[data-list-id="${listId}"]`);
    if (listElement) {
        listElement.style.setProperty('--list-color', newColor);
        
        // Update pin count badge
        const pinCount = listElement.querySelector('.pin-count');
        if (pinCount) {
            pinCount.style.background = newColor;
        }

        // Update selected color indicator
        const colorOptions = listElement.querySelectorAll('.color-option');
        colorOptions.forEach(option => {
            option.classList.toggle('selected', option.dataset.color === newColor);
        });
    }

    // Update markers if visible
    if (state.listVisibility[listId]) {
        hideMarkers(listId);
        showMarkers(listId);
    }
}

/**
 * Render all markers on the map
 */
function renderAllMarkers() {
    state.pinLists.forEach(list => {
        if (state.listVisibility[list.id]) {
            showMarkers(list.id);
        }
    });
}

/**
 * Show markers for a specific list
 */
function showMarkers(listId) {
    const list = state.pinLists.find(l => l.id === listId);
    if (!list) return;

    const color = state.listColors[listId];
    state.markers[listId] = [];

    list.pins.forEach(pin => {
        const marker = createMarker(pin, color, list.title);
        marker.addTo(state.map);
        state.markers[listId].push(marker);
    });
}

/**
 * Hide markers for a specific list
 */
function hideMarkers(listId) {
    if (state.markers[listId]) {
        state.markers[listId].forEach(marker => {
            state.map.removeLayer(marker);
        });
        state.markers[listId] = [];
    }
}

/**
 * Create a custom marker
 */
function createMarker(pin, color, listTitle) {
    // Create custom icon
    const icon = L.divIcon({
        className: 'custom-marker-wrapper',
        html: `<div class="custom-marker" style="background: ${color}"></div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32],
    });

    const marker = L.marker([pin.latitude, pin.longitude], { icon });

    // Add popup
    const popupContent = `
        <div class="popup-content">
            <div class="popup-title">${pin.title}</div>
            <div class="popup-description">${pin.description}</div>
            <div class="popup-list-badge" style="background: ${color}">${listTitle}</div>
        </div>
    `;

    marker.bindPopup(popupContent, {
        maxWidth: 280,
        closeButton: true,
    });

    return marker;
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Mobile toggle
    elements.mobileToggle.addEventListener('click', toggleSidebar);

    // Overlay click closes sidebar
    elements.overlay.addEventListener('click', closeSidebar);

    // Close sidebar on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeSidebar();
        }
    });

    // Handle window resize
    window.addEventListener('resize', handleResize);
}

/**
 * Toggle sidebar (mobile)
 */
function toggleSidebar() {
    const isOpen = elements.sidebar.classList.contains('open');
    if (isOpen) {
        closeSidebar();
    } else {
        openSidebar();
    }
}

/**
 * Open sidebar
 */
function openSidebar() {
    elements.sidebar.classList.add('open');
    elements.mobileToggle.classList.add('active');
    elements.overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

/**
 * Close sidebar
 */
function closeSidebar() {
    elements.sidebar.classList.remove('open');
    elements.mobileToggle.classList.remove('active');
    elements.overlay.classList.remove('active');
    document.body.style.overflow = '';
}

/**
 * Handle window resize
 */
function handleResize() {
    if (window.innerWidth > 768) {
        closeSidebar();
    }
    // Invalidate map size on resize
    if (state.map) {
        state.map.invalidateSize();
    }
}

/**
 * Show loading state
 */
function showLoading() {
    elements.listContainer.innerHTML = `
        <div class="loading">
            <div class="loading-spinner"></div>
            <p>데이터를 불러오는 중...</p>
        </div>
    `;
}

/**
 * Show error state
 */
function showError(message) {
    elements.listContainer.innerHTML = `
        <div class="loading">
            <p style="color: #e07a5f;">⚠️ ${message}</p>
        </div>
    `;
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', init);

