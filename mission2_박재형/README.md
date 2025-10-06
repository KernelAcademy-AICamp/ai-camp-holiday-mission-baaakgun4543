# SNS 데이터 고도화 - 대화 요약 시스템

## 프로젝트 개요
AI Hub의 "297.SNS 데이터 고도화" 공공 데이터셋을 활용하여 다자간 대화 데이터를 LLM(Large Language Model)으로 요약하고 성능을 평가하는 프로젝트입니다.

## 데이터셋 정보
- **출처**: AI Hub - 297.SNS 데이터 고도화
- **데이터 유형**: 한국어 다자간 대화 데이터 (JSON 형식)
- **구성**:
  - Training 데이터: `./res/297.SNS 데이터 고도화/01-1.정식개방데이터/Training/`
  - Validation 데이터: `./res/297.SNS 데이터 고도화/01-1.정식개방데이터/Validation/`
- **데이터 특징**: 2인 대화 및 3인 이상 다자간 대화, 발화 수 30개 이상 대화 선별

## 주요 파일 설명

### 데이터 처리
- **`data.ipynb`**: Validation 데이터 로드 및 전처리
  - 2인 대화 20개, 3인 이상 대화 30개 추출
  - `eval_data.pickle` 생성

- **`data_long.ipynb`**: Claude API를 활용한 대화 확장
  - 3인 대화에 대해 이전 맥락 생성 (3000자 이상)
  - `conv_long.pickle` 생성
  - **중요**: Anthropic 라이브러리 호환성 문제 발생 및 해결

- **`data_train.ipynb`**: Training 데이터 로드
  - 프롬프트 엔지니어링용 학습 데이터 준비
  - `train_data.pickle` 생성

### 모델 평가
- **`baseline.ipynb`**: 다중 LLM 성능 비교
  - Claude 3 Haiku
  - Gemini 2.0 Flash Exp
  - GPT-3.5 Turbo
  - GPT-4o를 Judge로 사용한 Pointwise 평가
  - **최적화**: 8번 셀에서 평가 샘플 수를 50개→8개로 축소 (API 호출 300회→48회, 84% 감소)

- **`llm_comparison.ipynb`**: LLM API 테스트
  - Google Gemini API 테스트
  - Anthropic Claude API 테스트

### 유틸리티
- **`utils.py`**: 핵심 유틸리티 함수
  - `summarize()`: 다중 LLM 요약 통합 인터페이스
  - `shorten_conv()`: 대화 길이 제한 (최대 3000자)
  - `get_prompt()`: Few-shot 프롬프트 생성 (단계별 요약 가이드)

- **`eval.py`**: 평가 함수
  - `pointwise_eval()`: GPT-4o 기반 1-10점 평가
  - 평가 기준: helpfulness, relevance, accuracy

## 기술 스택

### LLM APIs
- **Anthropic Claude**: claude-3-haiku-20240307
- **OpenAI GPT**: gpt-3.5-turbo-0125, gpt-4o-2024-05-13
- **Google Gemini**: gemini-2.0-flash-exp

### Python 라이브러리
```
openai==1.12.0
anthropic==0.69.0
google-generativeai==0.7.0
tqdm
gradio==4.36.1
```

## ⚠️ Anthropic 라이브러리 호환성 문제 및 해결

