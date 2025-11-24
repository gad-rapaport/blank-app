import streamlit as st

class AppConfig:
    PAGE_TITLE = "LoveFlow Ultimate"
    PAGE_ICON = "💎"
    LAYOUT = "centered"
    
class AIConfig:
    # שימוש במודל עדכני ותקין
    MODEL_NAME = "gemini-2.5-pro" 
    RETRY_ATTEMPTS = 3

# CSS פרימיום עם אופטימיזציה למובייל (Media Queries)
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        font-family: 'Heebo', sans-serif;
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        margin-bottom: 20px;
    }

    /* Mobile Optimization */
    @media (max-width: 600px) {
        .glass-card { padding: 1rem; }
        .stButton > button { width: 100%; border-radius: 12px; }
        h1 { font-size: 1.8rem !important; }
    }
    
    /* Button Animation */
    .stButton > button {
        background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
        color: #444;
        border: none;
        font-weight: bold;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
"""

# Chain of Thought (CoT) System Prompt
SYSTEM_PROMPT = """
You are a world-class creative writer and emotional intelligence expert.
Your goal is to generate a JSON response.

PROCESS (Chain of Thought):
1. Analyze the relationship dynamic and the specific occasion.
2. Determine the appropriate emotional depth based on the requested tone.
3. Draft a greeting in {language} that feels authentic, avoiding clichés.
4. Visualize a scene that complements this text for the image prompt.

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
    "greeting": "The greeting text in {language}...",
    "image_prompt": "Detailed English description for AI image generator, focusing on lighting and mood...",
    "tiktok_idea": "A viral video concept...",
    "hashtags": "#tag1 #tag2..."
}}
"""
