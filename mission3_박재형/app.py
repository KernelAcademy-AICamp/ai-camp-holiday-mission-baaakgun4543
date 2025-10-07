import streamlit as st
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드 (.env 파일에 OPENAI_API_KEY=sk-... 형식으로 저장)
load_dotenv()

# OpenAI API 키 가져오기 (환경 변수에서 읽기)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# OpenAI 클라이언트 초기화 (모든 API 호출에 사용됨)
client = OpenAI(api_key=OPENAI_API_KEY)

prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""You are an AI assistant. You are currently
    having a conversation with a human. Answer the questions.

    chat_history: {chat_history},
    Human: {question}
    AI:
    """
)

llm = ChatOpenAI(temperature=0,
                 model='gpt-4',
                 )

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)

# LCEL 파이프라인으로 변경 (LLMChain 대체)
chain = (
    RunnablePassthrough.assign(
        chat_history=lambda x: memory.load_memory_variables({})["chat_history"]
    )
    | prompt
    | llm
)

st.title("ChatGPT AI Assistant")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요, 저는 AI Assistant 박재형입니다."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = chain.invoke({"question": user_prompt})
            ai_response_content = ai_response.content
            st.write(ai_response_content)

            # 메모리에 대화 저장
            memory.save_context({"question": user_prompt}, {"output": ai_response_content})

    new_ai_message = {"role":"assistant", "content": ai_response_content}
    st.session_state.messages.append(new_ai_message)
