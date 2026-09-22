"""
Language Barrier Lead Alert System - Streamlit Version
Detects language mismatch and routes leads to appropriate BD teams
"""

import streamlit as st
import pandas as pd
import re
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="Language Barrier Alert System",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language configuration
LANGUAGE_CONFIG = {
    "hi": {"name": "Hindi", "region": "North India", "bd_team": "Hindi BD Team", "bd_email": "bd-hindi@company.com", "bd_phone": "+919876543210"},
    "ta": {"name": "Tamil", "region": "Tamil Nadu", "bd_team": "Tamil BD Team", "bd_email": "bd-tamil@company.com", "bd_phone": "+919876543211"},
    "te": {"name": "Telugu", "region": "Andhra Pradesh/Telangana", "bd_team": "Telugu BD Team", "bd_email": "bd-telugu@company.com", "bd_phone": "+919876543212"},
    "bn": {"name": "Bengali", "region": "West Bengal", "bd_team": "Bengali BD Team", "bd_email": "bd-bengali@company.com", "bd_phone": "+919876543213"},
    "mr": {"name": "Marathi", "region": "Maharashtra", "bd_team": "Marathi BD Team", "bd_email": "bd-marathi@company.com", "bd_phone": "+919876543214"},
    "kn": {"name": "Kannada", "region": "Karnataka", "bd_team": "Kannada BD Team", "bd_email": "bd-kannada@company.com", "bd_phone": "+919876543215"},
    "ml": {"name": "Malayalam", "region": "Kerala", "bd_team": "Malayalam BD Team", "bd_email": "bd-malayalam@company.com", "bd_phone": "+919876543216"},
    "pa": {"name": "Punjabi", "region": "Punjab", "bd_team": "Punjabi BD Team", "bd_email": "bd-punjabi@company.com", "bd_phone": "+919876543217"},
    "gu": {"name": "Gujarati", "region": "Gujarat", "bd_team": "Gujarati BD Team", "bd_email": "bd-gujarati@company.com", "bd_phone": "+919876543218"},
    "en": {"name": "English", "region": "International", "bd_team": "English BD Team", "bd_email": "bd-english@company.com", "bd_phone": "+919876543219"},
}

# Language detection patterns
LANGUAGE_PATTERNS = {
    "hi": ["ह", "ा", "ि", "ी", "ो", "े", "क", "म", "न", "स", "हाय", "नमस्ते", "मदद", "कृपया"],
    "ta": ["த", "மி", "ழ்", "்", "ா", "வ", "ர", "ல", "ஹலோ", "வணக்கம்", "உதவி"],
    "te": ["త", "ె", "లు", "ా", "ి", "్", "హలో", "నమస్కారం", "సహాయం"],
    "bn": ["ব", "া", "ি", "ী", "ো", "এ", "হ্যালো", "নমস্কার", "সাহায্য"],
    "mr": ["म", "र", "ा", "ि", "ी", "नमस्कार", "मदत", "कृपया", "halo"],
    "kn": ["ಕ", "ನ", "್", "ಾ", "ಿ", "ಹಲೋ", "ನಮಸ್ಕಾರ", "ಸಹಾಯ"],
    "ml": ["മ", "ല", "ാ", "ി", "ീ", "ഹലോ", "നമസ്കാരം", "സഹായം"],
    "pa": ["ਪ", "ੰ", "ਜ", "ਾ", "ਬ", "ੀ", "ਹੈਲੋ", "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ"],
    "gu": ["ગ", "ુ", "જ", "ર", "ા", "ત", "ી", "હેલો", "નમસ્તે"],
    "en": ["hello", "hi", "help", "please", "thank", "service", "name"],
}

def detect_language(text):
    """Detect language from text using character patterns"""
    if not text or len(text.strip()) == 0:
        return None, 0
    
    text_lower = text.lower()
    scores = {}
    
    for lang, patterns in LANGUAGE_PATTERNS.items():
        score = 0
        for pattern in patterns:
            if pattern in text_lower or pattern in text:
                score += 1
        if score > 0:
            scores[lang] = score
    
    if not scores:
        return "en", 0.5  # Default to English
    
    # Get best match
    best_lang = max(scores, key=scores.get)
    confidence = min(scores[best_lang] / 5.0, 1.0)
    
    return best_lang, confidence

