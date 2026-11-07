# Fetch a product detail from extracted text

from config import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.output_parsers import PydanticOutputParser

class ProductInfo(BaseModel):
    name: Optional[str] = Field(None, description="Product name")
    brand: Optional[str] = Field(None, description="Brand name")
    price: Optional[str] = Field(None, description="Current selling price with currency symbol, e.g. '₹854'")
    original_price: Optional[str] = Field(None, description="MRP / price before discount")
    discount: Optional[str] = Field(None, description="Discount percentage")
    rating: Optional[float] = Field(None, description="Average star rating, e.g. 4.0")
    rating_count: Optional[int] = Field(None, description="Total number of ratings")
    key_features: list[str] = Field(default_factory=list, description="Main features of the product")
    specs: dict[str, str] = Field(default_factory=dict, description="Important specifications like material, fit, wash care")
    return_policy: Optional[str] = Field(None, description="Return / exchange policy")
    review_insights: list[str] = Field(default_factory=list, description="What customers praise or complain about, only if present on the page")

parser = PydanticOutputParser(pydantic_object= ProductInfo)


extract_prompt = ChatPromptTemplate([
    ('system', """Fetch the product information only on the webpage content. 
        If the Field is not given then simple set it null or empty list. Don't try to hallucinate. 
        Do not add extra keys or markdown.\n\n{format_instructions}"""),
    ('human', """{page_text}""")
]).partial(format_instructions = parser.get_format_instructions())

chain = extract_prompt | get_llm() | parser

def fetch_product_detail(page_content):
    product = chain.invoke({'page_text': page_content})
    return product