
# Chatbot UI

import streamlit as st


def render_chatBot():
    with st.container(border = True):
        st.subheader('🤖 Product AI Assistant')

        st.write('Ask anything about this product.')

        st.text_area('Hello! How can I help you with these headphones?')