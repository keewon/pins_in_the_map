# 데이터 수집 스크립트

이 폴더에는 위치 데이터를 수집하는 스크립트들이 있습니다.

## 사전 준비

### 1. API 키 발급

#### 카카오 REST API 키
1. [카카오 개발자 사이트](https://developers.kakao.com) 방문
2. 로그인 후 "내 애플리케이션" → "애플리케이션 추가하기"
3. 앱 이름 입력 (예: "pins_in_the_map")
4. 생성된 앱 → "앱 키" 탭에서 **REST API 키** 복사

#### 나이스 교육정보 API 키 (학교 정보용)
1. [나이스 교육정보 개방 포털](https://open.neis.go.kr) 방문
2. 회원가입 후 로그인
3. "인증키 신청" → API 키 발급

### 2. 환경 설정

```bash
# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. API 키 설정

프로젝트 루트에 `.env` 파일 생성:

```bash
# 카카오 REST API 키
KAKAO_API_KEY=your_kakao_api_key_here

# 나이스 교육정보 API 키
NEIS_API_KEY=your_neis_api_key_here
```

## 스크립트 목록

### 위치 데이터 수집 (카카오맵 API)

| 스크립트 | 설명 | 출력 파일 |
|----------|------|-----------|
| `fetch_middle_schools.py` | 중학교 위치 | `data/1.json` |
| `fetch_mcdonalds.py` | 맥도날드 매장 | `data/2.json` |
| `fetch_subway.py` | 써브웨이 매장 | `data/3.json` |
| `fetch_libraries.py` | 도서관 | `data/4.json` |
| `fetch_swimming_pools.py` | 수영장 | `data/5.json` |
| `fetch_stations.py` | 지하철/기차역 | `data/6,7,8.json` |
| `fetch_high_schools.py` | 고등학교 위치 | `data/9.json` |

### 노선도 데이터 수집 (OpenStreetMap)

| 스크립트 | 설명 | 출력 파일 |
|----------|------|-----------|
| `fetch_subway_lines.py` | 지하철 노선도 | `data/subway_lines.json` |
| `fetch_train_lines.py` | 기차 노선도 | `data/train_lines.json` |

### 학교 상세 정보 (나이스 API)

| 스크립트 | 설명 | 기능 |
|----------|------|------|
| `fetch_school_info.py` | 학교 상세 정보 | 남/여/공학 구분, 학생수 등 |

```bash
# 예시: 학교 상세 정보 수집
python fetch_school_info.py
```

## API 제한

### 카카오 로컬 API
- 일일 30만 건 무료
- 페이지당 최대 15개, 쿼리당 최대 45개 (3페이지)
- 요청 간 0.1초 딜레이 권장

### 나이스 API
- 일일 10,000건 (기본)
- 요청 간 0.1초 딜레이 권장

## 문제 해결

### "API_KEY 환경변수가 설정되지 않았습니다"

`.env` 파일이 올바르게 설정되었는지 확인:

```bash
cat .env
```

### 매장 수가 적게 나오는 경우

- `DETAILED_REGIONS` 리스트에 더 많은 세부 지역 추가
- 카카오 API는 쿼리당 최대 45개 제한이 있어 지역을 세분화해야 함