def check_language_mismatch(text, expected_language="en"):
    """Check if there's a language mismatch"""
    detected_lang, confidence = detect_language(text)
    
    result = {
        "detected_language": detected_lang,
        "language_name": LANGUAGE_CONFIG.get(detected_lang, {}).get("name", "Unknown"),
        "confidence": confidence,
        "expected_language": expected_language,
        "is_mismatch": detected_lang != expected_language,
        "bd_team": LANGUAGE_CONFIG.get(detected_lang, {}).get("bd_team", "General BD Team"),
        "bd_email": LANGUAGE_CONFIG.get(detected_lang, {}).get("bd_email", "bd-general@company.com"),
        "bd_phone": LANGUAGE_CONFIG.get(detected_lang, {}).get("bd_phone", "+910000000000"),
        "region": LANGUAGE_CONFIG.get(detected_lang, {}).get("region", "Unknown"),
        "requires_attention": detected_lang != expected_language and confidence > 0.3,
    }
    
    return result

# Sample data for demonstration
SAMPLE_ALERTS = [
    {
        "id": "ALT-20240922101530",
        "name": "Rahul Kumar",
        "email": "rahul.kumar@gmail.com",
        "phone": "+919876543210",
        "message": "हाय, मुझे आपकी सेवाओं के बारे में जानना है। कृपया मुझे कॉल करें।",
        "full_message": "हाय, मुझे आपकी सेवाओं के बारे में जानना है। कृपया मुझे कॉल करें।",
        "language": "Hindi",
        "confidence": 0.92,
        "bd_team": "Hindi BD Team",
        "status": "new",
        "created_at": "2024-09-22 10:15:30",
        "requires_action": True
    },
    {
        "id": "ALT-20240922103045",
        "name": "Priya Sharma",
        "email": "priya.s@email.com",
        "phone": "+919876543211",
        "message": "வணக்கம், உங்கள் சேவைகள் பற்றி தெரிந்து கொள்ள விரும்புகிறேன்",
        "full_message": "வணக்கம், உங்கள் சேவைகள் பற்றி தெரிந்து கொள்ள விரும்புகிறேன்",
        "language": "Tamil",
        "confidence": 0.88,
        "bd_team": "Tamil BD Team",
        "status": "acknowledged",
        "created_at": "2024-09-22 10:30:45",
        "requires_action": True
    },
    {
        "id": "ALT-20240922104520",
        "name": "Venkat Reddy",
        "email": "venkat.r@outlook.com",
        "phone": "+919876543212",
        "message": "హలో, మీ సేవల గురించి తెలుసుకోవాలని అనుకుంటున్నాను",
        "full_message": "హలో, మీ సేవల గురించి తెలుసుకోవాలని అనుకుంటున్నాను",
        "language": "Telugu",
        "confidence": 0.85,
        "bd_team": "Telugu BD Team",
        "status": "in_progress",
        "created_at": "2024-09-22 10:45:20",
        "requires_action": True
    },
    {
        "id": "ALT-20240922110015",
        "name": "Amit Das",
        "email": "amit.das@gmail.com",
        "phone": "+919876543213",
        "message": "হ্যালো, আমি আপনার পরিষেবা সম্পর্কে জানতে চাই",
        "full_message": "হ্যালো, আমি আপনার পরিষেবা সম্পর্কে জানতে চাই",
        "language": "Bengali",
        "confidence": 0.90,
        "bd_team": "Bengali BD Team",
        "status": "new",
        "created_at": "2024-09-22 11:00:15",
        "requires_action": True
    },
    {
        "id": "ALT-20240922111500",
        "name": "Suresh Patil",
        "email": "suresh.p@yahoo.com",
        "phone": "+919876543214",
        "message": "Hello, I would like to know more about your services and pricing",
        "full_message": "Hello, I would like to know more about your services and pricing",
        "language": "English",
        "confidence": 0.95,
        "bd_team": "English BD Team",
        "status": "resolved",
        "created_at": "2024-09-22 11:15:00",
        "requires_action": False
    },
    {
        "id": "ALT-20240922113030",
        "name": "Meera Nair",
        "email": "meera.n@gmail.com",
        "phone": "+919876543216",
        "message": "ഹലോ, നിങ്ങളുടെ സേവനങ്ങളെക്കുറിച്ച് കൂടുതൽ അറിയാൻ ആഗ്രഹിക്കുന്നു",
        "full_message": "ഹലോ, നിങ്ങളുടെ സേവനങ്ങളെക്കുറിച്ച് കൂടുതൽ അറിയാൻ ആഗ്രഹിക്കുന്നു",
        "language": "Malayalam",
        "confidence": 0.87,
        "bd_team": "Malayalam BD Team",
        "status": "new",
        "created_at": "2024-09-22 11:30:30",
        "requires_action": True
    },
]

