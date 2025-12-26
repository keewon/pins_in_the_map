#!/usr/bin/env python3
"""공공도서관 위치 수집"""

from common import fetch_all, DETAILED_REGIONS

NAME = "공공도서관"
LIST_ID = 4
KEYWORDS = [
    "도서관",           # 일반 도서관 검색 추가
    "공공도서관",
    "시립도서관",
    "구립도서관",
    "군립도서관",
    "도립도서관",
    "국립도서관",
]


def filter_library(doc):
    """공공도서관만 필터링"""
    name = doc.get("place_name", "")
    category = doc.get("category_name", "")
    
    # 도서관이 이름에 포함되어야 함
    if "도서관" not in name:
        return False
    
    # 카테고리가 도서관이어야 함 (카페, 화장실 등 제외)
    if "도서관" not in category:
        return False
    
    # 제외 키워드 (학교도서관, 대학도서관 등)
    exclude = ["학교도서관", "대학도서관", "어린이집", "유치원", "사립"]
    for ex in exclude:
        if ex in name:
            return False
    return True


if __name__ == "__main__":
    fetch_all(NAME, KEYWORDS, LIST_ID, filter_library, DETAILED_REGIONS)

