# 야놀자 리뷰 크롤러 및 분석 시스템

야놀자 숙소 리뷰를 크롤링하고 OpenAI API를 활용하여 요약 및 평가하는 시스템입니다.

## 📋 프로젝트 구조

```
mission1_20251003/
├── crawler.py              # 야놀자 리뷰 크롤러 (별점 추출 포함)
├── crawler_debug.py        # HTML 구조 분석용 디버그 크롤러
├── model.ipynb             # 리뷰 요약 및 평가 노트북
├── res/
│   └── reviews.json        # 크롤링된 리뷰 데이터
├── .env                    # OpenAI API 키 설정
└── requirements.txt        # Python 패키지 의존성
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux

# 패키지 설치
pip install -r requirements.txt
```

### 2. API 키 설정

`.env` 파일 생성:

```
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. 크롤러 실행

```bash
python crawler.py
```

**출력**: `./res/reviews.json` (리뷰 데이터)

### 4. 분석 노트북 실행

Jupyter Notebook 실행:

```bash
jupyter notebook model.ipynb
```

## 🔧 주요 기능

### 1. 야놀자 리뷰 크롤러 (`crawler.py`)

- ✅ Selenium을 사용한 동적 페이지 크롤링
- ✅ 별점 정확 추출 (SVG path 분석)
- ✅ 리뷰 텍스트, 별점, 날짜 수집
- ✅ JSON 형식으로 저장

**별점 추출 알고리즘**:
- 야놀자는 활성 별(⭐)과 비활성 별(☆)을 같은 CSS 클래스로 표시
- SVG `path` 데이터 분석으로 정확한 별점 추출
  - 채워진 별: `path d="M12.638..."` → 카운트
  - 빈 별: `path d="M10.693..."` → 제외

### 2. 리뷰 분석 시스템 (`model.ipynb`)

- ✅ OpenAI API를 활용한 리뷰 요약
- ✅ GPT-4를 사용한 요약 품질 평가
- ✅ 다양한 프롬프트 엔지니어링 실험
- ✅ Few-shot Learning 지원

**실험 종류**:
1. Baseline: 기본 프롬프트
2. Prompt Engineering: 구체적 조건 추가
3. 1-shot Learning: 예시 1개 제공
4. 2-shot Learning: 예시 2개 제공

## 📊 데이터 구조

### reviews.json

```json
[
  {
    "review": "리뷰 텍스트",
    "stars": 5,
    "date": "2025.09.30"
  }
]
```

## 🔍 개발 과정

### 문제 1: 모든 별점이 0점

**원인**: HTML 구조 변경으로 기존 크롤러가 별점 추출 실패

**해결**: SVG 클래스 기반 추출로 수정

### 문제 2: 모든 별점이 5점

**원인**: 야놀자가 활성/비활성 별을 같은 클래스로 표시

**해결**: SVG `path` 데이터 분석으로 정확한 별점 추출

자세한 내용은 `model.ipynb`의 "크롤러 별점 추출 개선" 섹션 참고.

## 📝 요구사항

### Python 패키지

```
selenium
beautifulsoup4
openai
python-dotenv
tqdm
jupyter
python-dateutil
```

### 시스템 요구사항

- Python 3.8+
- Chrome 브라우저
- ChromeDriver (자동 설치됨)

## ⚠️ 주의사항

- **API 비용**: OpenAI API 사용 시 비용 발생
- **크롤링 윤리**: 적절한 대기시간(`SCROLL_PAUSE_TIME`) 설정
- **환경 변수**: `.env` 파일을 Git에 커밋하지 마세요

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 👤 작성자

박재형 (2025-10-04)