### 문제 발생
`data_long.ipynb` 5번째 셀 실행 시 다음 에러 발생:
```
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

### 원인 분석
1. **버전 불일치**: 프로젝트 가상환경(`.venv`)에 설치된 `anthropic 0.28.1`과 `httpx 0.28.1` 간의 호환성 문제
2. **API 변경**: `httpx 0.24.0` 이상부터 `proxies` 파라미터가 `mounts`로 변경됨
3. **레거시 코드**: `anthropic 0.28.1`은 구버전 httpx API(`proxies` 파라미터)를 사용하여 충돌 발생

### 해결 방법
가상환경에서 `anthropic` 라이브러리를 최신 버전으로 업그레이드:

```bash
# .venv 가상환경에서 실행
source .venv/bin/activate
pip install --upgrade anthropic
```

**업그레이드 결과**:
- `anthropic`: 0.28.1 → **0.69.0**
- `httpx`: 0.28.1 (유지, 최신 버전과 호환)
- 추가 의존성: `docstring-parser 0.17.0`, `jiter 0.11.0`, `httpcore 1.0.9`

### 실행 후 조치
Jupyter 노트북 사용 시 **커널 재시작 필수**:
- 메뉴: `Kernel` → `Restart` 또는 `Restart & Run All`
- 업데이트된 라이브러리를 메모리에 다시 로드

### 검증
```python
# 버전 확인
import anthropic
import httpx
print(f"anthropic: {anthropic.__version__}")  # 0.69.0
print(f"httpx: {httpx.__version__}")          # 0.28.1
```

## 환경 설정

### 1. 가상환경 생성 및 활성화
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. 패키지 설치
```bash
# 필요한 패키지 설치
source .venv/bin/activate
pip install openai==1.12.0 httpx==0.25.0 anthropic==0.69.0 google-generativeai tqdm ipykernel
```

### 3. Jupyter 커널 등록
```bash
# .venv를 Jupyter 커널로 등록
source .venv/bin/activate
python -m ipykernel install --user --name=mission2_venv --display-name="Python (mission2 .venv)"
```

Jupyter Notebook에서 커널 선택:
- 메뉴: `Kernel` → `Change Kernel` → `Python (mission2 .venv)` 선택
- VS Code: 우측 상단 커널 선택 버튼 → `Python (mission2 .venv)` 선택

### 4. 환경 변수 설정
`.env` 파일 또는 시스템 환경 변수에 API 키 설정:
```bash
export CLAUDE_API_KEY="your-anthropic-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export GOOGLE_API_KEY="your-google-api-key"
```

### 5. Jupyter Notebook 실행
```bash
jupyter notebook
```

**중요**: Jupyter Notebook 실행 후 반드시 커널을 `Python (mission2 .venv)`로 변경하세요!

## 실행 순서

1. **데이터 준비**
   ```
   data_train.ipynb → train_data.pickle 생성
   data.ipynb → eval_data.pickle 생성
   data_long.ipynb → conv_long.pickle 생성 (Claude API 사용)
   ```

2. **평가 실행**
   ```
   baseline.ipynb → 다중 LLM 성능 비교 및 평가
   ```

## 평가 방법론

### 프롬프트 전략
- **Few-shot Learning**: 학습 데이터 예시 포함
- **단계별 요약 가이드**:
  1. 대화 참여자 파악
  2. 주제 식별
  3. 핵심 내용 추출
  4. 감정과 태도 분석
  5. 맥락 이해
  6. 특이사항 기록
  7. 요약문 작성 (200자 내외, 3문장 이내)

### 평가 기준 (GPT-4o Judge)
- Helpfulness: 요약의 유용성
- Relevance: 원본 대화와의 관련성
- Accuracy: 정보의 정확성
- 점수: 1-10점 척도

### 성능 메트릭
- 평균 점수 (Mean Score)
- 표준편차 (Standard Deviation)
- 최고/최저 점수

## 프로젝트 구조
```
.
├── README.md
├── requirements.txt
├── baseline.ipynb          # LLM 성능 비교
├── data.ipynb              # Validation 데이터 처리
├── data_long.ipynb         # 대화 확장 (Claude)
├── data_train.ipynb        # Training 데이터 처리
├── llm_comparison.ipynb    # API 테스트
├── utils.py                # 유틸리티 함수
├── eval.py                 # 평가 함수
└── res/
    ├── 297.SNS 데이터 고도화/
    │   └── 01-1.정식개방데이터/
    │       ├── Training/
    │       └── Validation/
    ├── train_data.pickle
    ├── eval_data.pickle
    └── conv_long.pickle
