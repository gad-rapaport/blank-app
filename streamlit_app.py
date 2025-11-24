import streamlit as st
import google.generativeai as genai
import urllib.parse
import time

# --- 1. הגדרות בסיס ---
st.set_page_config(page_title="LoveFlow Infinity", page_icon="💎", layout="wide")

# --- 2. ניהול ערכות נושא (Themes) ---
# נשתמש ב-Session State כדי לשמור את הבחירה
if 'theme' not in st.session_state:
    st.session_state.theme = "Pastel Dreams"

themes = {
    "Pastel Dreams": {
        "bg": "linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%)",
        "primary": "#ff9a9e",
        "text": "#4a4a4a",
        "card_bg": "rgba(255, 255, 255, 0.8)"
    },
    "Red Velvet": {
        "bg": "linear-gradient(to right, #434343 0%, black 100%)",
        "primary": "#d31027",
        "text": "#ffffff",
        "card_bg": "rgba(40, 40, 40, 0.8)"
    },
    "Neon Nights": {
        "bg": "linear-gradient(to top, #09203f 0%, #537895 100%)",
        "primary": "#00d2ff",
        "text": "#e0e0e0",
        "card_bg": "rgba(16, 20, 50, 0.7)"
    }
}

current_theme = themes[st.session_state.theme]

# --- 3. CSS מתקדם ואנימציות ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&family=Dancing+Script:wght@700&display=swap');

    /* רקע דינמי לפי התמה */
    .stApp {{
        background: {current_theme['bg']};
        color: {current_theme['text']};
    }}

    /* אנימציית לבבות מרחפים ברקע */
    .heart-bg {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }}
    .heart {{
        position: absolute;
        bottom: -100px;
        width: 40px;
        height: 40px;
        background: {current_theme['primary']};
        opacity: 0.2;
        animation: fly 10s infinite linear;
        clip-path: path("M20,6.6c-5.3-6.6-14-5.3-17.6-1.3S-1.3,16,6.6,26.6C10.6,32,20,40,20,40s9.3-8,13.3-13.3c5.3-6.6,7.3-16,2.6-21.3S25.3,0,20,6.6z");
    }}
    @keyframes fly {{
        0% {{ transform: translateY(0) rotate(0deg); opacity: 0.5; }}
        100% {{ transform: translateY(-100vh) rotate(360deg); opacity: 0; }}
    }}

    /* טיפוגרפיה */
    h1 {{ font-family: 'Dancing Script', cursive; font-size: 4em !important; text-align: center; color: {current_theme['primary']}; }}
    h3, h4, h5 {{ font-family: 'Assistant', sans-serif; }}
    p, div {{ font-family: 'Assistant', sans-serif; font-size: 1.1em; }}

    /* כרטיסיות זכוכית */
    .glass {{
        background: {current_theme['card_bg']};
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }}

    /* כפתור ראשי פועם */
    .stButton>button {{
        background: {current_theme['primary']};
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 40px;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 0 20px {current_theme['primary']};
        transition: 0.3s;
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(255, 105, 180, 0.4); }}
        70% {{ box-shadow: 0 0 0 10px rgba(255, 105, 180, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(255, 105, 180, 0); }}
    }}
    .stButton>button:hover {{ transform: scale(1.05); }}

</style>

<div class="heart-bg">
    <div class="heart" style="left: 10%; animation-duration: 8s;"></div>
    <div class="heart" style="left: 30%; animation-duration: 12s; animation-delay: 2s;"></div>
    <div class="heart" style="left: 70%; animation-duration: 7s; animation-delay: 4s;"></div>
    <div class="heart" style="left: 90%; animation-duration: 9s; animation-delay: 1s;"></div>
