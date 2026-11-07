# env + llm instance

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

def get_llm(): 
    # Load environment variable (api key)
    load_dotenv()

    # Model Instance
    return ChatOpenAI(
        # model = 'nvidia/nemotron-3-ultra-550b-a55b:free',
        # model = 'recursive/flint-v1.0:free',
        # model = 'google/gemma-4-26b-a4b-it:free',
        # model = 'baseten/mammoth-1:free',
        # model = 'dots-studio/dots-3-note-preview:free',
        model = 'nvidia/nemotron-3.5-super-vl:free',
        openai_api_key = os.environ['OPENROUTER_API_KEY'],
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.1,
        max_retries=3,
    )   