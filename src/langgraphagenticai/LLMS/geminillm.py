import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiLLM:
    def __init__(self):
        pass

    def get_llm_model(self):
        try:
            gemini_api_key = api_key = st.secrets["GOOGLE_API_KEY"]
            
            if not gemini_api_key:
                st.error("Please set the GEMINI_API_KEY environment variable")
                return None

            llm = ChatGoogleGenerativeAI(
                api_key=gemini_api_key,
               model="gemini-3-flash-preview",
                temperature=0.7
            )

        except Exception as e:
            raise ValueError(f"Error occurred with Gemini LLM: {e}")
        
        return llm
