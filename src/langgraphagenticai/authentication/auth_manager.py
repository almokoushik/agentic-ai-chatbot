import streamlit as st
import bcrypt
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


class AuthenticationManager:
    """
    Handles user authentication with MongoDB backend and quota tracking.
    """

    def __init__(self):
        self.db = None
        self.users_collection = None
        self.init_mongodb()

    def init_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            # Get MongoDB URI from environment or use localhost
            mongodb_uri = st.secrets["MONGODB_URI"]
            
            # Create MongoDB client with timeout
            client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
            
            # Test connection
            client.admin.command('ping')
            
            # Connect to database
            self.db = client['agenticai_chatbot']
            self.users_collection = self.db['users']
            
            # Create indexes for better performance
            self.users_collection.create_index("email", unique=True)
            
            # Store client for later use
            self.client = client
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            st.error(f"❌ MongoDB Connection Error: {e}")
            st.info("💡 Make sure MongoDB is running. For local development:\n"
                   "```\nmongod\n```\n"
                   "Or set MONGODB_URI environment variable for remote MongoDB.")
            raise

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt(rounds=10)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def register_user(self, email: str, full_name: str, password: str = None, auth_method: str = "email"):
        """Register a new user"""
        if self.db is None:
            return False, "Database not initialized"
        
        # Check if user already exists
        existing_user = self.users_collection.find_one({"email": email})
        if existing_user:
            return False, "User already exists"

        user_data = {
            "email": email,
            "full_name": full_name,
            "password": self.hash_password(password) if password else None,
            "auth_method": auth_method,  # "email"
            "api_calls": 0,
            "login_count": 1,
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat()
        }

        try:
            result = self.users_collection.insert_one(user_data)
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Registration error: {str(e)}"

    def login_with_email(self, email: str, password: str) -> tuple:
        """Login user with email and password"""
        if self.db is None:
            return False, None, "Database not initialized"
        
        user = self.users_collection.find_one({"email": email})
        
        if not user:
            return False, None, "User not found"
        
        if not user.get("password"):
            return False, None, "Invalid credentials"
        
        if not self.verify_password(password, user["password"]):
            return False, None, "Incorrect password"
        
        # Update last login
        self.users_collection.update_one(
            {"email": email},
            {
                "$set": {
                    "last_login": datetime.now().isoformat(),
                    "login_count": user.get("login_count", 0) + 1
                }
            }
        )
        
        return True, user, "Login successful"

    def increment_api_call(self, email: str) -> int:
        """Increment API call count for user"""
        if self.db is None:
            return 0
        
        user = self.users_collection.find_one({"email": email})
        if user:
            new_count = user.get("api_calls", 0) + 1
            self.users_collection.update_one(
                {"email": email},
                {"$set": {"api_calls": new_count}}
            )
            return new_count
        return 0

    def get_api_call_count(self, email: str) -> int:
        """Get current API call count for user"""
        if self.db is None:
            return 0
        
        user = self.users_collection.find_one({"email": email})
        return user.get("api_calls", 0) if user else 0

    def check_quota_limit(self, email: str, limit: int = 20) -> bool:
        """Check if user has exceeded quota limit"""
        call_count = self.get_api_call_count(email)
        return call_count >= limit

    def reset_daily_quota(self):
        """Reset daily quota for all users (can be called by a cron job)"""
        if self.db is None:
            return False
        
        try:
            self.users_collection.update_many(
                {},
                {"$set": {"api_calls": 0}}
            )
            return True
        except Exception as e:
            print(f"Error resetting quota: {e}")
            return False

    def is_authenticated(self) -> bool:
        """Check if user is authenticated in session"""
        return "user_email" in st.session_state and st.session_state["user_email"] is not None

    def login_user(self, email: str, full_name: str):
        """Login user and store in session"""
        if self.db is None:
            return False
        
        user = self.users_collection.find_one({"email": email})
        if user:
            st.session_state["user_email"] = email
            st.session_state["user_name"] = full_name
            st.session_state["user_data"] = user
            return True
        return False

    def logout_user(self):
        """Logout user"""
        st.session_state.clear()

    def get_current_user(self) -> dict:
        """Get current logged-in user"""
        if "user_email" in st.session_state:
            return {
                "email": st.session_state["user_email"],
                "name": st.session_state["user_name"],
                "data": st.session_state.get("user_data", {})
            }
        return None

    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
