import streamlit as st
from models.text_model import MedicalChatbot, TASK_SPECIFIC_INSTRUCTIONS

if "messages" not in st.session_state:
       st.session_state.messages = [
           {'role': "user", "content": TASK_SPECIFIC_INSTRUCTIONS},
           {'role': "assistant", "content": "Understood"},
       ]

chatbot = MedicalChatbot(st.session_state)
for message in st.session_state.messages[2:]:
    # ignore tool use blocks
    if isinstance(message["content"], str):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if user_message := st.chat_input("Ask questions here"):
    st.chat_message("user").markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Eva is thinking..."):
            response_placeholder = st.empty()
            full_response = chatbot.process_user_input(user_message)
            response_placeholder.markdown(full_response)


