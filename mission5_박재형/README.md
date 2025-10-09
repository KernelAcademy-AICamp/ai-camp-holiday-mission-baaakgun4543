# Mission 5: 메뉴뚝딱 AI - 리뷰 기반 메뉴 추천 챗봇

## 📋 프로젝트 개요

배달의민족 스타일의 메뉴 추천 AI 챗봇입니다. 요기요(Yogiyo) 웹사이트에서 수집한 리뷰 데이터를 OpenAI Embedding으로 벡터화하여, 사용자의 자연어 질문에 가장 적합한 메뉴를 추천합니다.

### 주요 기능

- 🍜 **자연어 기반 메뉴 추천**: "숙취에 좋은 메뉴 추천해줘" 같은 자연어 입력으로 메뉴 추천
- 🤖 **GPT-4 Function Calling**: 대화형 AI와 검색 API의 유기적 결합
- 🔍 **시맨틱 검색**: OpenAI text-embedding-3-large 모델로 의미 기반 검색
- 💬 **Gradio 챗봇 UI**: 사용자 친화적인 웹 인터페이스
- 🗄️ **MongoDB Atlas 연동**: 확장 가능한 데이터 저장소

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐
│  Gradio Web UI  │
│  (demo_chat.py) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐       ┌──────────────────┐
│   GPT-4 + FN    │◄──────┤   OpenAI API     │
│   (Function     │       │  (Completion +   │
│    Calling)     │       │   Embedding)     │
└────────┬────────┘       └──────────────────┘
         │
         ▼
┌─────────────────┐       ┌──────────────────┐
│  FastAPI Server │◄──────┤   MongoDB Atlas  │
│ (recommend_api  │       │  (menu_db)       │
│   _chat.py)     │       │                  │
└─────────────────┘       └──────────────────┘
         ▲
         │
    ┌────┴─────┐
    │  Vector  │
    │  Search  │
    └──────────┘
```

## 🔧 기술 스택

### Backend
- **Python 3.13**
- **FastAPI**: 고성능 추천 API 서버
- **OpenAI API**: GPT-4 (function calling) + text-embedding-3-large
- **MongoDB Atlas**: 벡터 임베딩 저장소

### Frontend
- **Gradio**: 빠른 프로토타이핑용 웹 UI

### Data Collection
- **Selenium**: 동적 웹 크롤링
- **BeautifulSoup4**: HTML 파싱

## 📦 설치 방법

### 1. 가상환경 생성 및 활성화

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
fastapi
uvicorn
selenium
beautifulsoup4
pymongo
python-dotenv
certifi
openai
gradio
numpy
pydantic
```

### 3. 환경변수 설정

`.env` 파일을 프로젝트 루트에 생성:

```env
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
```

## 🚀 실행 방법

### 1단계: API 서버 실행

```bash
cd chat
uvicorn recommend_api_chat:app --reload --port 8000
```

**실행 확인:**
```bash
curl http://localhost:8000/health
# 출력: "OK"
```

### 2단계: 챗봇 실행 (새 터미널)

```bash
cd chat
python demo_chat.py
```

브라우저에서 `http://127.0.0.1:7860` 접속

## 📸 실행 화면

### 정상 작동 화면 - 다이어트 메뉴 추천
![다이어트 메뉴 추천 성공](./스크린샷%202025-10-09%20오후%203.51.47.png)

**시스템 이름**: 먹어본 박재형의 한 마디 ♾

**추천 결과:**
- **추천 사유**: "다이어트에 좋은 메뉴들로 생선이 많아, 생선과 닭의 조화를 즐길 거예요."
- **추천 아이템**:
  1. 육회덮밥
  2. 훈발세트2 (육회100g + 우츠조 + 육딤)
  3. 훈슬세트 1 (육회100g + 연어8 )
  4. 최상급육회 (180g)
  5. 최상급육회 금품 (270g)
  6. 생생한 생연어초밥 6p
  7. 최상급 육회
  8. 핵꿀맛 육회초밥 6p
  9. 육회물면
  10. 생연어덮밥
  11. 훈육회덮밥

GPT-4가 사용자의 "다이어트" 선택에 따라 자동으로 추천 API를 호출하고, 육회바른연어 옥수점의 건강식 메뉴들을 추천합니다.

