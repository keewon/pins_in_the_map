# 📍 Pins in the Map

지도에 핀을 꽂아 다양한 장소를 관리하는 웹 서비스입니다.

![Desktop & Mobile Support](https://img.shields.io/badge/Platform-Desktop%20%7C%20Mobile-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ 기능

- 🗺️ **인터랙티브 지도**: Leaflet 기반의 부드러운 지도 인터랙션
- 📋 **다중 핀 리스트**: 여러 개의 핀 리스트를 동시에 관리
- ✅ **체크박스 토글**: 각 리스트를 표시/숨김 가능
- 🎨 **색상 커스터마이징**: 각 리스트별 색상 지정 가능
- 📱 **반응형 디자인**: 데스크탑 및 모바일 완벽 지원
- 🌙 **다크 테마**: 눈이 편한 다크 테마 기본 적용

## 🚀 시작하기

### 방법 1: 간단한 로컬 서버 (권장)

#### Python 사용 시
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

#### Node.js 사용 시
```bash
# npx 사용 (Node.js 설치 필요)
npx serve

# 또는 http-server 설치 후
npm install -g http-server
http-server
```

### 방법 2: VS Code Live Server

1. VS Code에서 "Live Server" 확장 프로그램 설치
2. `index.html` 파일 우클릭 → "Open with Live Server"

### 접속

브라우저에서 `http://localhost:8000` (또는 해당 포트) 접속

## 📁 프로젝트 구조

```
pins_in_the_map/
├── index.html          # 메인 HTML 파일
├── styles.css          # 스타일시트
├── app.js              # 애플리케이션 로직
├── data/
│   └── pins.json       # 핀 데이터 (정적 JSON)
├── SPEC.md             # 기획 문서
└── README.md           # 이 문서
```

## 📝 데이터 구조

### 핀 리스트 (List)
```json
{
  "id": "unique-id",
  "title": "리스트 제목",
  "description": "리스트 설명",
  "color": "#hex-color",
  "pins": [...]
}
```

### 핀 (Pin)
```json
{
  "latitude": 37.5665,
  "longitude": 126.9780,
  "title": "장소 이름",
  "description": "장소 설명"
}
```

## 🎨 새로운 핀 리스트 추가하기

`data/pins.json` 파일을 편집하여 새로운 핀 리스트를 추가할 수 있습니다:

```json
{
  "lists": [
    {
      "id": "my-new-list",
      "title": "나만의 리스트",
      "description": "나만의 장소 모음",
      "color": "#ff6b6b",
      "pins": [
        {
          "latitude": 37.5665,
          "longitude": 126.9780,
          "title": "서울역",
          "description": "서울특별시 용산구"
        }
      ]
    }
  ]
}
```

## 🎨 사용 가능한 기본 색상

| 색상명 | HEX 코드 |
|--------|----------|
| Gold | `#d4a853` |
| Copper | `#c47d4e` |
| Teal | `#4a9d8e` |
| Coral | `#e07a5f` |
| Indigo | `#5c6bc0` |
| Rose | `#d4648a` |
| Emerald | `#4caf50` |
| Amber | `#ffa726` |

## 📱 반응형 브레이크포인트

- **Desktop**: 768px 이상
- **Tablet**: 768px 이하
- **Mobile**: 400px 이하

## 🛠️ 기술 스택

- **HTML5** / **CSS3** / **JavaScript (ES6+)**
- **[Leaflet](https://leafletjs.com/)** - 오픈소스 지도 라이브러리
- **[Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster)** - 마커 클러스터링
- **[CartoDB](https://carto.com/)** - 다크 테마 맵 타일
- **Google Fonts** - Noto Sans KR, Playfair Display

## 📊 데이터 출처

| 데이터 | 출처 | 라이선스 |
|--------|------|----------|
| 맥도날드, 써브웨이, 도서관, 수영장 위치 | [카카오맵 API](https://developers.kakao.com/) | 카카오 API 이용약관 |
| 중학교, 고등학교 위치 | [카카오맵 API](https://developers.kakao.com/) | 카카오 API 이용약관 |
| 지하철역, 기차역 위치 | [카카오맵 API](https://developers.kakao.com/) | 카카오 API 이용약관 |
| 지하철 노선도 | [OpenStreetMap](https://www.openstreetmap.org/) via Overpass API | ODbL |
| 기차 노선도 | [OpenStreetMap](https://www.openstreetmap.org/) via Overpass API | ODbL |

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포하실 수 있습니다.

### 데이터 라이선스
- 카카오맵 API 데이터: [카카오 API 이용약관](https://developers.kakao.com/terms/latest/ko/site-policy) 준수
- OpenStreetMap 데이터: [ODbL (Open Database License)](https://opendatacommons.org/licenses/odbl/) - © OpenStreetMap contributors

---

Made with ❤️ for exploring places on the map

