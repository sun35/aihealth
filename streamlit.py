import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Chatbot Demos 😎")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    We built some example chatbots with integrations like Slack and Github. \n
    **👈 Select a demo from the sidebar** to see some examples
    of what it can do!
"""
)