### API 오류 처리 화면
![에러 처리 화면](./스크린샷%202025-10-09%20오후%205.20.21.png)

**시스템 이름**: 메뉴뚝딱 AI ♾

API 서버가 실행되지 않았을 때의 에러 처리 화면입니다. 사용자가 "숙취에 좋은 메뉴 좀 추천해줄래...?"라고 입력했지만, 백엔드 API 서버가 응답하지 않아 정중하게 에러 메시지를 안내하고 재시도를 제안합니다.

## 📂 프로젝트 구조

```
mission5_박재형/
├── chat/                                # 🤖 챗봇 시스템
│   ├── demo_chat.py                    # Gradio 챗봇 메인 애플리케이션
│   ├── recommend_api_chat.py           # FastAPI 추천 검색 API 서버
│   ├── create_item_pool_chat.ipynb     # 메뉴 DB 생성 및 임베딩 생성
│   ├── function_calling_chat.ipynb     # Function Calling 테스트 노트북
│   ├── assistants_api_chat.ipynb       # OpenAI Assistants API 실험
│   └── test_request_chat.ipynb         # API 엔드포인트 테스트
├── crawler.py                           # 🕷️ 요기요 리뷰 크롤러
├── utils.py                             # 🛠️ 공통 유틸리티 함수
├── recommend_batch.py                   # 📦 배치 추천 시스템
├── demo.py                              # 🎨 Gradio 데모 (간단 버전)
├── mongodb.ipynb                        # 🗄️ MongoDB 연결 테스트
├── test_request.ipynb                   # ✅ API 테스트 노트북
├── .env                                 # 🔐 환경변수 설정
├── requirements.txt                     # 📦 Python 의존성
├── 스크린샷 2025-10-09 오후 3.51.47.png # 📸 챗봇 성공 화면
├── 스크린샷 2025-10-09 오후 5.20.21.png # 📸 에러 처리 화면
└── README.md                            # 📖 프로젝트 문서
```

### Chat 폴더 상세 구조

#### `demo_chat.py` - Gradio 챗봇 UI
**기능:**
- GPT-4 Function Calling 통합
- 대화형 메뉴 추천 인터페이스
- 실시간 에러 처리 및 복구

**핵심 구현:**
```python
# System Prompt
SYSTEM_PROMPT = """당신의 이름은 '메뉴뚝딱AI'이며 당신의 역할은
배달의민족이라는 음식 주문 모바일 어플에서 리뷰 텍스트 기반으로
메뉴를 추천해주는 것입니다."""

# Tool 정의
TOOLS = [{
    "type": "function",
    "function": {
        "name": "recommend",
        "description": "사용자 발화 기반으로 메뉴 추천 API를 호출합니다.",
        "parameters": {...}
    }
}]

# 에러 처리
try:
    tool_result = recommend(**json.loads(tool_args))
except Exception as e:
    tool_response = json.dumps({
        "error": f"오류: {str(e)}",
        "recommendations": []
    }, ensure_ascii=False)
```

#### `recommend_api_chat.py` - FastAPI 추천 API
**엔드포인트:**
- `POST /recommend` - 시맨틱 검색 기반 메뉴 추천
- `GET /health` - 헬스체크

**API 스펙:**
```json
// Request
{
  "query_text": "숙취에 좋은 메뉴 추천해줘"
}

// Response (Top 10)
[
  {
    "_id": "1363980_0",
    "score": 0.85,
    "menu": "해장국",
    "restaurant": "할매해장국",
    "url": "https://www.yogiyo.co.kr/mobile/#/1363980/"
  }
]
```

**추천 알고리즘:**
1. 키워드 추출 (`extract_keywords`)
2. 임베딩 생성 (`get_embedding` - text-embedding-3-large)
3. 코사인 유사도 계산 (`get_most_relevant_indices`)
4. Top-K 결과 반환 (K=10)

#### `create_item_pool_chat.ipynb` - 메뉴 DB 생성
**데이터 파이프라인:**
```
restaurant_db.restaurant_info (원본 리뷰)
           ↓
   메뉴별 리뷰 집계 및 필터링
           ↓
   OpenAI Embedding 생성 (1536차원)
           ↓
menu_db.menu_info (임베딩 + 메타데이터)
```

