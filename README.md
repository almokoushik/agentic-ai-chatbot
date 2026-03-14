# Agentic AI Chatbot

A production-ready, multi-tenant AI chatbot framework built with **LangGraph**, **Multiple-LLM Support** (Groq & Google Gemini, and more), and **Streamlit**. Demonstrates enterprise-grade implementations including user authentication with bcrypt security, MongoDB persistence, API quota management, and agentic workflow orchestration for intelligent conversational AI.

---

##  Key Features

### Core Capabilities
- **Dual-LLM Architecture**: Support for Groq (low-latency inference) and Google Gemini with fallback mechanisms
- **Agentic Reasoning**: LangGraph-powered multi-step reasoning with stateful conversation management
- **Multi-Tenant Architecture**: Role-based access control with per-user API quota enforcement (20 calls/user)

### Authentication & Security
- **Secure Authentication**: Email/password authentication with bcrypt password hashing (10-round salt)
- **MongoDB Integration**: Persistent user data storage with atomic operations and unique email indexing
- **Session Management**: Streamlit-based session state with automatic logout and token invalidation
- **API Rate Limiting**: Real-time quota tracking with color-coded usage indicators (green/yellow/red)

### User Experience
- **Interactive Web UI**: Streamlit-based responsive interface with sidebar user management
- **Real-Time Quota Display**: Dynamic API call counter with automatic refresh and persistent MongoDB updates
- **Error Handling**: Comprehensive error handling with user-friendly feedback and graceful degradation
- **Modular Architecture**: Extensible node and graph structure for custom workflow implementation

### Technical Stack
- **LLM Framework**: LangGraph for orchestrating multi-step agentic workflows
- **Language Models**: Groq API (fast inference), Google Gemini (advanced reasoning)
- **Database**: MongoDB with PyMongo for non-relational persistence
- **Security**: bcrypt for password hashing, environment variable-based API key management
- **Deployment**: Streamlit for rapid UI development and cloud deployment

---

##  Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment (venv/conda)
- MongoDB instance (local or MongoDB Atlas)
- API keys:
  - Groq
  - Gemini

### Installation

1. **Clone repository**:
   ```bash
   git clone https://github.com/almokoushik/agentic-ai-chatbot.git
   cd agentic-ai-chatbot
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   Create `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your_groq_key_here"
   GOOGLE_API_KEY = "your_gemini_key_here"
   MONGODB_URI = "mongodb://localhost:27017"
   ```

5. **Start MongoDB** (if local):
   ```bash
   mongod
   ```

6. **Run application**:
   ```bash
   streamlit run app.py
   ```

Access at: `http://localhost:8501`

---

##  Project Structure

```
agentic-ai-chatbot/
├── src/langgraphagenticai/
│   ├── authentication/
│   │   ├── auth_manager.py       # MongoDB-backed auth + quota management
│   │   └── google_auth.py        # User login/signup UI with email & password
│   ├── graph/
│   │   └── graph_builder.py      # LangGraph workflow orchestration
│   ├── LLMS/
│   │   ├── groqllm.py           # Groq model integration
│   │   └── geminillm.py         # Google Gemini model integration
│   ├── nodes/
│   │   └── basic_chatbot_node.py # Conversation processing node
│   ├── state/
│   │   └── state.py             # Conversation state schema
│   └── ui/
│       └── streamlitui/
│           ├── loadui.py         # UI component rendering
│           └── display_result.py # Response display + quota tracking
├── app.py                        # Application entry point
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation
```

---

##  Authentication Flow

```
User Entry
    ↓
[Email/Password Login] → [Sign Up New Account]
    ↓                          ↓
    └─────→ MongoDB Lookup ←───┘
            ├─ bcrypt verification
            └─ Create session state
                ↓
         Main Application Access
                ↓
    [User Sidebar] → API Quota Display
```

---

##  API Quota System

**Per-User Limits**:
- 20 API calls per user session
- Real-time counter updates via MongoDB
- Visual indicators:
  - 🟢 **Green** (0-9 calls): Active quota available
  - 🟡 **Yellow** (10-19 calls): Quota warning threshold
  - 🔴 **Red** (20+ calls): Quota exceeded, access blocked



---

##  LLM Selection & Configuration

### Groq Models Available
- `llama-3.1-8b-instant` - Fast, lightweight reasoning
- `llama-3.3-70b-versatile` - Advanced multi-task performance
- `groq-compound-mini` - Optimized for edge inference

### Google Gemini Models Available
- `gemini-1.5-pro` - Advanced reasoning and complex tasks
- `gemini-1.5-flash` - Fast, cost-effective inference
- `gemini-2.0-pro` - Latest generation with extended context

---

##  Development

### MongoDB Operations
```bash
# Connect to local MongoDB
mongosh

# View stored users
use agenticai_chatbot
db.users.find()

# Check API call counts
db.users.find({ email: "user@example.com" }, { api_calls: 1 })
```

### Environment Variables Reference
| Variable | Purpose | Example |
|----------|---------|---------|
| `GROQ_API_KEY` | Groq API authentication | `gsk_xxxx` |
| `GOOGLE_API_KEY` | Google Gemini API key | `AIzaxxxx` |
| `MONGODB_URI` | Database connection string | `mongodb://localhost:27017` |

---

##  Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add secrets in deployment settings
4. Auto-deploy on push

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```


##  Performance Metrics

| Metric | Value |
|--------|-------|
| Auth Response Time | ~50ms (bcrypt, local MongoDB) |
| LLM Response Latency | 200-800ms (Groq), 800-2000ms (Gemini) |
| MongoDB Query Time | ~5-10ms (indexed email lookup) |
| Session State Refresh | ~100ms (Streamlit cache) |
| API Quota Increment | ~15ms (atomic MongoDB operation) |

---
