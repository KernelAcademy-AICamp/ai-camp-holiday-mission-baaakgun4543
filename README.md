# AI Camp Holiday Mission - 박재형

패스트캠퍼스 AI 부트캠프 Holiday Mission 프로젝트 모음집

## 📋 프로젝트 개요

OpenAI, Anthropic Claude, Google Gemini 등 최신 LLM API를 활용한 5가지 AI 애플리케이션 개발 프로젝트입니다. 웹 크롤링부터 RAG 시스템, 대화형 AI 챗봇까지 실무에 적용 가능한 다양한 AI 기술을 학습하고 구현했습니다.

## 🎯 학습 목표

- ✅ **LLM API 활용**: OpenAI GPT-4, Claude, Gemini API 실전 사용
- ✅ **프롬프트 엔지니어링**: Few-shot Learning, Chain of Thought
- ✅ **RAG 시스템**: 검색 증강 생성 기술 이해 및 구현
- ✅ **웹 크롤링**: Selenium을 활용한 동적 페이지 데이터 수집
- ✅ **대화형 AI**: Function Calling, 메모리 관리, 챗봇 구현
- ✅ **성능 평가**: RAGAS, GPT-4 Judge를 활용한 정량적 평가

## 📂 프로젝트 구조

```
holiday-mission_박재형/
├── mission1_박재형/          # 야놀자 리뷰 크롤러 및 요약
├── mission2_박재형/          # SNS 대화 요약 (다중 LLM 비교)
├── mission3_박재형/          # ChatGPT AI Assistant (Streamlit)
├── mission4_박재형/          # RAG 시스템 구현 및 평가
├── mission5_박재형/          # 메뉴뚝딱 AI 챗봇 (Function Calling)
├── .gitignore
└── README.md                 # 이 파일
```

## 📊 미션 요약

| 미션 | 주제 | 핵심 기술 | 주요 기능 | 날짜 |
|------|------|----------|----------|------|
| **Mission 1** | 야놀자 리뷰 크롤링 & 요약 | Selenium, GPT-4, Few-shot Learning | 동적 페이지 크롤링, 별점 추출, 리뷰 요약 | 2025-10-04 |
| **Mission 2** | SNS 대화 요약 시스템 | Claude, Gemini, GPT-3.5/4, Pointwise 평가 | 다중 LLM 성능 비교, 대화 요약, 평가 자동화 | 2025-10-06 |
| **Mission 3** | ChatGPT AI Assistant | Streamlit, LangChain, LCEL, Conversation Memory | 대화형 웹 챗봇, 맥락 유지 (4개 메시지) | 2025-10-07 |
| **Mission 4** | RAG 시스템 구현 | Embeddings, RAGAS, 코사인 유사도 | 문서 검색, 증강 생성, 성능 평가 | 2025-10-08 |
| **Mission 5** | 메뉴뚝딱 AI 챗봇 | Function Calling, FastAPI, Gradio, MongoDB | 요기요 크롤링, 임베딩 검색, 메뉴 추천 챗봇 | 2025-10-09 |

## 🔧 기술 스택

### AI/ML
- **LLM APIs**: OpenAI GPT-4/3.5, Anthropic Claude 3 Haiku, Google Gemini 2.0 Flash
- **Embeddings**: text-embedding-3-small, text-embedding-3-large
- **Frameworks**: LangChain (LCEL), RAGAS
- **Techniques**: Few-shot Learning, RAG, Function Calling, Prompt Engineering

### Backend
- **FastAPI**: 고성능 API 서버 (Mission 5)
- **Streamlit**: 빠른 프로토타이핑 웹 앱 (Mission 3)
- **Gradio**: 챗봇 UI 프레임워크 (Mission 5)

### Database
- **MongoDB Atlas**: NoSQL 클라우드 데이터베이스 (Mission 5)

