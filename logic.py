import streamlit as st
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_fixed
import json
import logging
import urllib.parse  # <--- הוספתי את השורה הזאת שהייתה חסרה!
from config import AIModels, SYSTEM_PROMPT

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)

def configure_genai(api_key: str):
    """מגדיר את מפתח ה-API."""
    genai.configure(api_key=api_key)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def generate_content_with_retry(model, prompt):
    """פונקציית עזר עם מנגנון ניסיון חוזר במקרה של כשל רשת."""
    return model.generate_content(prompt)

@st.cache_data(ttl=3600, show_spinner=False)
def generate_perfect_content(api_key: str, params: dict) -> dict:
    """
    מייצר את התוכן באמצעות Gemini.
    משתמש ב-Cache כדי לחסוך קריאות זהות.
    """
    try:
        configure_genai(api_key)
        
        # הגדרת המודל עם פלט JSON מובנה
        # שימוש ב-AIModels.GEMINI_PRO שואב את השם שהגדרנו ב-config.py
        model = genai.GenerativeModel(
            AIModels.GEMINI_PRO,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # בניית הפרומפט
        formatted_prompt = SYSTEM_PROMPT.format(**params)
        
        # שליחה וקבלת תשובה
        response = generate_content_with_retry(model, formatted_prompt)
        
        # פענוח JSON
        return json.loads(response.text)

    except Exception as e:
        logging.error(f"AI Generation Error: {e}")
        # במקרה של שגיאה, נחזיר None והממשק יציג הודעה
        return None

def generate_image_url(prompt: str) -> str:
    """מייצר קישור לתמונה באמצעות Flux-Realism (Pollinations)."""
    # עכשיו השורה הזו תעבוד כי urllib.parse יובא בהצלחה
    safe_prompt = urllib.parse.quote(f"cinematic shot, 8k, {prompt}")
    return f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=768&model=flux-realism&nologo=true"
