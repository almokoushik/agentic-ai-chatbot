import streamlit as st

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    ChatGoogleGenerativeAI = None


class GeminiLLM:
    """Google Gemini language model integration for agentic AI workflows.
    
    Provides interface to Google's advanced language models with configurable
    temperature and error handling for production deployments.
    """
    
    def __init__(self):
        """Initialize Gemini LLM handler."""
        if not GEMINI_AVAILABLE:
            st.warning("⚠️ Gemini LLM support is not available. Install langchain-google-genai package.")

    def get_llm_model(self):
        """Load and configure Google Gemini language model with API authentication.
        
        Retrieves API key from Streamlit secrets and initializes ChatGoogleGenerativeAI
        with production-grade temperature settings (0.7 for balanced creativity/consistency).
        
        Returns:
            ChatGoogleGenerativeAI: Configured Gemini model instance ready for inference.
            
        Raises:
            ValueError: When API key is missing or model initialization fails.
        """
        if not GEMINI_AVAILABLE:
            st.error("❌ Gemini LLM unavailable. Please install langchain-google-genai: pip install langchain-google-genai")
            return None
            
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
