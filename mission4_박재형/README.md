# Mission 4: RAG (Retrieval-Augmented Generation) 시스템 구현 및 평가

OpenAI API를 활용한 RAG 시스템 구현 및 성능 평가 프로젝트

## 📋 프로젝트 개요

이 프로젝트는 **RAG (검색 증강 생성)** 기술을 이해하고 구현하는 것을 목표로 합니다. 한국어 금융 Q&A 데이터셋을 사용하여 임베딩 기반 검색과 GPT-4를 활용한 답변 생성을 구현하고, RAG 적용 전후의 성능을 비교 평가합니다.

## 🎯 학습 목표

- **RAG 개념 이해**: 검색(Retrieve), 증강(Augment), 생성(Generate)의 3단계 프로세스
- **임베딩(Embedding) 활용**: 텍스트를 벡터로 변환하고 코사인 유사도로 관련성 측정
- **성능 평가**: RAGAS 프레임워크를 활용한 정량적 평가
- **RAG의 효과**: 컨텍스트 제공 여부에 따른 답변 품질 비교

## 📁 프로젝트 구조

```
mission4_박재형/
├── README.md                 # 프로젝트 설명 문서
├── requirements.txt          # 필요한 Python 패키지 목록
├── utils.py                  # OpenAI API 유틸리티 함수
│
├── intro.ipynb              # 프로젝트 소개 및 개요
├── embedding.ipynb          # 임베딩 개념 및 실습
├── rag_data.ipynb           # RAG 데이터 준비 및 전처리
├── rag_eval.ipynb           # RAG 성능 평가
└── rag_exercise.ipynb       # RAG vs Non-RAG 비교 실습
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 패키지 설치
pip install -r requirements.txt
```

### 2. OpenAI API 키 설정

