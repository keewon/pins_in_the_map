#!/usr/bin/env python3
"""써브웨이 매장 위치 수집"""

from common import fetch_all, DETAILED_REGIONS

NAME = "써브웨이"
LIST_ID = 3
KEYWORDS = ["써브웨이"]  # 카카오맵에서는 "써브웨이"로 표기됨


def filter_subway(doc):
    """써브웨이 매장만 필터링"""
    name = doc.get("place_name", "")
    category = doc.get("category_name", "")
    
    if "써브웨이" not in name and "서브웨이" not in name and "SUBWAY" not in name.upper():
        return False
    if "지하철" in category:
        return False
    return True


if __name__ == "__main__":
    fetch_all(NAME, KEYWORDS, LIST_ID, filter_subway, DETAILED_REGIONS)