# Initialize session state for alerts with sample data
if "alerts" not in st.session_state:
    st.session_state.alerts = SAMPLE_ALERTS.copy()

# Title
st.title("🌐 Language Barrier Lead Alert System")
st.markdown("Detect language mismatch and route leads to appropriate BD teams")

# Sidebar
st.sidebar.header("📋 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🔍 Detect Language", "📊 Dashboard", "📞 BD Teams", "⚙️ Settings"])

# Home Page
if page == "🏠 Home":
    st.header("Welcome!")
    st.markdown("""
    ### What does this app do?
    
    This system helps you:
    - 🔍 **Detect languages** in lead messages (Hindi, Tamil, Telugu, and more)
    - 📧 **Route leads** to the right Business Development team
    - ⚠️ **Alert teams** when there's a language mismatch
    - 📊 **Track alerts** in a dashboard
    
    ### Supported Languages
    """)
    
    # Display supported languages in columns
    cols = st.columns(5)
    for i, (code, config) in enumerate(LANGUAGE_CONFIG.items()):
        with cols[i % 5]:
            st.metric(config["name"], config["region"])

# Detect Language Page
elif page == "🔍 Detect Language":
    st.header("Language Detection & Alert Creation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Lead Information")
        
        name = st.text_input("Lead Name", placeholder="Enter lead name")
        email = st.text_input("Email", placeholder="lead@example.com")
        phone = st.text_input("Phone", placeholder="+91XXXXXXXXXX")
        message = st.text_area("Message", placeholder="Enter the lead's message here...", height=150)
        
        expected_lang = st.selectbox(
            "Expected Language",
            options=list(LANGUAGE_CONFIG.keys()),
            format_func=lambda x: LANGUAGE_CONFIG[x]["name"]
        )
        
        send_alert = st.checkbox("Send alert to BD team", value=True)
        
        if st.button("🔍 Detect Language & Create Alert", type="primary"):
            if not message:
                st.error("Please enter a message to analyze")
            else:
                with st.spinner("Analyzing language..."):
                    result = check_language_mismatch(message, expected_lang)
                    
                    # Display results
                    st.subheader("Detection Results")
                    
                    res_col1, res_col2, res_col3 = st.columns(3)
                    
                    with res_col1:
                        st.metric("Detected Language", result["language_name"])
                    with res_col2:
                        st.metric("Confidence", f"{result['confidence']*100:.0f}%")
                    with res_col3:
                        status = "⚠️ Mismatch!" if result["is_mismatch"] else "✅ Match"
                        st.metric("Status", status)
                    
                    if result["requires_attention"]:
                        st.warning(f"⚠️ **Action Required:** Route to **{result['bd_team']}**")
                    else:
                        st.success("✅ No action required - language matches expected")
                    
                    # BD Team info
                    st.subheader("Routing Information")
                    
                    route_col1, route_col2 = st.columns(2)
                    with route_col1:
                        st.info(f"""
                        **Team:** {result['bd_team']}
                        
                        **Email:** {result['bd_email']}
                        
                        **Phone:** {result['bd_phone']}
                        
                        **Region:** {result['region']}
                        """)
                    
                    # Create alert
                    alert = {
                        "id": f"ALT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "name": name or "Unknown",
                        "email": email or "Not provided",
                        "phone": phone or "Not provided",
                        "message": message[:100] + "..." if len(message) > 100 else message,
                        "full_message": message,
                        "language": result["language_name"],
                        "confidence": result["confidence"],
                        "bd_team": result["bd_team"],
                        "status": "new",
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "requires_action": result["requires_attention"]
                    }
                    
                    st.session_state.alerts.append(alert)
                    
                    if send_alert and result["requires_attention"]:
                        st.success(f"📧 Alert sent to {result['bd_team']} at {result['bd_email']}")
    
    with col2:
        st.subheader("Quick Detection")
        quick_text = st.text_area("Text to analyze (no alert)", height=200)
        
        if st.button("Quick Detect"):
            if quick_text:
                lang, conf = detect_language(quick_text)
                lang_name = LANGUAGE_CONFIG.get(lang, {}).get("name", "Unknown")
                st.metric("Language", lang_name)
                st.metric("Confidence", f"{conf*100:.0f}%")

