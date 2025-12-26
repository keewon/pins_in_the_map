# 데이터 수집 스크립트

이 폴더에는 실제 매장 위치 데이터를 수집하는 스크립트들이 있습니다.

## 사전 준비

### 1. 카카오 REST API 키 발급

1. [카카오 개발자 사이트](https://developers.kakao.com) 방문
2. 로그인 후 "내 애플리케이션" 클릭
3. "애플리케이션 추가하기" 클릭
4. 앱 이름 입력 (예: "pins_in_the_map")
5. 생성된 앱 클릭 → "앱 키" 탭에서 **REST API 키** 복사

### 2. 환경 설정

```bash
# 의존성 설치
pip install -r requirements.txt

# API 키 환경변수 설정
export KAKAO_API_KEY="your_rest_api_key_here"
```

## 스크립트 목록

### `fetch_mcdonalds.py` - 맥도날드 매장 수집

전국 맥도날드 매장 위치를 수집하여 `data/2.json`에 저장합니다.

```bash
cd scripts
python fetch_mcdonalds.py
```

**실행 결과:**
- `../data/2.json` - 핀 데이터 (앱에서 사용)
- `mcdonalds_raw.json` - 원본 데이터 백업

## 다른 브랜드 데이터 수집

스크립트를 복사하여 다른 브랜드의 데이터도 수집할 수 있습니다:

```python
# fetch_subway.py 예시
QUERY = "서브웨이"  # 검색 키워드 변경
OUTPUT_FILE = "3.json"  # 출력 파일 변경
```

## API 제한

- 카카오 로컬 API: 일일 30만 건 무료
- 페이지당 최대 15개, 쿼리당 최대 45개 (3페이지)
- 요청 간 0.1~0.2초 딜레이 권장

## 문제 해결

### "KAKAO_API_KEY 환경변수가 설정되지 않았습니다"

```bash
# API 키가 제대로 설정되었는지 확인
echo $KAKAO_API_KEY

# 설정되지 않았다면 다시 설정
export KAKAO_API_KEY="your_key"
```

### 매장 수가 적게 나오는 경우

- `REGIONS` 리스트에 더 많은 지역 추가
- 검색 키워드 변경 (예: "맥도날드" → "맥도날드 드라이브스루")

