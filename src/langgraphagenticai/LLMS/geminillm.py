import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiLLM:
    """Google Gemini language model integration for agentic AI workflows.
    
    Provides interface to Google's advanced language models with configurable
    temperature and error handling for production deployments.
    """
    
    def __init__(self):
        """Initialize Gemini LLM handler."""
        pass

    def get_llm_model(self):
        """Load and configure Google Gemini language model with API authentication.
        
        Retrieves API key from Streamlit secrets and initializes ChatGoogleGenerativeAI
        with production-grade temperature settings (0.7 for balanced creativity/consistency).
        
        Returns:
            ChatGoogleGenerativeAI: Configured Gemini model instance ready for inference.
            
        Raises:
            ValueError: When API key is missing or model initialization fails.
        """
        try:
            gemini_api_key = st.secrets["GOOGLE_API_KEY"]
            
            if not gemini_api_key:
                st.error("❌ Google Gemini API key not configured. Please set GOOGLE_API_KEY in secrets.")
                return None

            llm = ChatGoogleGenerativeAI(
                api_key=gemini_api_key,
                model="gemini-2.5-flash-lite",
                temperature=0.7
            )
            return llm

        except KeyError:
            st.error("❌ GOOGLE_API_KEY not found in Streamlit secrets. Configure it in .streamlit/secrets.toml")
            return None
        except Exception as e:
            raise ValueError(f"Error initializing Gemini LLM: {e}")