### Data Collection
- **Selenium**: 동적 웹 크롤링 (Mission 1, 5)
- **BeautifulSoup4**: HTML 파싱 (Mission 1, 5)

### Development Tools
- **Python 3.13**: 주 개발 언어
- **Jupyter Notebook**: 데이터 분석 및 실험
- **Git/GitHub**: 버전 관리

## 🚀 각 미션 상세 내용

### Mission 1: 야놀자 리뷰 크롤러 및 분석 시스템

**핵심 기술**: Selenium, OpenAI GPT-4, Few-shot Learning

**주요 기능**:
- 야놀자 숙소 리뷰 자동 수집 (별점, 텍스트, 날짜)
- SVG path 분석을 통한 정확한 별점 추출
- GPT-4 기반 리뷰 요약
- 다양한 프롬프트 전략 실험 (Baseline, 1-shot, 2-shot)

**기술적 도전**:
- HTML 구조 변경 대응: SVG 클래스 분석으로 해결
- 별점 추출 정확도 향상: path 데이터 분석

[📖 자세히 보기](./mission1_박재형/)

---

### Mission 2: SNS 대화 요약 시스템

**핵심 기술**: Claude, Gemini, GPT-3.5/4, Pointwise 평가

**주요 기능**:
- AI Hub "SNS 데이터 고도화" 공공 데이터셋 활용
- 3개 LLM 성능 비교 (Claude Haiku, Gemini 2.0, GPT-3.5)
- GPT-4o를 Judge로 사용한 자동 평가
- Few-shot 프롬프트 엔지니어링

**기술적 도전**:
- Anthropic 라이브러리 호환성: 버전 업그레이드로 해결 (0.28.1 → 0.69.0)
- Gemini 모델 종료: 1.5 → 2.0 Flash 마이그레이션
- API 비용 최적화: 평가 샘플 50개 → 8개로 축소 (84% 절감)

**평가 메트릭**: Helpfulness, Relevance, Accuracy (1-10점)

[📖 자세히 보기](./mission2_박재형/)

---

### Mission 3: ChatGPT AI Assistant

**핵심 기술**: Streamlit, LangChain LCEL, Conversation Memory

**주요 기능**:
- GPT-4 기반 실시간 대화형 웹 챗봇
- ConversationBufferWindowMemory로 최근 4개 대화 기억
- LCEL 파이프라인으로 효율적인 LLM 호출
- Streamlit UI로 직관적인 사용자 경험

**구현 특징**:
```python
chain = (
    RunnablePassthrough.assign(
        chat_history=lambda x: memory.load_memory_variables({})["chat_history"]
    )
    | prompt
    | llm
)
```

[📖 자세히 보기](./mission3_박재형/)

---

### Mission 4: RAG 시스템 구현 및 평가

**핵심 기술**: Embeddings, RAGAS, 코사인 유사도

**주요 기능**:
- 한국어 금융 Q&A 데이터셋 (200개)
- 임베딩 기반 문서 검색 (text-embedding-3-large)
- RAG vs Non-RAG 성능 비교
- RAGAS 프레임워크 평가

**RAG 프로세스**:
1. **Retrieve**: 코사인 유사도로 관련 문서 검색
2. **Augment**: 검색한 컨텍스트를 프롬프트에 추가
3. **Generate**: GPT-4로 증강된 답변 생성

**평가 결과**: RAG 적용 시 답변 정확도 대폭 향상

[📖 자세히 보기](./mission4_박재형/)

---

### Mission 5: 메뉴뚝딱 AI 챗봇 시스템

**핵심 기술**: GPT-4 Function Calling, FastAPI, Gradio, MongoDB Atlas

**시스템 아키텍처**:
```
Gradio Web UI → GPT-4 Function Calling → FastAPI Server → MongoDB Atlas
                                            ↓
                                    Vector Search (Embeddings)
```

