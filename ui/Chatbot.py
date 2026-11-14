
# Chatbot UI

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from config import get_llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
# Model
model = get_llm()


def render_chatBot():

    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.container(border = True):

        st.markdown("""
            <div class='chat-header'>
                <img src="https://tse1.mm.bing.net/th/id/OIP.K_DsBNDJlsds4cl4AJTX0gHaJQ?r=0&rs=1&pid=ImgDetMain&o=7&rm=3">
                <div class='chat-header-div'>
                    <h3>Product AI Assistant</h3>
                    <p>Ask anything about this product.</p>
                </div>
                
            </div>
        """, unsafe_allow_html=True)
      
        def get_history():
            history = []

            for msg in st.session_state.messages:

                if( msg['role'] == 'user'):
                    history.append(HumanMessage(msg['content']))
                else:
                    history.append(AIMessage(msg['content']))
            return history
        
        # Show chat history
        with st.container(height=450, border=1):
            for msg in get_history():
                if(msg.type == 'human'):
                    st.write(f'👤 : {msg.content}')
                else:
                    st.write(f'🤖 : {msg.content}')


        with st.form(key="chat_form", clear_on_submit=True):
            input_col, sendbtn_col = st.columns([0.90, 0.10])
            with input_col:
                user_input = st.text_area(
                    'Message',
                    placeholder='Hello! How can I help you with this product?',
                    label_visibility='collapsed')
            
            with sendbtn_col:
                submitted = st.form_submit_button('➤', use_container_width=True)

            if submitted and user_input.strip():
    
                # Prompt template 
                prompt = ChatPromptTemplate([
                    ('system', """
                            You are a helpful, Concise supportive agent. 
                            Your goal is to help user to answer all the queries related to the provided product detail.
                            Please don't answer any unrelated queries. 
                            Your tone must be polite and helpful. 
                            Guide the user they should buy this product or not based on this detail: 
                            product detail: {product_detail}.
                            If you don't found the answer simply say "Sorry This information is not available". 
                        """),
                    ('human', f'{user_input}')
                ])

                chain = prompt | model | StrOutputParser()

                result = chain.invoke({
                    'product_detail': st.session_state["product"],
                    'user_input': user_input, 
                    'history': get_history()})
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "Agent", "content": result})
        

                