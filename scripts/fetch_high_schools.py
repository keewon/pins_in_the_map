#!/usr/bin/env python3
"""고등학교 위치 수집"""

from common import fetch_all, DETAILED_REGIONS

NAME = "고등학교"
LIST_ID = 9
KEYWORDS = ["고등학교"]


def filter_school(doc):
    """고등학교만 필터링 ('학교'로 끝나거나 '예정'이 포함된 것만)"""
    name = doc.get("place_name", "")
    category = doc.get("category_name", "")
    
    if "고등학교" not in name:
        return False
    if "교육" not in category and "학교" not in category:
        return False
    # '학교'로 끝나거나 '예정'이 포함되면 통과
    if name.endswith("학교") or "예정" in name:
        return True
    return False


if __name__ == "__main__":
    fetch_all(NAME, KEYWORDS, LIST_ID, filter_school, DETAILED_REGIONS)

