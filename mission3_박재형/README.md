# Mission 3: ChatGPT AI Assistant

Streamlit 기반 대화형 AI 챗봇 애플리케이션

## 📋 프로젝트 개요

OpenAI GPT-4와 LangChain을 활용한 대화형 AI Assistant 웹 애플리케이션입니다.
- **프레임워크**: Streamlit
- **AI 모델**: OpenAI GPT-4
- **대화 메모리**: LangChain ConversationBufferWindowMemory (최근 4개 대화 기억)
- **구현 방식**: LCEL (LangChain Expression Language) 파이프라인

## ✨ 주요 기능

- 🤖 GPT-4 기반 자연어 대화
- 💬 실시간 채팅 인터페이스
- 🧠 대화 맥락 유지 (최근 4개 메시지)
- 🎨 Streamlit UI로 직관적인 사용자 경험
- ⚡ LCEL 파이프라인을 통한 효율적인 LLM 호출

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI Framework**: LangChain (LCEL)
- **LLM**: OpenAI GPT-4
- **Language**: Python 3.x
- **Environment**: python-dotenv

## 📦 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/KernelAcademy-AICamp/ai-camp-holiday-mission-baaakgun4543.git
cd ai-camp-holiday-mission-baaakgun4543/mission3_박재형
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install streamlit openai langchain langchain-openai python-dotenv
```

### 4. 환경 변수 설정
`.env` 파일을 생성하고 OpenAI API 키를 추가합니다:
```
OPENAI_API_KEY=sk-your-api-key-here
```

## 🚀 실행 방법

```bash
streamlit run app.py
```

브라우저가 자동으로 열리며, 다음 주소로 접속할 수 있습니다:
- **Local URL**: http://localhost:8501
- **Network URL**: http://[YOUR_IP]:8501

## 📝 사용 방법

1. 애플리케이션 실행 후 브라우저에서 채팅 인터페이스가 표시됩니다
2. 하단 입력창에 메시지를 입력합니다
3. AI Assistant가 GPT-4를 통해 응답을 생성합니다
4. 대화 내역은 세션 동안 유지되며, 최근 4개 메시지를 기억합니다

## 🏗️ 프로젝트 구조

```
mission3_박재형/
├── app.py              # Streamlit 메인 애플리케이션
├── .env                # 환경 변수 (API 키)
├── .gitignore          # Git 제외 파일 목록
├── README.md           # 프로젝트 문서
└── .venv/              # Python 가상환경
```

## 🔧 주요 구현 내용

### LCEL 파이프라인 구조
```python
chain = (
    RunnablePassthrough.assign(
        chat_history=lambda x: memory.load_memory_variables({})["chat_history"]
    )
    | prompt
    | llm
)
```

### 대화 메모리 관리
- `ConversationBufferWindowMemory`: 최근 4개 대화 유지
- `memory.save_context()`: 대화 히스토리 저장
- Streamlit `session_state`: UI 메시지 상태 관리

## ⚠️ 주의사항

- OpenAI API 키가 필요합니다 (유료)
- `.env` 파일은 절대 공개 저장소에 업로드하지 마세요
- GPT-4 사용 시 API 비용이 발생합니다

## 📸 스크린샷

![ChatGPT AI Assistant 실행 화면](스크린샷%202025-10-07%20오후%205.01.42.png)

## 🔄 업데이트 내역

- **2025-10-07**: 초기 버전 릴리스
  - GPT-4 기반 챗봇 구현
  - LCEL 파이프라인 적용
  - Streamlit UI 구현
  - 대화 메모리 통합

## 👤 Author

**박재형**
- AI Camp Holiday Mission - Mission 3
