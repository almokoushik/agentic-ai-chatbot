import os
import streamlit as st
from langchain_groq import ChatGroq


class GroqLLM:
    def __init__(self, user_contols_input):
        self.user_controls_input = user_contols_input

    def get_llm_model(self):
        try:
            # Load API key from environment variable
            groq_api_key = api_key = st.secrets["GROQ_API_KEY"]
            selected_groq_model = self.user_controls_input.get("selected_groq_model")
            
            if not groq_api_key:
                st.error(" GROQ_API_KEY environment variable is not set")
                return None

            llm = ChatGroq(api_key=groq_api_key, model=selected_groq_model)

        except Exception as e:
            raise ValueError(f"Error occurred with Groq LLM: {e}")
    
        
        return llm