#!/usr/bin/env python3
"""
학교 상세 정보 수집 (나이스 교육정보 개방 포털)
- 남/여/공학 구분
- 학생수
- 추후: 학업성취도

출처: 나이스 교육정보 개방 포털 (https://open.neis.go.kr)
라이선스: 공공누리 제1유형
"""

import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

NEIS_API_KEY = os.getenv("NEIS_API_KEY")
BASE_URL = "https://open.neis.go.kr/hub"

# 시도교육청 코드
SIDO_CODES = {
    "서울": "B10",
    "부산": "C10",
    "대구": "D10",
    "인천": "E10",
    "광주": "F10",
    "대전": "G10",
    "울산": "H10",
    "세종": "I10",
    "경기": "J10",
    "강원": "K10",
    "충북": "M10",
    "충남": "N10",
    "전북": "P10",
    "전남": "Q10",
    "경북": "R10",
    "경남": "S10",
    "제주": "T10",
}

# 학교급 코드
SCHOOL_KIND = {
    "중학교": "03",
    "고등학교": "04",
}


def fetch_schools(sido_code, school_kind_code, page=1, per_page=1000):
    """나이스 API에서 학교 기본정보 조회"""
    url = f"{BASE_URL}/schoolInfo"
    params = {
        "KEY": NEIS_API_KEY,
        "Type": "json",
        "pIndex": page,
        "pSize": per_page,
        "ATPT_OFCDC_SC_CODE": sido_code,
        "SCHUL_KND_SC_NM": "중학교" if school_kind_code == "03" else "고등학교",
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # API 응답 구조 확인
        if "schoolInfo" in data:
            # 첫 번째 항목은 메타데이터, 두 번째가 실제 데이터
            if len(data["schoolInfo"]) > 1:
                return data["schoolInfo"][1].get("row", [])
        
        return []
    except Exception as e:
        print(f"  ⚠️ API 오류: {e}")
        return []


def get_coed_type(coedu_sc_nm):
    """남녀공학 구분 변환"""
    if coedu_sc_nm == "남":
        return "남학교"
    elif coedu_sc_nm == "여":
        return "여학교"
    elif coedu_sc_nm == "남여공학":
        return "공학"
    else:
        return coedu_sc_nm or "미분류"


def fetch_all_schools(school_type):
    """전국 학교 정보 수집"""
    school_kind_code = SCHOOL_KIND[school_type]
    all_schools = []
    
    print(f"\n🏫 {school_type} 정보 수집 중...")
    
    for sido_name, sido_code in SIDO_CODES.items():
        print(f"  [{sido_name}] 조회 중...", end=" ")
        
        schools = fetch_schools(sido_code, school_kind_code)
        
        for school in schools:
            school_info = {
                "name": school.get("SCHUL_NM", ""),
                "address": school.get("ORG_RDNMA", "") or school.get("ORG_RDNDA", ""),
                "coed_type": get_coed_type(school.get("COEDU_SC_NM", "")),
                "found_type": school.get("FOND_SC_NM", ""),  # 공립/사립
                "sido": sido_name,
                "school_code": school.get("SD_SCHUL_CODE", ""),
                "neis_code": school.get("ATPT_OFCDC_SC_CODE", "") + school.get("SD_SCHUL_CODE", ""),
            }
            all_schools.append(school_info)
        
        print(f"→ {len(schools)}개")
        time.sleep(0.1)  # API 부하 방지
    
    return all_schools


def merge_with_existing_data(school_info_list, existing_data_path, output_path):
    """기존 위치 데이터와 병합"""
    
    # 기존 데이터 로드
    with open(existing_data_path, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    # 학교명으로 매칭을 위한 딕셔너리 생성
    school_info_map = {}
    for info in school_info_list:
        # 학교명 정규화 (공백 제거, 소문자)
        name_key = info["name"].replace(" ", "").strip()
        school_info_map[name_key] = info
    
    # 기존 데이터에 정보 추가
    matched_count = 0
    for pin in existing_data.get("pins", []):
        title = pin.get("title", "").replace(" ", "").strip()
        
        if title in school_info_map:
            info = school_info_map[title]
            pin["coed_type"] = info["coed_type"]
            pin["found_type"] = info["found_type"]
            pin["neis_code"] = info["neis_code"]
            matched_count += 1
    
    # 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 매칭 완료: {matched_count}/{len(existing_data.get('pins', []))}개")
    print(f"💾 저장 완료: {output_path}")
    
    return existing_data


def save_raw_data(schools, filename):
    """원본 데이터 저장"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(schools, f, ensure_ascii=False, indent=2)
    print(f"📋 원본 데이터 저장: {filepath}")


if __name__ == "__main__":
    if not NEIS_API_KEY:
        print("❌ 오류: NEIS_API_KEY 환경변수가 설정되지 않았습니다.")
        print("   .env 파일에 NEIS_API_KEY=your_key_here 형식으로 추가해주세요.")
        print("   API 키는 https://open.neis.go.kr 에서 발급받을 수 있습니다.")
        exit(1)
    
    print("=" * 50)
    print("🏫 학교 상세 정보 수집 (나이스 API)")
    print("=" * 50)
    
    # 중학교 정보 수집
    middle_schools = fetch_all_schools("중학교")
    save_raw_data(middle_schools, "중학교_neis_raw.json")
    
    # 고등학교 정보 수집
    high_schools = fetch_all_schools("고등학교")
    save_raw_data(high_schools, "고등학교_neis_raw.json")
    
    # 기존 데이터와 병합
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    
    print("\n📝 중학교 데이터 병합 중...")
    merge_with_existing_data(
        middle_schools,
        os.path.join(data_dir, "1.json"),
        os.path.join(data_dir, "1.json")
    )
    
    print("\n📝 고등학교 데이터 병합 중...")
    merge_with_existing_data(
        high_schools,
        os.path.join(data_dir, "9.json"),
        os.path.join(data_dir, "9.json")
    )
    
    print("\n" + "=" * 50)
    print("✅ 완료!")
    print("=" * 50)
    print("\n데이터 출처: 나이스 교육정보 개방 포털 (https://open.neis.go.kr)")
    print("라이선스: 공공누리 제1유형")