**주요 기능**:
1. **요기요 리뷰 크롤링**: Selenium으로 리뷰 데이터 수집
2. **임베딩 생성**: OpenAI text-embedding-3-large로 벡터화
3. **시맨틱 검색**: 코사인 유사도 기반 메뉴 추천
4. **대화형 챗봇**: GPT-4가 자동으로 추천 API 호출
5. **에러 처리**: 안정적인 에러 복구 로직

**데이터 파이프라인**:
```
요기요 리뷰 → MongoDB (원본) → 메뉴별 집계 → 임베딩 생성 → MongoDB (벡터)
```

**기술적 도전**:
- Tool Call Response 누락: 에러 처리 강화로 해결
- IndexError 방지: 안전한 top-k 처리 구현

[📖 자세히 보기](./mission5_박재형/)

## 🛠️ 환경 설정

### 1. 공통 요구사항

```bash
# Python 버전
Python 3.8 이상 (권장: 3.13)

# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

### 2. API 키 설정

각 미션 폴더에 `.env` 파일 생성:

```env
# OpenAI (Mission 1, 3, 4, 5)
OPENAI_API_KEY=your_openai_api_key

# Anthropic Claude (Mission 2)
CLAUDE_API_KEY=your_claude_api_key

# Google Gemini (Mission 2)
GOOGLE_API_KEY=your_google_api_key

# MongoDB Atlas (Mission 5)
MONGODB_USERNAME=your_mongodb_username
MONGODB_PASSWORD=your_mongodb_password
```

### 3. 패키지 설치

각 미션 폴더에서:

```bash
pip install -r requirements.txt
```

## 📈 학습 성과

### 기술적 성장
- ✅ 5가지 주요 LLM API 실전 활용 경험
- ✅ 프롬프트 엔지니어링 기법 습득
- ✅ RAG 시스템 end-to-end 구현 능력
- ✅ 웹 크롤링 및 데이터 수집 자동화
- ✅ 대화형 AI 시스템 설계 및 구현

### 문제 해결 능력
- 🔧 라이브러리 호환성 문제 해결
- 🔧 API 비용 최적화 (84% 절감)
- 🔧 동적 웹페이지 크롤링 안정화
- 🔧 에러 처리 및 복구 로직 설계

## 🎯 향후 개선 방향

### Mission 1-4 공통
- [ ] 통합 대시보드 구축 (Streamlit)
- [ ] API 비용 추적 및 모니터링
- [ ] 성능 벤치마크 자동화

### Mission 5 (메뉴뚝딱 AI)
- [ ] 멀티턴 대화 지원
- [ ] 사용자 선호도 학습 및 개인화
- [ ] 가격대, 배달시간 필터링 기능
- [ ] A/B 테스트 프레임워크 구축

## ⚠️ 주의사항

- **API 비용**: 모든 미션에서 OpenAI API 사용 시 비용 발생
- **환경 변수**: `.env` 파일은 절대 Git에 커밋하지 마세요
- **크롤링 윤리**: 적절한 대기시간 설정 및 robots.txt 준수
- **데이터 저장**: 대용량 데이터는 `.gitignore`에 포함

## 📚 참고 자료

### 공식 문서
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [Google Gemini API](https://ai.google.dev/docs)
- [LangChain Documentation](https://python.langchain.com)
- [RAGAS Documentation](https://docs.ragas.io)

### 데이터셋
- [AI Hub - SNS 데이터 고도화](https://www.aihub.or.kr/)
- [Hugging Face - RAG-KO](https://huggingface.co/datasets/allganize/rag-ko)

### 프레임워크
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Gradio](https://www.gradio.app/)

## 👤 작성자

**박재형**
- 패스트캠퍼스 AI 부트캠프
- AI Camp Holiday Mission
- 프로젝트 기간: 2025-10-04 ~ 2025-10-09

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

---

**🤖 Generated with [Claude Code](https://claude.com/claude-code)**

**Co-Authored-By: Claude <noreply@anthropic.com>**
