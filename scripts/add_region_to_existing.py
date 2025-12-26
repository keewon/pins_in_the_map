"""
기존 데이터에 region 필드 추가
raw 데이터를 다시 가져오지 않고 기존 raw 파일에서 region을 추출해서 핀 데이터 업데이트
"""

import json
from pathlib import Path
from common import extract_region, PROJECT_ROOT

SCRIPTS_DIR = Path(__file__).parent

# 리스트 ID와 raw 파일 매핑
LIST_RAW_MAP = {
    1: "중학교_raw.json",
    2: "맥도날드_raw.json", 
    3: "써브웨이_raw.json",
    4: "공공도서관_raw.json",
    5: "공공수영장_raw.json",
}


def update_pins_with_region(list_id: int, raw_filename: str):
    """raw 데이터에서 region 추출하여 핀 데이터 업데이트"""
    
    raw_path = SCRIPTS_DIR / raw_filename
    pins_path = PROJECT_ROOT / "data" / f"{list_id}.json"
    
    if not raw_path.exists():
        print(f"⚠️  {raw_filename} 파일이 없습니다. 건너뜁니다.")
        return 0
    
    if not pins_path.exists():
        print(f"⚠️  {pins_path} 파일이 없습니다. 건너뜁니다.")
        return 0
    
    # raw 데이터 로드 (place_id -> 장소 데이터)
    with open(raw_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    raw_by_name = {}
    for place in raw_data:
        name = place.get("name", "")
        address = place.get("road_address") or place.get("address", "")
        key = f"{name}|{address}"
        raw_by_name[key] = {
            "region": extract_region(address),
            "url": place.get("url", "")
        }
    
    # 핀 데이터 로드
    with open(pins_path, "r", encoding="utf-8") as f:
        pins_data = json.load(f)
    
    # region 필드 추가
    updated_count = 0
    for pin in pins_data.get("pins", []):
        key = f"{pin['title']}|{pin['description']}"
        if key in raw_by_name:
            pin["region"] = raw_by_name[key]["region"]
            if not pin.get("url") and raw_by_name[key]["url"]:
                pin["url"] = raw_by_name[key]["url"]
            updated_count += 1
        else:
            # raw에서 찾지 못하면 주소에서 직접 추출
            pin["region"] = extract_region(pin.get("description", ""))
            updated_count += 1
    
    # 저장
    with open(pins_path, "w", encoding="utf-8") as f:
        json.dump(pins_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {list_id}.json 업데이트 완료: {updated_count}개 핀에 region 추가")
    return updated_count


def main():
    print("🔄 기존 데이터에 region 필드 추가 시작...\n")
    
    total = 0
    for list_id, raw_filename in LIST_RAW_MAP.items():
        count = update_pins_with_region(list_id, raw_filename)
        total += count
    
    print(f"\n✅ 총 {total}개 핀 업데이트 완료!")


if __name__ == "__main__":
    main()