```

## 주요 기능

### 1. 대화 요약 (utils.py)
```python
from utils import summarize

summary = summarize(
    conversation=conversation_text,
    prompt=custom_prompt,
    model='claude-3-haiku-20240307'  # or 'gpt-3.5-turbo-0125', 'gemini-1.5-flash'
)
```

### 2. 평가 (eval.py)
```python
from eval import pointwise_eval

score = pointwise_eval(
    conversation=original_conversation,
    answer_a=summary
)
```

## 참고사항

- **API 비용**: Claude API 호출당 약 50원 (대화 확장 작업)
- **처리 시간**: Gemini API는 rate limit을 위해 1초 sleep 적용
- **대화 길이 제한**: 최대 3000자로 제한, 초과 시 앞부분 제거
- **데이터 크기**:
  - Training: 2인 대화 데이터
  - Validation: 2인 대화 20개 + 3인 이상 대화 30개

## 트러블슈팅

### Issue 1: Anthropic API 에러
**증상**: `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`
**해결**: 위 "Anthropic 라이브러리 호환성 문제 및 해결" 섹션 참조

### Issue 2: OpenAI API 호환성 에러
**증상**: `baseline.ipynb` 실행 시 `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`
**원인**:
1. 상위 폴더명 변경 시 `.venv` 가상환경 경로 깨짐
2. `openai` 라이브러리와 `httpx` 라이브러리 간의 호환성 문제

**해결**:
```bash
# .venv 재생성
cd /Users/jaehyungpark/Documents/holiday-mission_박재형/mission2_박재형
rm -rf .venv
python -m venv .venv

# 패키지 재설치
source .venv/bin/activate
pip install openai==1.12.0 httpx==0.25.0 anthropic==0.69.0 google-generativeai tqdm ipykernel

# Jupyter 커널 재등록
python -m ipykernel install --user --name=mission2_venv --display-name="Python (mission2 .venv)"
```

이후 Jupyter에서 커널을 `Python (mission2 .venv)`로 변경하고 재시작

**참고**:
- `httpx==0.25.0`은 `openai 1.12.0`과 `anthropic 0.69.0` 모두와 호환됩니다.
- 폴더명을 변경하면 `.venv` 가상환경을 재생성해야 합니다.

### Issue 3: tqdm 위젯 에러
**증상**: `ImportError: IProgress not found. Please update jupyter and ipywidgets`
**해결**: `model.ipynb` 1번 셀 수정
```python
# 기존
from tqdm.notebook import tqdm

# 수정 후
from tqdm import tqdm
```
커널 재시작 후 다시 실행

### Issue 4: Jupyter 커널에서 변경사항 미반영
**해결**: 커널 재시작 (Kernel → Restart)

### Issue 5: API 키 오류
**해결**: 환경 변수가 올바르게 설정되었는지 확인
```python
import os
print(os.environ.get('CLAUDE_API_KEY'))
print(os.environ.get('OPENAI_API_KEY'))
print(os.environ.get('GOOGLE_API_KEY'))
```

### Issue 6: Gemini 모델 404 에러
**증상**: `NotFound: 404 models/gemini-1.5-flash-001 is not found for API version v1beta`
**원인**: Gemini 1.5 Flash 001 모델이 2024년 5월에 종료됨
**해결**: 모든 파일에서 모델명 변경
```python
# 기존
model='gemini-1.5-flash-001'

# 시도 1 (실패 - 1.5 버전 자체가 종료됨)
model='gemini-1.5-flash'

# 최종 해결
model='gemini-2.0-flash-exp'
```

**영향받는 파일**:
- `baseline.ipynb`: 5번 셀, 8번 셀
- `model.ipynb`: 셀 1a24eb10, 74e14ff3
- `README.md`: 문서 업데이트 (gemini-2.0-flash-exp)

## 작성자
박재형

## 날짜
2025-10-06
