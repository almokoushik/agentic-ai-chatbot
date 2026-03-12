import streamlit as st
import os

from src.langgraphagenticai.ui.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                # Check if API key is set in environment
                if not os.environ.get("GROQ_API_KEY"):
                    st.warning("⚠️ GROQ_API_KEY environment variable is not set")
                else:
                    st.success("✅ GROQ_API_KEY loaded from environment")
                
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
            
            elif self.user_controls["selected_llm"] == 'Gemini':
                # Check if API key is set in environment
                if not os.environ.get("GEMINI_API_KEY"):
                    st.warning("⚠️ GEMINI_API_KEY environment variable is not set")
                else:
                    st.success("✅ GEMINI_API_KEY loaded from environment")
                
                # Model selection for Gemini
                model_options = self.config.get_gemini_model_options()
                self.user_controls["selected_gemini_model"] = st.selectbox("Select Model", model_options)

            ## Usecase selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)

        return self.user_controls