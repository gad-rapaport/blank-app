import streamlit as st
import bleach
import urllib.parse
from typing import Dict, Any

def init_session_state():
    """מאתחל את משתני ה-Session לניהול היסטוריה ומצב."""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'generated' not in st.session_state:
        st.session_state.generated = False

def sanitize_input(text: str) -> str:
    """ניקוי קלט משתמש למניעת הזרקת קוד (XSS/Injection)."""
    if not text:
        return ""
    return bleach.clean(text, strip=True)

def get_whatsapp_link(text: str) -> str:
    """יוצר קישור מהיר לוואטסאפ."""
    return f"https://wa.me/?text={urllib.parse.quote(text)}"

def save_to_history(data: Dict[str, Any]):
    """שומר את התוצאה להיסטוריית הסשן הנוכחי."""
    st.session_state.history.insert(0, data)
