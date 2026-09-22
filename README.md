# Language Barrier Alert System - Streamlit

> Detect language mismatch and route leads to the appropriate Business Development team

## 🚀 Features

- **Language Detection**: Automatically detects Hindi, Tamil, Telugu, Bengali, Marathi, Kannada, Malayalam, Punjabi, Gujarati, and English
- **Smart Routing**: Routes leads to the appropriate BD team based on detected language
- **Alert Dashboard**: Real-time dashboard to track all alerts
- **Status Management**: Update alert status as they're processed

## 📦 Project Structure

```
language-barrier-alert-streamlit/
├── app.py              # Main Streamlit application
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## 🏃 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## ☁️ Deploy to Streamlit Cloud (Free)

### Step 1: Create GitHub Repository

Push this code to GitHub repository.

### Step 2: Deploy on Streamlit

1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `language-barrier-alert-streamlit`
5. Branch: `main`
6. Main file path: `app.py`
7. Click "Deploy"

## 🌐 Supported Languages

| Language | Region | BD Team |
|----------|--------|---------|
| Hindi | North India | Hindi BD Team |
| Tamil | Tamil Nadu | Tamil BD Team |
| Telugu | Andhra Pradesh/Telangana | Telugu BD Team |
| Bengali | West Bengal | Bengali BD Team |
| Marathi | Maharashtra | Marathi BD Team |
| Kannada | Karnataka | Kannada BD Team |
| Malayalam | Kerala | Malayalam BD Team |
| Punjabi | Punjab | Punjabi BD Team |
| Gujarati | Gujarat | Gujarati BD Team |
| English | International | English BD Team |

## 📝 License

MIT License
