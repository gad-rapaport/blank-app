import streamlit as st
import google.generativeai as genai
import time

# --- הגדרת העמוד ---
st.set_page_config(page_title="PostFlow AI", page_icon="🚀", layout="wide")

# --- עיצוב CSS (כדי שיראה יוקרתי וכהה) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    .stTextArea textarea {
        background-color: #1E1E1E;
        color: white;
    }
    .stButton>button {
        background-color: #7C3AED;
        color: white;
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #6D28D9;
    }
</style>
""", unsafe_allow_html=True)

# --- כותרת ---
st.title("🚀 PostFlow")
st.caption("הפוך מחשבות גולמיות לפוסטים ויראליים בשניות")

# --- סרגל צד להגדרות ---
with st.sidebar:
    st.header("⚙️ הגדרות")
    api_key = st.text_input("הכנס מפתח Gemini API", type="password")
    st.info("המפתח נשמר זמנית רק לצורך הפעלה זו.")

# --- מסך ראשי מחולק ל-2 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💡 הרעיון שלך")
    platform = st.selectbox("לאיזו פלטפורמה?", ["LinkedIn", "Twitter/X Thread", "Instagram Caption", "Facebook"])
    tone = st.selectbox("איזה סגנון?", ["מקצועי ורציני", "ויראלי וקצבי", "מצחיק ושנון", "סיפורי ורגשי"])
    raw_idea = st.text_area("שפוך כאן את המחשבות שלך...", height=200)
    
    generate_btn = st.button("צור קסם ✨")

with col2:
    st.subheader("📝 התוצאה")
    result_container = st.empty()
    
    if generate_btn:
        if not api_key:
            st.error("חסר מפתח API! נא להכניס אותו בצד ימין.")
        elif not raw_idea:
            st.warning("לא כתבת שום רעיון...")
        else:
            # כאן מתבצע הקסם האמיתי
            try:
                with st.spinner('ה-AI כותב עבורך...'):
                    # חיבור לגוגל
                    genai.configure(api_key=api_key)
                    
                    # בחירת המודל (ביקשת את הפרו)
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    
                    # בניית הבקשה (הפרומפט)
                    prompt = f"""
                    You are an expert social media ghostwriter.
                    Platform: {platform}
                    Tone: {tone}
                    
                    User's raw thought:
                    "{raw_idea}"
                    
                    Task: Rewrite this into a perfect, engaging post in Hebrew (or the language of the input).
                    Add emojis, line breaks, and hashtags.
                    """
                    
                    # שליחה
                    response = model.generate_content(prompt)
                    
                    # הצגת התוצאה
                    result_container.success("הפוסט מוכן!")
                    st.text_area("העתק מכאן:", value=response.text, height=400)
                    
            except Exception as e:
                st.error(f"שגיאה: {str(e)}")