**생성되는 스키마:**
```json
{
  "_id": "1363980_0",
  "menu": "뿌링클 스틱",
  "restaurant": "BHC-금호동점",
  "url": "https://www.yogiyo.co.kr/mobile/#/1363980/",
  "embeddings": [0.123, -0.456, ...],
  "reviews": ["치킨이 바삭해요", "양이 많아요"]
}
```

#### `function_calling_chat.ipynb` - Function Calling 테스트
**테스트 시나리오:**
1. 사용자 입력: "숙취에 좋은 메뉴 추천해줘"
2. GPT-4가 `recommend` 함수 호출 결정
3. 함수 실행 및 결과 반환
4. GPT-4가 결과를 자연어로 변환

#### `assistants_api_chat.ipynb` - Assistants API 실험
**실험 내용:**
- OpenAI Assistants API 탐색
- Function Calling vs Assistants API 비교
- 멀티턴 대화 가능성 검토

#### `test_request_chat.ipynb` - API 테스트
**테스트 항목:**
- `/recommend` 엔드포인트 정상 동작 확인
- 다양한 쿼리 시나리오 검증
- 응답 시간 측정
- 추천 품질 평가

## 💡 핵심 기능 상세

### 1. GPT-4 Function Calling

**demo_chat.py:**
```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "recommend",
            "description": "사용자 발화 기반으로 메뉴 추천 API를 호출합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_text": {
                        "type": "string",
                        "description": "사용자 발화 텍스트 원문",
                    },
                },
                "required": ["query_text"],
            },
        }
    }
]
```

GPT-4가 사용자 입력을 분석하여 자동으로 `recommend()` 함수를 호출합니다.

### 2. 시맨틱 검색 (Embedding 기반)

**recommend_api_chat.py:**
```python
@app.post("/recommend")
def recommend(query: QueryModel):
    # 키워드 추출
    keywords = extract_keywords(query.query_text)

    # 쿼리 임베딩 생성
    query_embedding = get_embedding(keywords, model='text-embedding-3-large')

    # 코사인 유사도 계산
    context_embeddings = [menu["embeddings"] for menu in menu_db]
    indices, scores = get_most_relevant_indices(query_embedding, context_embeddings)

    # Top 10 결과 반환
    return top_10_menus
```

### 3. 에러 처리 및 복구

**demo_chat.py:**
```python
try:
    # API 호출
    tool_result = recommend(**json.loads(tool_args))
    tool_response = json.dumps(tool_result, ensure_ascii=False)
except Exception as e:
    # 에러 발생 시 빈 결과로 응답
    tool_response = json.dumps({
        "error": f"메뉴 추천 API 호출 중 오류가 발생했습니다: {str(e)}",
        "recommendations": []
    }, ensure_ascii=False)
```

## 📊 데이터 구조

### MongoDB 스키마

**restaurant_db.restaurant_info (크롤링 데이터):**
```json
{
  "_id": "1363980",
  "restaurant": "BHC-금호동점",
  "url": "https://www.yogiyo.co.kr/mobile/#/1363980/",
  "reviews": [
    {
      "menus": "뿌링클,콜라",
      "review_text": "맛있어요!"
    }
  ]
}
```

**menu_db.menu_info (임베딩 데이터):**
```json
{
  "_id": "1363980_0",
  "menu": "뿌링클 스틱",
  "restaurant": "BHC-금호동점",
  "url": "https://www.yogiyo.co.kr/mobile/#/1363980/",
  "embeddings": [0.123, -0.456, ...],  // 1536차원 벡터
  "reviews": ["치킨이 바삭해요", "양이 많아요"]
}
```

## 🔍 주요 알고리즘

### 키워드 추출 (utils.py)

```python
KEYWORDS_CONTEXT = ['해장', '숙취', '다이어트']

def extract_keywords(review_text):
    keywords = []
    for word in review_text.split():
        if any(keyword in word for keyword in KEYWORDS_CONTEXT):
            keywords.append(word)
    return keywords
```

### 코사인 유사도 계산

```python
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_most_relevant_indices(query_embedding, context_embeddings):
    query = np.array(query_embedding)
    context = np.array(context_embeddings)

    similarities = np.array([cosine_similarity(query, ctx) for ctx in context])
    sorted_indices = np.argsort(similarities)[::-1].tolist()

    return sorted_indices, similarities
```

## 🛠️ 개발 과정

### 문제 1: Tool Call Response 누락