# Dashboard Page
elif page == "📊 Dashboard":
    st.header("Alert Dashboard")
    
    # Stats
    total_alerts = len(st.session_state.alerts)
    pending = len([a for a in st.session_state.alerts if a["status"] == "new"])
    action_required = len([a for a in st.session_state.alerts if a["requires_action"]])
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Total Alerts", total_alerts)
    with stat_col2:
        st.metric("Pending", pending)
    with stat_col3:
        st.metric("Action Required", action_required)
    with stat_col4:
        st.metric("Resolved", total_alerts - pending)
    
    # Alerts table
    st.subheader("Recent Alerts")
    
    if st.session_state.alerts:
        df = pd.DataFrame(st.session_state.alerts)
        
        # Display alerts
        for alert in reversed(st.session_state.alerts[-10:]):  # Show last 10
            with st.expander(f"🔔 {alert['id']} - {alert['name']} ({alert['created_at']})"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"**Language:** {alert['language']}")
                    st.markdown(f"**Confidence:** {alert['confidence']*100:.0f}%")
                    st.markdown(f"**Team:** {alert['bd_team']}")
                
                with col_b:
                    st.markdown(f"**Email:** {alert['email']}")
                    st.markdown(f"**Phone:** {alert['phone']}")
                    st.markdown(f"**Message:** {alert['message']}")
                
                status = st.selectbox(
                    "Status",
                    ["new", "acknowledged", "in_progress", "resolved", "dismissed"],
                    key=f"status_{alert['id']}",
                    index=["new", "acknowledged", "in_progress", "resolved", "dismissed"].index(alert["status"])
                )
                
                if st.button(f"Update Status", key=f"btn_{alert['id']}"):
                    alert["status"] = status
                    st.success(f"Status updated to {status}")
    else:
        st.info("No alerts yet. Go to 'Detect Language' to create alerts.")
    
    # Clear all alerts
    if st.button("🗑️ Clear All Alerts"):
        st.session_state.alerts = []
        st.success("All alerts cleared")

# BD Teams Page
elif page == "📞 BD Teams":
    st.header("Business Development Teams")
    
    for lang_code, config in LANGUAGE_CONFIG.items():
        with st.expander(f"🇮🇳 {config['name']} - {config['region']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Team:** {config['bd_team']}")
                st.markdown(f"**Region:** {config['region']}")
            
            with col2:
                st.markdown(f"**Email:** {config['bd_email']}")
                st.markdown(f"**Phone:** {config['bd_phone']}")

# Settings Page
elif page == "⚙️ Settings":
    st.header("Settings")
    
    st.subheader("Alert Threshold")
    threshold = st.slider("Language Confidence Threshold", 0.0, 1.0, 0.3, 0.05)
    st.info(f"Alerts will be triggered when confidence is above {threshold*100:.0f}%")
    
    st.subheader("Environment Variables")
    st.code("""
# Superleap CRM Integration
SUPERLEAP_API_KEY=your-api-key
SUPERLEAP_API_URL=https://app.superleap.com/api/v1/org

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# WhatsApp Business API
WHATSAPP_PHONE_NUMBER_ID=your-phone-id
WHATSAPP_ACCESS_TOKEN=your-access-token
    """, language="bash")
    
    st.subheader("API Endpoints")
    st.markdown("""
    - `POST /api/detect` - Detect language and create alert
    - `GET /api/alerts` - Get all alerts
    - `GET /api/languages` - Get supported languages
    - `GET /api/teams` - Get BD teams
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ for seamless multilingual lead management | Language Barrier Alert System v2.0")