</div>
""", unsafe_allow_html=True)

# --- 4. לוגיקה ---

def get_api_key():
    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]
    return st.sidebar.text_input("🔑 מפתח Gemini API", type="password")

def generate_infinity_content(api_key, sender_g, recipient_g, recipient_name, relation, occasion, tone, details):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    prompt = f"""
    Act as a world-class creative director.
    Sender: {sender_g}. Recipient: {recipient_g} ({recipient_name}).
    Occasion: {occasion}. Tone: {tone}. Details: {details}.
    
    Tasks:
    1. **Greeting (Hebrew):** Modern, emotional, perfect grammar.
    2. **Image Prompt (English):** Cinematic lighting, photorealistic, 8k, distinct style matching the tone.
    3. **Music:** Name a specific song (Artist - Title) that fits perfectly.
    4. **Color:** Suggest a hex color code that fits the mood.
    
    OUTPUT FORMAT:
    [TEXT]{{hebrew_greeting}}[/TEXT]
    [IMG]{{image_prompt}}[/IMG]
    [SONG]{{song_name}}[/SONG]
    """
    
    try:
        response = model.generate_content(prompt)
        t = response.text
        greeting = t.split("[TEXT]")[1].split("[/TEXT]")[0].strip()
        img_p = t.split("[IMG]")[1].split("[/IMG]")[0].strip()
        song = t.split("[SONG]")[1].split("[/SONG]")[0].strip()
        return greeting, img_p, song
    except:
        return None, None, None

# --- 5. ממשק משתמש (UI) ---

# סרגל צד לבחירת עיצוב
with st.sidebar:
    st.title("🎨 עיצוב")
    selected_theme = st.selectbox("בחר אווירה:", list(themes.keys()), index=list(themes.keys()).index(st.session_state.theme))
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()
    
    st.markdown("---")
    st.info("💡 טיפ: נסה את 'Neon Nights' לברכות מסיבה, ואת 'Red Velvet' לאהבה רומנטית.")

# כותרת ראשית
st.markdown("<h1>LoveFlow Infinity</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; opacity:0.8;'>המילים שלך, הרגש שלנו. עכשיו ב-{st.session_state.theme}</p>", unsafe_allow_html=True)

api_key = get_api_key()

# אזור הקלט - מחולק ל-2 עמודות
col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 👤 פרטים בסיסיים")
    sender_gender = st.radio("אני:", ["גבר", "אישה"], horizontal=True)
    recipient_gender = st.radio("כותב ל:", ["גבר", "אישה"], horizontal=True)
    recipient_name = st.text_input("שם המקבל/ת")
    relation = st.selectbox("קשר", ["בן/בת זוג", "דייט", "משפחה", "חבר/ה", "אקס/ית"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### ✨ הקסם")
    c1, c2 = st.columns(2)
    with c1:
        occasion = st.selectbox("אירוע", ["יום הולדת", "יום אהבה", "סליחה", "געגוע", "עידוד"])
    with c2:
        tone = st.selectbox("סגנון", ["רומנטי (דמעות)", "שנון וסקסי", "קליל וחברי", "פיוטי ועמוק"])
    
    details = st.text_area("פרטים אישיים (שפוך את הלב...)", height=100)
    generate_btn = st.button("💎 צור יצירת מופת")
    st.markdown('</div>', unsafe_allow_html=True)

# תוצאה
if generate_btn and api_key and recipient_name:
    with st.spinner("מפעיל את קסמי ה-AI... 🔮"):
        s_gen = "Male" if sender_gender == "גבר" else "Female"
        r_gen = "Male" if recipient_gender == "גבר" else "Female"
        
        greeting, img_prompt, song = generate_infinity_content(api_key, s_gen, r_gen, recipient_name, relation, occasion, tone, details)
        
        if greeting:
            # יצירת תמונה
            enc_prompt = urllib.parse.quote(f"cinematic shot, {img_prompt}")
            img_url = f"https://image.pollinations.ai/prompt/{enc_prompt}?width=1200&height=600&model=flux-realism&nologo=true"
            
            st.markdown("---")
            
            # תצוגה ראשית גדולה
            st.image(img_url, use_container_width=True)
            
            col_music, col_text = st.columns([1, 2])
            
            with col_music:
                st.markdown('<div class="glass">', unsafe_allow_html=True)
                st.markdown("### 🎧 הפסקול שלך")
                st.markdown(f"**{song}**")
                # הטמעת נגן יוטיוב (חיפוש השיר)
                st.video(f"https://www.youtube.com/embed?listType=search&list={urllib.parse.quote(song)}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_text:
                st.markdown('<div class="glass">', unsafe_allow_html=True)
                st.markdown(f"<div style='direction:rtl; white-space:pre-wrap; font-size:1.2em; line-height:1.6;'>{greeting}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # כפתור וואטסאפ ענק
                st.markdown(f"""
                <a href="https://wa.me/?text={urllib.parse.quote(greeting)}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:15px; width:100%; border-radius:10px; font-weight:bold; font-size:1.2em; cursor:pointer;">
                        שלח את זה עכשיו בוואטסאפ 💚
                    </button>
                </a>
                """, unsafe_allow_html=True)

        else:
            st.error("שגיאה ביצירה. נסה שוב.")
