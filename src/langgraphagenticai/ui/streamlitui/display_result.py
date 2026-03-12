import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message, auth_manager=None, user_email=None):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        self.auth_manager = auth_manager
        self.user_email = user_email

    @staticmethod
    def extract_content(message_content):
        """
        Extract text content from both Groq (string) and Gemini (list) formats.
        
        Groq format: "Hello. How are you?"
        Gemini format: [{'type': 'text', 'text': 'Hello! How can I help?', ...}]
        """
        if isinstance(message_content, str):
            # Groq format - content is already a string
            return message_content
        elif isinstance(message_content, list):
            # Gemini format - content is a list of dicts
            text_parts = []
            for item in message_content:
                if isinstance(item, dict) and 'text' in item:
                    text_parts.append(item['text'])
            return ' '.join(text_parts)
        else:
            # Fallback for unknown formats
            return str(message_content)

    def display_result_on_ui(self):
        # Check quota before processing
        user_email = self.user_email or st.session_state.get("user_email")
        
        if not user_email:
            st.error("❌ User not authenticated")
            return
        
        if not self.auth_manager:
            st.error("❌ Authentication manager not initialized")
            return
        
        # Get current API call count
        current_calls = self.auth_manager.get_api_call_count(user_email)
        
        # Check if quota exceeded (limit: 20 calls)
        if self.auth_manager.check_quota_limit(user_email, limit=20):
            st.error("❌ API Quota Exceeded! You have reached the maximum of 20 API calls.")
            return
        
        # Display warning at 10 calls
        if current_calls >= 10:
            st.warning(f"⚠️ You have used {current_calls} API calls. Maximum allowed: 20")
        
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        print(user_message)
        
        if usecase == "Basic Chatbot":
            try:
                for event in graph.stream({'messages': ("user", user_message)}):
                    print(event.values())
                    for value in event.values():
                        print(value['messages'])
                        with st.chat_message("user"):
                            st.write(user_message)
                        with st.chat_message("assistant"):
                            # Extract content handling both Groq (string) and Gemini (list) formats
                            response_text = self.extract_content(value["messages"].content)
                            st.write(response_text)
                
                # Increment API call count after successful call
                new_call_count = self.auth_manager.increment_api_call(user_email)
                st.session_state["api_calls"] = new_call_count
                
                # Display updated call count
                st.success(f"✅ API Calls Used: {new_call_count}/20")
                
            except Exception as e:
                st.error(f"❌ Error processing message: {e}")
