import streamlit as st
from chatbot.chat import add_message, print_messages, handle_user_input
from chatbot.chain import create_retriever
from preprocessing.data import make_metadata
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv
from common import langsmith

load_dotenv()
langsmith("LEGAL_CASE_SEARCH_CHATBOT")

data = make_metadata("./data")
retriever = create_retriever(data)

# Streamlit UI 설정
st.set_page_config(page_title="판례 검색 챗봇")
st.title("판례 검색 챗봇")
st.write("확인하고자 하는 형법의 사건 내용을 적어주세요.")

# 대화기록 저장 용도로 처음 1번만 실행
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True, memory_key="chat_history"
    )
print(st.session_state["memory"].load_memory_variables({}))

# 대화 초기화 버튼
with st.sidebar:
    clear_btn = st.button("대화 초기화")

# 초기화 버튼이 눌리면
if clear_btn:
    st.session_state["messages"] = []
    st.session_state["memory"].clear()

# 이전 대화 기록 출력
print_messages()

# 사용자의 입력
user_input = st.chat_input("내용을 적어주세요")

if user_input:
    st.chat_message("user").write(user_input)
    with st.chat_message("assistant"):
        container = st.empty()
        response = handle_user_input(user_input, retriever, st.session_state["memory"])
        ai_answer = ""
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)
        add_message("user", user_input)
        add_message("assistant", ai_answer)
        st.session_state["memory"].save_context(
            {"user": user_input}, {"assistant": ai_answer}
        )
        print(st.session_state["memory"].load_memory_variables({}))