**증상:**
```python
openai.BadRequestError: Error code: 400 - "An assistant message with 'tool_calls'
must be followed by tool messages responding to each 'tool_call_id'."
```

**원인:**
- API 호출 실패 시 tool response를 추가하지 않아 메시지 히스토리 불일치

**해결:**
```python
try:
    tool_result = recommend(**json.loads(tool_args))
    tool_response = json.dumps(tool_result, ensure_ascii=False)
except Exception as e:
    tool_response = json.dumps({
        "error": f"오류: {str(e)}",
        "recommendations": []
    }, ensure_ascii=False)

# 반드시 tool response 추가
MESSAGES.append({
    "role": "tool",
    "content": tool_response,
    "tool_call_id": tool_id
})
```

### 문제 2: IndexError - List Index Out of Range

**증상:**
```python
IndexError: list index out of range
# recommend_api_chat.py:57
```

**원인:**
- `indices` 리스트가 비어있거나 menu_db보다 작을 때 발생
- `top_k=10`으로 고정되어 있어 결과가 10개 미만이면 에러

**해결:**
```python
# 수정 전
top_k = 10

# 수정 후
top_k = min(10, len(indices))  # 안전한 처리
```

## 📈 크롤링 시스템

### 요기요 크롤러 (crawler.py)

**주요 개선 사항:**

1. **Headless 모드 제거**: Angular SPA 완전 렌더링 보장
2. **브라우저 인스턴스 재사용**: 약 70% 시간 단축
3. **안정적인 XPath 선택자**: ID 기반 선택자로 안정성 향상
4. **에러 처리**: 한 URL 실패 시에도 계속 진행

**실행 예시:**
```bash
python crawler.py

🚀 브라우저 초기화 중...
✅ 브라우저 초기화 및 주소 설정 완료

[1/3] 크롤링 시작: https://www.yogiyo.co.kr/mobile/#/1363980/
✅ 크롤링 완료: BHC-금호동점 (리뷰 131개)
💾 MongoDB 저장 완료: BHC-금호동점

📊 크롤링 완료: 성공 3개 / 실패 0개
```

## ⚠️ 주의사항

1. **API 서버 먼저 실행**: 챗봇보다 FastAPI 서버를 먼저 실행해야 합니다.
2. **OpenAI API 비용**: 임베딩 생성 및 GPT-4 호출 시 비용 발생
3. **MongoDB 연결**: `.env` 파일의 인증 정보 확인 필요
4. **크롤링 속도**: 요기요 서버 부하 방지를 위해 적절한 지연 시간 유지

## 🔧 문제 해결

### API 서버 연결 실패

**증상:**
```
ConnectionError: HTTPConnectionPool(host='localhost', port=8000):
Max retries exceeded
```

**해결:**
```bash
# 1. API 서버 실행 확인
curl http://localhost:8000/health

# 2. 서버 재시작
cd chat
uvicorn recommend_api_chat:app --reload --port 8000
```

### OpenAI API 키 오류

**증상:**
```
openai.AuthenticationError: Invalid API key
```

**해결:**
- `.env` 파일에서 `OPENAI_API_KEY` 확인
- https://platform.openai.com/api-keys 에서 새 키 발급

### MongoDB 연결 오류

**증상:**
```
pymongo.errors.ServerSelectionTimeoutError:
[SSL: CERTIFICATE_VERIFY_FAILED]
```

**해결:**
```bash
pip install certifi
```

코드에 `tlsCAFile=certifi.where()` 추가 (이미 포함됨)

## 📚 참고 자료

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [OpenAI Embeddings Documentation](https://platform.openai.com/docs/guides/embeddings)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gradio Documentation](https://www.gradio.app/docs/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Selenium Documentation](https://www.selenium.dev/documentation/)

## 🎯 개선 방향

### 향후 개선 사항

1. **멀티턴 대화**: 대화 맥락을 유지하며 추가 질문 처리
2. **필터링 기능**: 가격대, 배달 시간, 리뷰 평점 필터
3. **개인화**: 사용자 선호도 학습 및 추천
4. **성능 최적화**: 임베딩 캐싱, 배치 처리
5. **A/B 테스트**: 다양한 임베딩 모델 비교
6. **실시간 크롤링**: 최신 리뷰 자동 수집

## 👨‍💻 작성자

박재형

## 📄 라이선스

MIT License
