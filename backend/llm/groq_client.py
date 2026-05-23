# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# import os

# from backend.utils.config import LLM_MODEL

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# def load_llm():

#     llm = ChatGroq(
#         model_name=LLM_MODEL,
#         groq_api_key=GROQ_API_KEY
#     )

#     return llm

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from backend.utils.config import LLM_MODEL  # ✅

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def load_llm():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Please add it to your .env file.")

    llm = ChatGroq(
        model_name=LLM_MODEL,
        groq_api_key=GROQ_API_KEY
    )
    return llm