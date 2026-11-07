import streamlit as st
from pathlib import Path

def load_css():
    CSS = Path('./assets/style.css').read_text(encoding="utf-8")
    st.markdown(f"""<style>{CSS}</style>""", unsafe_allow_html=True)