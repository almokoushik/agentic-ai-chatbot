import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.LLMS.geminillm import GeminiLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
from src.langgraphagenticai.authentication.google_auth import GoogleAuthHandler
from src.langgraphagenticai.authentication.auth_manager import AuthenticationManager


@st.cache_resource
def get_auth_manager():
    """Initialize cached authentication manager to prevent multiple MongoDB connections."""
    return AuthenticationManager()


def display_user_sidebar(auth_manager, user_email, user_name):
    """Render user profile and API quota management panel in sidebar."""
    with st.sidebar:
        st.divider()
        st.markdown(f"**👤 Logged in as:** {user_name}")
        st.caption(f"Email: {user_email}")
        
        api_calls = auth_manager.get_api_call_count(user_email)
        
        if api_calls < 10:
            st.success(f" API Calls: {api_calls}/20")
        elif api_calls < 20:
            st.warning(f" API Calls: {api_calls}/20")
        else:
            st.error(f" API Calls: {api_calls}/20 (Quota Exceeded)")
        
        if st.button(" Logout", use_container_width=True):
            auth_manager.logout_user()
            st.session_state.authenticated = False
            st.rerun()


def load_langgraph_agenticai_app():
    """Main application orchestrator managing authentication, LLM selection, and agentic workflow execution.
    
    Handles user authentication, LLM initialization (Groq/Gemini), dynamic graph setup,
    and real-time API quota tracking with comprehensive error handling.
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    auth_manager = get_auth_manager()

    if not st.session_state.authenticated:
        GoogleAuthHandler.show_google_login_page()
        return

    user_email = st.session_state.get("user_email", "")
    user_name = st.session_state.get("user_name", "User")
    
    display_user_sidebar(auth_manager, user_email, user_name)
    
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            selected_llm = user_input.get("selected_llm")
            model = None

            if selected_llm == "Groq":
                obj_llm_config = GroqLLM(user_contols_input=user_input)
                model = obj_llm_config.get_llm_model()

            elif selected_llm == "Gemini":
                obj_llm_config = GeminiLLM()
                model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized")
                return

            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No use case selected.")
                return

            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                
                display_result = DisplayResultStreamlit(
                    usecase=usecase, 
                    graph=graph, 
                    user_message=user_message,
                    auth_manager=auth_manager,
                    user_email=user_email
                )
                display_result.display_result_on_ui()
                
            except Exception as e:
                st.error(f"Error: Graph set up failed- {e}")
                return

        except Exception as e:
            st.error(f"Error: {e}")
            return

   
