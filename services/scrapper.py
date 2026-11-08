
# Fetch a web page content
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

def fetch_page_text(url: str) -> str:

    # fetch webpage detail
    loader = WebBaseLoader(url)
    document = loader.load()
    # st.write(document[0])
    # if not document or document[0].page_content.strip():
    #     raise ValueError("Page se content nahi mila")
    return document[0].page_content
   