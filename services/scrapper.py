
# Fetch a web page content
from langchain_community.document_loaders import WebBaseLoader

def fetch_page_text(url: str) -> str:

    # fetch webpage detail
    loader = WebBaseLoader(url)
    document = loader.load()

    if not document or document[0].page_content.strip():
        raise ValueError("Page se content nahi mila")
    return document[0].page_content
   