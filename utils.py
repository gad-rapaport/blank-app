import streamlit as st
import bleach
import urllib.parse
import random
from typing import Dict, Any

def init_session_state():
    """אתחול משתנים: שפה, היסטוריה, ו-A/B Testing."""
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # ברירת מחדל לעברית
    if 'lang' not in st.session_state:
        st.session_state.lang = 'he'
        
    # A/B Testing: חלוקה רנדומלית של משתמשים לגרסאות UI שונות
    if 'ab_variant' not in st.session_state:
        st.session_state.ab_variant = 'A' if random.random() > 0.5 else 'B'

def sanitize_input(text: str) -> str:
    """ניקוי XSS."""
    if not text:
        return ""
    return bleach.clean(text, strip=True)

def get_whatsapp_link(text: str) -> str:
    return f"https://wa.me/?text={urllib.parse.quote(text)}"

def save_to_history(data: Dict[str, Any]):
    st.session_state.history.insert(0, data)
