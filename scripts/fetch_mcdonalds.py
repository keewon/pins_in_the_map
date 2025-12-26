#!/usr/bin/env python3
"""
맥도날드 매장 위치 데이터 수집 스크립트
카카오맵 API를 사용하여 전국 맥도날드 위치를 가져옵니다.

사용법:
    1. 카카오 개발자 사이트에서 REST API 키 발급: https://developers.kakao.com
    2. 프로젝트 루트에 .env 파일 생성하고 KAKAO_API_KEY=발급받은키 입력
    3. 스크립트 실행: python fetch_mcdonalds.py
"""

import os
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트의 .env 파일 로드
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# 카카오 REST API 키 (.env 또는 환경변수에서 가져오기)
API_KEY = os.environ.get("KAKAO_API_KEY", "")

# 광역자치단체 기준 검색 (새 매장이 추가되어도 자동으로 검색됨)
REGIONS = [
    # 특별시/광역시
    "서울특별시",
    "부산광역시",
    "대구광역시",
    "인천광역시",
    "광주광역시",
    "대전광역시",
    "울산광역시",
    "세종특별자치시",
    
    # 도 단위
    "경기도",
    "강원특별자치도",
    "충청북도",
    "충청남도",
    "전북특별자치도",
    "전라남도",
    "경상북도",
    "경상남도",
    "제주특별자치도",
    
    # 고속도로 휴게소
    "고속도로 휴게소",
]


def search_keyword(query: str, page: int = 1) -> dict:
    """카카오 키워드 검색 API 호출"""
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    params = {
        "query": query,
        "page": page,
        "size": 15,  # 최대 15개
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def fetch_mcdonalds_in_region(region: str) -> list:
    """특정 지역의 맥도날드 매장 검색"""
    results = []
    
    # 여러 검색어로 검색하여 결과 최대화
    queries = [
        f"{region} 맥도날드",
        f"맥도날드 {region}",
    ]
    
    # 큰 지역은 추가 검색어 사용
    large_regions = ["경기도", "서울특별시", "경상북도", "경상남도", "전라남도"]
    if region in large_regions:
        queries.extend([
            f"{region} 맥도날드 드라이브스루",
            f"{region} 맥도날드 24시",
        ])
    
    for query in queries:
        for page in range(1, 4):  # 최대 3페이지 (45개)
            try:
                data = search_keyword(query, page)
                documents = data.get("documents", [])
                
                if not documents:
                    break
                    
                for doc in documents:
                    # 맥도날드인지 확인 (카테고리 또는 이름으로)
                    place_name = doc.get("place_name", "")
                    category = doc.get("category_name", "")
                    
                    if "맥도날드" in place_name or "McDonald" in place_name:
                        results.append({
                            "id": doc.get("id"),
                            "name": place_name,
                            "address": doc.get("address_name", ""),
                            "road_address": doc.get("road_address_name", ""),
                            "latitude": float(doc.get("y", 0)),
                            "longitude": float(doc.get("x", 0)),
                            "phone": doc.get("phone", ""),
                            "url": doc.get("place_url", ""),
                        })
                
                # 다음 페이지가 없으면 종료
                if data.get("meta", {}).get("is_end", True):
                    break
                    
                time.sleep(0.1)  # API 부하 방지
                
            except Exception as e:
                print(f"  오류 발생 ({query}, page {page}): {e}")
                break
        
        time.sleep(0.1)  # 쿼리 간 딜레이
    
    return results


def remove_duplicates(stores: list) -> list:
    """중복 제거 (카카오 place id 기준)"""
    seen = set()
    unique = []
    
    for store in stores:
        store_id = store.get("id")
        if store_id and store_id not in seen:
            seen.add(store_id)
            unique.append(store)
    
    return unique


def convert_to_pin_format(stores: list) -> list:
    """pins_in_the_map 데이터 형식으로 변환"""
    pins = []
    
    for store in stores:
        pin = {
            "latitude": store["latitude"],
            "longitude": store["longitude"],
            "title": store["name"],
            "description": store["road_address"] or store["address"]
        }
        pins.append(pin)
    
    return pins


def main():
    if not API_KEY:
        print("❌ 오류: KAKAO_API_KEY가 설정되지 않았습니다.")
        print()
        print("사용법:")
        print("  1. 카카오 개발자 사이트 방문: https://developers.kakao.com")
        print("  2. 앱 생성 후 REST API 키 복사")
        print("  3. 프로젝트 루트에 .env 파일 생성:")
        print('     echo \'KAKAO_API_KEY=발급받은키\' > ../.env')
        print("  4. 스크립트 다시 실행")
        return
    
    print("🍔 맥도날드 매장 위치 수집 시작...")
    print(f"   검색할 지역 수: {len(REGIONS)}개")
    print()
    
    all_stores = []
    
    for i, region in enumerate(REGIONS, 1):
        print(f"[{i}/{len(REGIONS)}] {region} 검색 중...")
        stores = fetch_mcdonalds_in_region(region)
        print(f"         → {len(stores)}개 발견")
        all_stores.extend(stores)
        time.sleep(0.2)  # API 부하 방지
    
    # 중복 제거
    unique_stores = remove_duplicates(all_stores)
    print()
    print(f"✅ 총 {len(unique_stores)}개 매장 수집 완료 (중복 제거 후)")
    
    # 데이터 형식 변환
    pins = convert_to_pin_format(unique_stores)
    
    # 파일 저장
    output_path = Path(__file__).parent.parent / "data" / "2.json"
    output_data = {"pins": pins}
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 저장 완료: {output_path}")
    print()
    
    # 원본 데이터도 백업 (디버깅용)
    backup_path = Path(__file__).parent / "mcdonalds_raw.json"
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(unique_stores, f, ensure_ascii=False, indent=2)
    
    print(f"📋 원본 데이터 백업: {backup_path}")


if __name__ == "__main__":
    main()

