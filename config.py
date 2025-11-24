import streamlit as st

PAGE_CONFIG = {
    "page_title": "LoveFlow Ultimate",
    "page_icon": "💎",
    "layout": "centered",
    "initial_sidebar_state": "expanded"
}

# שימוש ב-Enum למודלים
class AIModels:
    GEMINI_PRO = "gemini-2.5-pro-latest"
    # ניתן להוסיף כאן מודלים נוספים בעתיד

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        font-family: 'Heebo', sans-serif;
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        margin-bottom: 20px;
    }
    
    /* Button Animation */
    .stButton > button {
        background: linear-gradient(45deg, #FF9A9E 0%, #FECFEF 99%, #FECFEF 100%);
        color: #555;
        border: none;
        transition: all 0.3s ease;
        font-weight: bold;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    h1, h2, h3 { color: #5D5D5D; }
</style>
"""

# פרומפט בסיס מובנה ומותאם ל-JSON Output
SYSTEM_PROMPT = """
You are a world-class Israeli creative writer and emotional intelligence expert.
Your goal is to generate a JSON response containing a romantic greeting, an image prompt, a video idea, and hashtags.

STRICT GRAMMAR RULES:
Sender: {sender_gender}
Recipient: {recipient_gender}

CONTEXT:
Recipient Name: {recipient_name}
Relation: {relation}
Occasion: {occasion}
Tone: {tone}
Details: {details}

OUTPUT JSON FORMAT:
{{
    "greeting": "Modern Hebrew greeting...",
    "image_prompt": "English description for AI image generator...",
    "tiktok_idea": "Short script description...",
    "hashtags": "#tag1 #tag2..."
}}
"""
