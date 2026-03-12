import streamlit as st


class GoogleAuthHandler:
    """
    Handles authentication for the application.
    """

    @staticmethod
    def show_google_login_page():
        """
        Display login page with email/password and sign up options.
        """
        st.set_page_config(page_title="🔐 Login - Agentic AI Chatbot", layout="centered")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.title("🔐 Login")
            st.markdown("---")
            
            # Import here to avoid circular imports
            from src.langgraphagenticai.authentication.auth_manager import AuthenticationManager
            auth_manager = AuthenticationManager()
            
            tab1, tab2 = st.tabs(["Email Login", "Sign Up"])
            
            # Tab 1: Email Login
            with tab1:
                st.subheader("Login with Email & Password")
                
                email = st.text_input(
                    "Email",
                    value="",
                    key="login_email",
                    placeholder="Enter your email"
                )
                password = st.text_input(
                    "Password",
                    value="",
                    key="login_password",
                    type="password",
                    placeholder="Enter your password"
                )
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if st.button("🔑 Login", use_container_width=True):
                        if email and password:
                            try:
                                success, user, message = auth_manager.login_with_email(email, password)
                                if success:
                                    st.session_state.authenticated = True
                                    st.session_state.user_email = email
                                    st.session_state.user_name = user.get("full_name", email.split("@")[0])
                                    st.session_state.user_data = user
                                    st.success("✅ Login successful!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                            except Exception as e:
                                st.error(f"❌ Login error: {e}")
                        else:
                            st.warning("⚠️ Please enter email and password")
                
                with col2:
                    if st.button("📧 Demo Login", use_container_width=True):
                        st.session_state.authenticated = True
                        st.session_state.user_email = "demo@example.com"
                        st.session_state.user_name = "Demo User"
                        st.session_state.user_data = {"full_name": "Demo User"}
                        st.success("✅ Demo login successful!")
                        st.rerun()
                
                st.markdown("---")
                st.caption("💡 Demo Login: Use any email with password 'demo'")
            
            # Tab 2: Sign Up with Email
            with tab2:
                st.subheader("Create Your Account")
                
                signup_name = st.text_input(
                    "Full Name",
                    value="",
                    key="signup_name",
                    placeholder="Enter your full name"
                )
                signup_email = st.text_input(
                    "Email",
                    value="",
                    key="signup_email", 
                    placeholder="Enter your email"
                )
                signup_password = st.text_input(
                    "Password",
                    value="",
                    key="signup_password",
                    type="password",
                    placeholder="Enter your password (min 6 characters)"
                )
                signup_confirm = st.text_input(
                    "Confirm Password",
                    value="",
                    key="signup_confirm",
                    type="password",
                    placeholder="Confirm your password"
                )
                
                if st.button("📝 Sign Up", use_container_width=True):
                    if signup_name and signup_email and signup_password:
                        if len(signup_password) < 6:
                            st.error("❌ Password must be at least 6 characters")
                        elif signup_password != signup_confirm:
                            st.error("❌ Passwords do not match")
                        else:
                            try:
                                success, message = auth_manager.register_user(
                                    email=signup_email,
                                    full_name=signup_name,
                                    password=signup_password,
                                    auth_method="email"
                                )
                                if success:
                                    st.session_state.authenticated = True
                                    st.session_state.user_email = signup_email
                                    st.session_state.user_name = signup_name
                                    st.session_state.user_data = {"full_name": signup_name}
                                    st.success("✅ Account created and logged in!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                            except Exception as e:
                                st.error(f"❌ Sign up error: {e}")
                    else:
                        st.warning("⚠️ Please fill in all fields")

            st.markdown("---")
            st.caption("🤖 Agentic AI Chatbot | Powered by LangGraph")

