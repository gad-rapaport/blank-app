import streamlit as st
import google.generativeai as genai
import urllib.parse
import time

# --- 1. הגדרות בסיס ועיצוב ---
st.set_page_config(page_title="LoveFlow Pro", page_icon="💘", layout="centered")

# CSS מתקדם: פונטים, אנימציות, כפתורים מעוצבים
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;700&family=Varela+Round&display=swap');

    body { font-family: 'Rubik', sans-serif; background-color: #fff0f5; }
    
    .stApp {
        background: linear-gradient(180deg, #fff0f5 0%, #ffe4e6 100%);
    }

    /* כותרת ראשית */
    .main-header {
        font-family: 'Varela Round', sans-serif;
        color: #be185d;
        text-align: center;
        font-size: 3.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0px;
    }
    
    .subtitle {
        text-align: center;
        color: #9d174d;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }

    /* כרטיסיות קלט */
    .glass-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 20px;
    }

    /* כרטיס התוצאה הסופי */
    .result-card {
        background-color: #fff;
        border: 1px solid #eee;
        padding: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        transform: rotate(-1deg);
        border-radius: 8px;
        margin-top: 20px;
    }
    .result-text {
        font-family: 'Rubik', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333;
        direction: rtl;
        white-space: pre-wrap;
    }

    /* כפתורי מגדר */
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
        gap: 20px;
    }

    /* כפתור ראשי */
    .stButton>button {
        background: linear-gradient(45deg, #FF512F 0%, #DD2476 100%);
        color: white;
        border-radius: 50px;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        border: none;
        box-shadow: 0 4px 15px rgba(221, 36, 118, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(221, 36, 118, 0.6);
    }
    
    /* טאבים */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. פונקציות לוגיקה ---

def get_api_key():
    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]
    return st.sidebar.text_input("🔑 מפתח Gemini API", type="password")

def generate_perfect_content(api_key, sender_g, recipient_g, recipient_name, relation, occasion, tone, details):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # בניית פרומפט שרגיש למגדר בצורה קיצונית
    prompt = f"""
    Act as a top-tier Israeli creative writer.
    
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
    1. **Greeting (Hebrew):** Write a touching, human-sounding message. Modern Hebrew. No archaic language.
    2. **Image Prompt (English):** Visual description for the vibe.
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

# --- 3. ממשק המשתמש (UI) ---

st.markdown('<div class="main-header">LoveFlow</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">המילים הנכונות. לאנשים הנכונים.</div>', unsafe_allow_html=True)

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
        # המרה למחרוזות נקיות לפרומפט
        s_gen = "Male" if "גבר" in sender_gender else "Female"
        r_gen = "Male" if "גבר" in recipient_gender else "Female"
        
        with st.spinner('מג'נרט אהבה... ❤️'):
            greeting, img_prompt, tiktok, tags = generate_perfect_content(
                api_key, s_gen, r_gen, recipient_name, relation, occasion, tone, details
            )
            
            if greeting:
                st.balloons() # אפקט חגיגי
                
                # יצירת תמונה
                encoded_prompt = urllib.parse.quote(img_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&model=flux&nologo=true"

                # --- טאבים לסידור התוכן ---
                tab1, tab2, tab3 = st.tabs(["💌 הברכה", "📱 סושיאל קיט", "🎁 הפתעה"])

                with tab1:
                    # הברכה המעוצבת
                    col_img, col_txt = st.columns([1, 1.5])
                    with col_img:
                        st.image(image_url, use_container_width=True, caption="נוצר ע\"י AI")
                    with col_txt:
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-text">{greeting}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        # כפתור וואטסאפ
                        st.markdown(f"""
                        <a href="{get_whatsapp_link(greeting)}" target="_blank" style="text-decoration:none;">
                            <div style="background-color:#25D366; color:white; padding:12px; border-radius:10px; text-align:center; font-weight:bold; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
                                שליחה בוואטסאפ 🚀
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
                        <button style="background-color:#db2777; color:white; border:none; padding:15px; width:100%; border-radius:10px; cursor:pointer;">
                            הזמן מתנה עכשיו (Zer4U) 💐
                        </button>
                    </a>
                    """, unsafe_allow_html=True)

            else:
                st.error("ה-AI התבלבל לרגע. נסה שוב!")

# --- Footer ---
st.markdown("<br><hr><center style='color:#bbb'>LoveFlow V3.0 | Created with ❤️ & Python</center>", unsafe_allow_html=True)
