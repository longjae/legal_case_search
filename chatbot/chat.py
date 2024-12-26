import streamlit as st
from langchain_core.messages.chat import ChatMessage
from chatbot.chain import create_chain


def print_messages():
    for chat_message in st.session_state["messages"]:
        if chat_message.role == "user":
            st.chat_message("user").write(chat_message.content)
        elif chat_message.role == "assistant":
            st.chat_message("assistant").write(chat_message.content)


def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))


def handle_user_input(user_input, retriever, memory):
    # 체인 생성
    chain = create_chain(retriever, memory)
    # 체인 실행 및 결과 반환
    response = chain.stream({"question": user_input})
    return response
