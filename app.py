
import streamlit as st
from ui.style import load_css
from ui.header import render_header
from ui.product_card import render_productCard
from ui.Chatbot import render_chatBot
from dotenv import load_dotenv
from services.scrapper import fetch_page_text
from services.extracter import fetch_product_detail
from services.scrapper import fetch_productImage


# Page Configuration
st.set_page_config(
    page_title="SmartBuy AI",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Environment variable
load_dotenv() 

# Load a CSS 
load_css()

# Show Header
render_header()

#Search button with product url textbox
url_col, btn_col = st.columns([5,1])
with url_col:
    product_url = st.text_input(
        "Product Url",
        label_visibility='collapsed',
        placeholder='🔗 Enter a product Url here'
    )
with btn_col:
    submit_btn = st.button(
        '🔍 Analyze Product',
        use_container_width=True
    )


if submit_btn:
    if not product_url:
        st.error('Enter a product url')
        st.stop()


    with st.spinner('Reading Product page...'):
       
        page_content = fetch_page_text(product_url)
        try:
            product = fetch_product_detail(page_content)
        except Exception as e:
            st.write(f'Could Not extract web page information: {e}')
            st.stop()

        try:
            image_url = fetch_productImage(product_url)
        except Exception as e:
            st.write(f'Image Error: {e}')
            image_url = None


    st.session_state["product"] = product
    st.session_state["image_url"] = image_url
   
if "product" in st.session_state:
    
    product_col, Chatbot_col = st.columns(2, gap='large', vertical_alignment='top')

    # Render product component
    with product_col:
        render_productCard()

    # Render chatbot component
    with Chatbot_col:
        render_chatBot()




# for ChatBot
# -----------------------------------------------------------------------------------------------------------------------------------
# prompt = ChatPromptTemplate([
#     ('system', """You are Expert Product Advisor Agent that help customer to make decision regarding the product should buy or not.
#         Your Tone Should be polite and helping nature.""")
#     ('human', """{question}""")
# ])

# prompt.invoke({'question': question})


# For Product Information
# -----------------------------------------------------------------------------------------------------------------------------------





