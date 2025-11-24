import streamlit as st
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_fixed
import json
import logging
import urllib.parse
from config import AIConfig, SYSTEM_PROMPT

# הגדרת לוגים (לצורך מוניטורינג עתידי)
logging.basicConfig(level=logging.INFO)

def configure_genai(api_key: str):
    genai.configure(api_key=api_key)

@retry(stop=stop_after_attempt(AIConfig.RETRY_ATTEMPTS), wait=wait_fixed(2))
def generate_content_with_retry(model, prompt):
    """מנגנון שרידות: מנסה שוב אם יש כשל רשת."""
    return model.generate_content(prompt)

@st.cache_data(ttl=3600, show_spinner=False)
def generate_perfect_content(api_key: str, params: dict, language: str) -> dict:
    """יצירת תוכן עם Caching לחיסכון במשאבים."""
    try:
        configure_genai(api_key)
        
        model = genai.GenerativeModel(
            AIConfig.MODEL_NAME,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # הוספת השפה לפרומפט
        params['language'] = "Hebrew" if language == 'he' else "English"
        
        formatted_prompt = SYSTEM_PROMPT.format(**params)
        response = generate_content_with_retry(model, formatted_prompt)
        
        return json.loads(response.text)

    except Exception as e:
        logging.error(f"AI Generation Error: {e}")
        # כאן ניתן להוסיף שליחה ל-Sentry
        return None

def generate_image_url(prompt: str) -> str:
    """
    יצירת תמונה.
    הערה: כאן ניתן להוסיף לוגיקת Fallback ל-DALL-E אם רוצים.
    כרגע משתמשים ב-Pollinations כפתרון חינמי ומהיר.
    """
    safe_prompt = urllib.parse.quote(f"cinematic lighting, photorealistic, 8k, {prompt}")
    return f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=768&model=flux-realism&nologo=true"