```bash
# .env 파일 생성 후 API 키 입력
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 3. 실습 순서

1. **`intro.ipynb`** - 프로젝트 개요 및 RAG 개념 소개
2. **`embedding.ipynb`** - 임베딩과 코사인 유사도 이해
3. **`rag_data.ipynb`** - 데이터셋 준비 및 전처리
4. **`rag_eval.ipynb`** - RAG 시스템 성능 평가
5. **`rag_exercise.ipynb`** - RAG 효과 비교 실습

## 📊 데이터셋

- **출처**: [Hugging Face - allganize/rag-ko](https://huggingface.co/datasets/allganize/rag-ko)
- **내용**: 한국어 금융 도메인 Q&A 데이터
- **규모**: 200개의 질문-답변 쌍
- **구성**: 각 질문마다 3개의 후보 컨텍스트 제공

## 🔧 주요 기능

### 1. 임베딩 생성 (`embedding.ipynb`)
- OpenAI의 `text-embedding-3-small` 및 `text-embedding-3-large` 모델 활용
- 텍스트를 고차원 벡터로 변환
- 코사인 유사도로 문서 간 관련성 측정

### 2. RAG 데이터 준비 (`rag_data.ipynb`)
- Hugging Face 데이터셋 다운로드
- 시스템 프롬프트에서 컨텍스트 추출
- Pickle 형식으로 데이터 저장

### 3. RAG 성능 평가 (`rag_eval.ipynb`)
- 질문과 컨텍스트 간 유사도 계산
- 가장 관련 있는 컨텍스트 자동 선택
- 정확도 및 RAGAS 메트릭 측정

### 4. RAG 효과 비교 (`rag_exercise.ipynb`)
- **Non-RAG**: 컨텍스트 없이 GPT-4 직접 답변
- **RAG**: 검색한 컨텍스트를 활용한 답변
- Answer Correctness 메트릭으로 품질 비교

## 📈 평가 메트릭

### RAGAS (RAG Assessment) 메트릭
- **Context Recall**: 정답을 포함하는 컨텍스트를 얼마나 잘 찾았는가
- **Context Precision**: 검색한 컨텍스트의 정확도
- **Context Relevancy**: 컨텍스트와 질문의 관련성
- **Answer Correctness**: 생성된 답변의 정확도
- **Faithfulness**: 답변이 컨텍스트에 충실한 정도

## 🔬 실험 결과

### RAG 적용 전후 비교

| 구분 | 컨텍스트 | 정보 출처 | 정확도 |
|------|---------|---------|--------|
| **Non-RAG** | ❌ 없음 | GPT-4 학습 데이터 | 낮음 |
| **RAG** | ✅ 있음 | 특정 문서 검색 | **높음** ⬆️ |

### 핵심 인사이트
- RAG를 적용하면 실제 정답에 더 가까운 답변 생성
- 구체적이고 상세한 정보 제공 가능
- 문서 기반의 정확한 사실 관계 유지

## 🛠️ 주요 기술 스택

- **Python 3.13**
- **OpenAI API** - GPT-4, Embedding 모델
- **RAGAS** - RAG 시스템 평가 프레임워크
- **Hugging Face** - 데이터셋
- **Pandas** - 데이터 처리
- **NumPy** - 수치 연산

## 📚 참고 자료

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [RAGAS Documentation](https://docs.ragas.io/)
- [Hugging Face Datasets](https://huggingface.co/docs/datasets)
- [RAG 개념 설명](https://www.pinecone.io/learn/retrieval-augmented-generation/)

## 💡 주요 개념 설명

### RAG (Retrieval-Augmented Generation)
1. **Retrieve (검색)**: 질문과 관련된 문서/컨텍스트를 검색
2. **Augment (증강)**: 검색한 컨텍스트를 프롬프트에 추가
3. **Generate (생성)**: 증강된 프롬프트로 AI가 답변 생성

### 임베딩 (Embedding)
- 텍스트를 고차원 벡터(숫자 배열)로 변환
- 의미가 비슷한 텍스트는 비슷한 벡터 값을 가짐
- 코사인 유사도로 두 벡터 간 유사도 측정 (0~1)

### 코사인 유사도 (Cosine Similarity)
- 두 벡터의 방향이 얼마나 비슷한지 측정
- 1에 가까울수록 유사, 0에 가까울수록 상이
- 텍스트 검색에서 관련성 측정에 활용

## 🎓 학습 포인트

### 초보자를 위한 가이드
모든 노트북 파일에는 **주니어 개발자도 이해할 수 있는 상세한 마크다운 설명**이 포함되어 있습니다:

- 각 코드 셀의 목적과 동작 과정
- 주요 함수/변수 설명
- 실행 결과 해석
- 개념 설명 및 비유
- 실전 적용 방법

### 핵심 학습 내용
1. **임베딩 이해**: 텍스트를 벡터로 변환하는 원리
2. **유사도 측정**: 코사인 유사도를 활용한 문서 검색
3. **RAG 프로세스**: 3단계 파이프라인 구현
4. **성능 평가**: RAGAS를 활용한 정량적 평가

## 🔄 재현 방법

### 전체 파이프라인 실행
```bash
# 1. 데이터 준비
jupyter notebook rag_data.ipynb

# 2. 성능 평가
jupyter notebook rag_eval.ipynb

# 3. RAG 효과 비교
jupyter notebook rag_exercise.ipynb
```

## ⚠️ 주의사항

- **API 비용**: OpenAI API 사용 시 비용이 발생할 수 있습니다
- **데이터 크기**: `res/rag-ko/` 폴더는 `.gitignore`에 포함되어 있습니다
- **환경 변수**: `.env` 파일에 API 키를 안전하게 보관하세요
- **재생성 가능**: `.pkl` 파일은 재생성 가능하므로 Git에서 제외됩니다

## 📝 라이선스

이 프로젝트는 학습 목적으로 제작되었습니다.

## 👤 작성자

박재형 - AI Camp Holiday Mission

---

**🤖 Generated with [Claude Code](https://claude.com/claude-code)**
