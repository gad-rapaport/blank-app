import streamlit as st
import google.generativeai as genai
import urllib.parse
import time

# --- 1. הגדרות בסיס ועיצוב פרימיום ---
st.set_page_config(page_title="LoveFlow Premium", page_icon="💖", layout="centered")

# CSS מתקדם: עיצוב פרימיום, פונטים, צבעים הרמוניים
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&display=swap');

    body { font-family: 'Heebo', sans-serif; background-color: #f8f0fc; }
    
    .stApp {
        background: linear-gradient(135deg, #f8f0fc 0%, #eaddff 100%);
    }

    /* כותרת ראשית */
    .main-header {
        font-family: 'Heebo', sans-serif;
        font-weight: 700;
        color: #6a1b9a;
        text-align: center;
        font-size: 3rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        background: linear-gradient(90deg, #ab47bc, #8e24aa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        text-align: center;
        color: #7b1fa2;
        font-size: 1.1rem;
        margin-bottom: 40px;
        font-weight: 400;
    }

    /* כרטיסיות קלט - עיצוב זכוכית עדין */
    .glass-container {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 25px;
    }

    /* כרטיס התוצאה הסופי - עיצוב נקי ומודרני */
    .result-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: none;
        margin-top: 20px;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    
    .result-image {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        width: 100%;
        object-fit: cover;
    }

    .result-text {
        font-family: 'Heebo', sans-serif;
        font-size: 1.1rem;
        line-height: 1.7;
        color: #333;
        direction: rtl;
        white-space: pre-wrap;
        background: #fcf8ff;
        padding: 20px;
        border-radius: 12px;
        border-right: 4px solid #ab47bc;
    }

    /* כפתורי מגדר - עיצוב כרטיסייה */
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
        gap: 15px;
        background: rgba(255, 255, 255, 0.5);
        padding: 15px;
        border-radius: 12px;
    }
    
    .stRadio label {
        font-size: 1rem;
        color: #4a148c;
    }

    /* כפתור ראשי - גרדיאנט חלק */
    .stButton>button {
        background: linear-gradient(90deg, #8e24aa 0%, #ab47bc 100%);
        color: white;
        border-radius: 50px;
        height: 55px;
        font-size: 18px;
        font-weight: 600;
        width: 100%;
        border: none;
        box-shadow: 0 4px 20px rgba(142, 36, 170, 0.3);
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(142, 36, 170, 0.5);
    }
    
    /* עיצוב טאבים */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        background-color: rgba(255, 255, 255, 0.5);
        padding: 10px;
        border-radius: 50px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Heebo', sans-serif;
        color: #6a1b9a;
        font-weight: 500;
        border-radius: 50px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #8e24aa;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* כותרות פנימיות */
    h4 { color: #7b1fa2; font-weight: 600; margin-bottom: 15px; }
    
</style>
""", unsafe_allow_html=True)

# --- 2. פונקציות לוגיקה משודרגות ---

def get_api_key():
    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]
    return st.sidebar.text_input("🔑 מפתח Gemini API", type="password")

def generate_perfect_content(api_key, sender_g, recipient_g, recipient_name, relation, occasion, tone, details):
    genai.configure(api_key=api_key)
    # --- שינוי למודל Gemini 1.5 Pro החזק יותר ---
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    prompt = f"""
    Act as a top-tier Israeli creative writer and emotional intelligence expert.
    
    --- CRITICAL GRAMMAR RULES ---
    Sender Gender: {sender_g} (You must use grammar for {sender_g} - e.g., if Male: "אני כותב", if Female: "אני כותבת").
    Recipient Gender: {recipient_g} (You must use grammar for {recipient_g} - e.g., if Male: "אתה", if Female: "את").
    ------------------------------

    Context:
    - Recipient Name: {recipient_name}
    - Relation: {relation}
    - Occasion: {occasion}
    - Tone: {tone}
    - Personal Details: {details}
    
    Tasks:
    1. **Greeting (Hebrew):** Write a touching, human-sounding message. Modern Hebrew. No archaic language. Be creative and authentic.
    2. **Image Prompt (English):** A detailed visual description for a realistic photo that captures the mood. Focus on lighting, composition, and emotion.
    3. **TikTok/Reels Idea:** A short script/concept for a video to go with this greeting.
    4. **Hashtags:** 5 viral Hebrew hashtags for this specific event.
    
    OUTPUT FORMAT:
    [TEXT_START]
    ...greeting...
    [TEXT_END]
    [IMG_START]
    ...prompt...
    [IMG_END]
    [TIKTOK_START]
    ...script idea...
    [TIKTOK_END]
    [TAGS_START]
    ...hashtags...
    [TAGS_END]
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        greeting = text.split("[TEXT_START]")[1].split("[TEXT_END]")[0].strip()
        img_prompt = text.split("[IMG_START]")[1].split("[IMG_END]")[0].strip()
        tiktok = text.split("[TIKTOK_START]")[1].split("[TIKTOK_END]")[0].strip()
        tags = text.split("[TAGS_START]")[1].split("[TAGS_END]")[0].strip()
        
        return greeting, img_prompt, tiktok, tags
    except:
        return None, None, None, None

def get_whatsapp_link(text):
    return f"https://wa.me/?text={urllib.parse.quote(text)}"

# --- 3. ממשק המשתמש (UI) פרימיום ---

st.markdown('<div class="main-header">LoveFlow Premium</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">יצירת תוכן רומנטי, ברמה אחרת.</div>', unsafe_allow_html=True)

api_key = get_api_key()

# --- חלק 1: מי נגד מי (מגדר) ---
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
col_gender1, col_gender2 = st.columns(2)

with col_gender1:
    st.markdown("<h4 style='text-align:center;'>אני... (השולח/ת)</h4>", unsafe_allow_html=True)
    sender_gender = st.radio("מגדר שולח", ["גבר 👨", "אישה 👩"], horizontal=True, label_visibility="collapsed", key="sender")

with col_gender2:
    st.markdown("<h4 style='text-align:center;'>כותב/ת ל... (המקבל/ת)</h4>", unsafe_allow_html=True)
    recipient_gender = st.radio("מגדר מקבל", ["גבר 👨", "אישה 👩"], horizontal=True, label_visibility="collapsed", key="recipient")
st.markdown('</div>', unsafe_allow_html=True)

# --- חלק 2: הפרטים ---
with st.container():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        recipient_name = st.text_input("שם המקבל/ת", placeholder="למשל: דני / נועה")
        relation = st.selectbox("מה הקשר?", ["בן/בת זוג", "דייט", "חבר/ה טוב/ה", "משפחה (הורים/אחים)", "קולגה", "אקס/ית"])
        
    with col2:
        occasion = st.selectbox("האירוע", ["יום הולדת", "יום אהבה", "סתם צומי", "סליחה", "יום נישואין", "פרידה", "עידוד"])
        tone = st.selectbox("הסגנון", ["מרגש ורומנטי", "קליל ומצחיק", "עמוק ופילוסופי", "חרוזים קלילים", "ישראלי סחבק"])

    details = st.text_area("פרטים אישיים (הקסם קורה כאן)", placeholder="הוא אוהב סושי, היא תמיד מאחרת, הבדיחה על הכלב...")
    st.markdown('</div>', unsafe_allow_html=True)

    generate_btn = st.button("✨ צור את הברכה המושלמת")

# --- חלק 3: התוצאה ---
if generate_btn:
    if not api_key or not recipient_name:
        st.warning("חסרים פרטים! מלא את השם ואת המפתח.")
    else:
        s_gen = "Male" if "גבר" in sender_gender else "Female"
        r_gen = "Male" if "גבר" in recipient_gender else "Female"
        
        with st.spinner("מג'נרט אהבה עם המנועים החדשים... 💖"):
            greeting, img_prompt, tiktok, tags = generate_perfect_content(
                api_key, s_gen, r_gen, recipient_name, relation, occasion, tone, details
            )
            
            if greeting:
                st.balloons()
                
                # --- יצירת תמונה - ניסיון לריאליזם ---
                encoded_prompt = urllib.parse.quote(f"realistic photo, high quality, {img_prompt}")
                # שימוש במודל flux-realism
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&model=flux-realism&nologo=true"

                # --- טאבים לסידור התוכן ---
                tab1, tab2, tab3 = st.tabs(["💌 הברכה", "📱 סושיאל קיט", "🎁 הפתעה"])

                with tab1:
                    # הברכה המעוצבת מחדש
                    st.markdown(f"""
                    <div class="result-card">
                        <img src="{image_url}" class="result-image" alt="AI generated image">
                        <div class="result-text">{greeting}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    # כפתור וואטסאפ משודרג
                    st.markdown(f"""
                    <a href="{get_whatsapp_link(greeting)}" target="_blank" style="text-decoration:none;">
                        <div style="background: linear-gradient(45deg, #25D366, #128C7E); color:white; padding:15px; border-radius:50px; text-align:center; font-weight:600; box-shadow:0 4px 15px rgba(37, 211, 102, 0.3); transition: 0.3s;">
                            שליחה מהירה בוואטסאפ 🚀
                        </div>
                    </a>
                    """, unsafe_allow_html=True)

                with tab2:
                    st.success("✨ הערכה למשפיענ/ית:")
                    st.markdown("#### 🎥 רעיון לטיקטוק/רילס")
                    st.info(tiktok)
                    
                    st.markdown("#### #️⃣ האשטאגים להעתקה")
                    st.code(tags, language="text")
                    
                    st.markdown("#### 🔗 קיצורי דרך")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.link_button("פתח טיקטוק", "https://www.tiktok.com/")
                    with c2:
                        st.link_button("פתח אינסטגרם", "https://www.instagram.com/")
                    with c3:
                        st.link_button("פתח טוויטר/X", "https://twitter.com/")

                with tab3:
                    st.markdown("### רוצה להוסיף מתנה אמיתית? 🎁")
                    st.markdown(f"הברכה הזו תלך מושלם עם זר פרחים או שוקולד.")
                    st.markdown("""
                    <a href="https://zer4u.co.il" target="_blank">
                        <button style="background: linear-gradient(90deg, #db2777, #e91e63); color:white; border:none; padding:15px; width:100%; border-radius:12px; cursor:pointer; font-weight:600; font-size:16px;">
                            הזמן מתנה עכשיו (Zer4U) 💐
                        </button>
                    </a>
                    """, unsafe_allow_html=True)

            else:
                st.error("ה-AI נתקל בבעיה. נסה שוב!")

# --- Footer ---
st.markdown("<br><hr><center style='color:#9e9e9e; font-size:0.9rem;'>LoveFlow Premium | Created with 💖 & Python</center>", unsafe_allow_html=True)
