# Deployment Troubleshooting Guide

## Issue: ModuleNotFoundError: No module named 'langchain_google_genai'

### Root Cause
The `langchain_google_genai` package is not installed in the deployment environment, even though it's listed in `requirements.txt`.

### Solution

#### For Local Development
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or upgrade specific package
pip install langchain-google-genai --upgrade
```

#### For Streamlit Cloud Deployment
The issue typically resolves automatically on redeploy. Try:

1. **Force redeployment**:
   - Go to Streamlit Cloud dashboard
   - Click "Reboot app" or redeploy from Git

2. **Clear cache and reinstall**:
   ```bash
   # In your GitHub repository, commit a small change to trigger redeploy
   git commit --allow-empty -m "Trigger redeploy for dependency installation"
   git push
   ```

3. **Verify requirements.txt**:
   Ensure the file is at project root and contains:
   ```
   langchain_google_genai
   ```

#### For Docker Deployment
```dockerfile
# Rebuilds container with fresh dependencies
docker build --no-cache -t agentic-ai-chatbot .
docker run -p 8501:8501 agentic-ai-chatbot
```

#### For Railway/Heroku/Other Platforms
Most platforms automatically install `requirements.txt` on deployment. If not:
- Verify `requirements.txt` is in project root
- Check deployment logs for package installation
- Manually trigger redeploy/rebuild

---

## Prevention Tips

### In Development
- Regularly test the app: `streamlit run app.py`
- Update dependencies safely: `pip install --upgrade -r requirements.txt`
- Dev environment should match deployment environment Python version

### Before Deployment
```bash
# Create fresh virtual environment to test
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Python Version Compatibility
The error mentioned Python 3.14 with Pydantic V1 deprecation warnings. Recommended setup:
- **Python 3.10-3.12**: Fully tested and stable
- **Python 3.13+**: May have compatibility issues with older packages

### Requirements.txt Maintenance
```bash
# Generate exact versions from current environment
pip freeze > requirements.txt

# Or use more flexible version pinning:
pip-tools  # Tool for managing dependencies
```

---

## Related Issues & Solutions

### Issue: "GOOGLE_API_KEY not found in Streamlit secrets"
**Solution**: Create `.streamlit/secrets.toml` with:
```toml
GOOGLE_API_KEY = "your_gemini_api_key"
GROQ_API_KEY = "your_groq_api_key"
MONGODB_URI = "mongodb://localhost:27017"
```

### Issue: "Core Pydantic V1 functionality isn't compatible with Python 3.14"
**Solution**: Either use Python 3.12 or wait for package updates. Current workaround:
```bash
pip install pydantic==1.10.12  # Pin older Pydantic
```

### Issue: Model "gemini-3-flash-preview" not found
**Solution**: Use valid model names:
- `gemini-1.5-flash` - Fast, cost-effective
- `gemini-1.5-pro` - Advanced reasoning
- `gemini-2.0-pro` - Latest generation

Updated in `geminillm.py` to use `gemini-1.5-flash` by default.

---

## Verification Checklist

After deployment, verify:
- [ ] App loads without errors
- [ ] Login/signup works
- [ ] Groq LLM initialization succeeds
- [ ] Gemini LLM initialization succeeds
- [ ] API quota tracking works
- [ ] MongoDB connection is established

Test with:
```bash
# Local test
streamlit run app.py

# Check logs for errors
# Try demo login with any credentials + password: demo
```

---

## Support Resources

- [LangChain Google Genai Docs](https://python.langchain.com/docs/integrations/llms/google_generative_ai)
- [Streamlit Cloud Deployment](https://docs.streamlit.io/deploy/streamlit-cloud)
- [Requirements.txt Best Practices](https://pip.pypa.io/en/latest/reference/requirements-file-format/)

---

## Summary of Recent Fixes

✅ **Fixed geminillm.py**:
- Removed unused imports
- Fixed duplicate variable assignment  
- Updated model to valid `gemini-1.5-flash`
- Added professional documentation
- Improved error handling with specific messages
- Added guidance for missing API key configuration

These changes ensure:
1. Cleaner, production-grade code
2. Better error messages for debugging
3. Correct model names for Gemini API
4. Professional documentation for maintenance

