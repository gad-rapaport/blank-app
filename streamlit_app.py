import streamlit as st
import google.generativeai as genai
import urllib.parse
import random

# --- 1. הגדרות בסיס ועיצוב ---
st.set_page_config(page_title="LoveFlow V2", page_icon="💌", layout="centered")

# עיצוב CSS מתקדם - פונטים בעברית, אנימציות וכרטיסיות
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;500;700&family=Amatic+SC:wght@700&display=swap');

    body { font-family: 'Rubik', sans-serif; background-color: #fdf2f8; }
    
    .stApp {
        background: radial-gradient(circle at top, #fce7f3, #fbcfe8, #fff1f2);
    }

    /* כותרת ראשית */
    .main-title {
        font-family: 'Amatic SC', cursive;
        font-size: 4em;
        color: #db2777;
        text-align: center;
        text-shadow: 2px 2px 0px #fbcfe8;
        margin-bottom: -10px;
    }

    /* כרטיס הקלט */
    .input-card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(219, 39, 119, 0.15);
        border: 1px solid #fce7f3;
        margin-bottom: 20px;
    }

    /* כרטיס התוצאה - סגנון פולארויד */
    .polaroid {
        background: white;
        padding: 15px 15px 40px 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transform: rotate(-1deg);
        transition: transform 0.3s;
        border-radius: 4px;
        margin-top: 20px;
        text-align: center;
    }
    .polaroid:hover { transform: rotate(0deg) scale(1.02); }
    
    .polaroid img { width: 100%; border-radius: 2px; border: 1px solid #eee; }
    
    .handwritten-text {
        font-family: 'Amatic SC', cursive;
        font-size: 1.8em;
        color: #333;
        margin-top: 15px;
        line-height: 1.2;
        direction: rtl;
    }

    /* כפתור ראשי */
    .stButton>button {
        background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
        color: white;
        border-radius: 50px;
        font-size: 22px;
        padding: 12px;
        border: none;
        width: 100%;
        box-shadow: 0 4px 15px rgba(190, 24, 93, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 6px 20px rgba(190, 24, 93, 0.5); }

</style>
""", unsafe_allow_html=True)

# --- 2. לוגיקה ופונקציות ---

def get_api_key():
    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]
    return st.sidebar.text_input("🔑 מפתח Gemini API", type="password")

def generate_full_package(api_key, recipient, occasion, tone, details, relation):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Act as a professional Israeli copywriter and emotional intelligence expert.
    
    Input Data:
    - Recipient: {recipient}
    - Relation: {relation}
    - Occasion: {occasion}
    - Tone: {tone}
    - Specific Details: {details}
    
    Your Tasks (Output strictly in the requested format):
    
    1. **The Greeting (HEBREW):** Write a message that sounds 100% HUMAN. 
       - Do NOT use archaic words like 'שזורה', 'טנא', 'רבב'.
       - Use modern Israeli Hebrew. Use slang if the tone implies it.
       - Make it feel personal, slightly imperfect, and warm.
       - Include emojis.
    
    2. **Image Prompt (ENGLISH):** A visual description for an AI image generator representing the mood. No text in image.
    
    3. **Song Recommendation:** Suggest ONE real Israeli or International song that fits the mood perfectly (Artist - Song).
    
    4. **Social Captions (HEBREW):** 3 short options for an Instagram/Facebook caption if the user shares this.
    
    RESPONSE FORMAT:
    [GREETING_START]
    ...text...
    [GREETING_END]
    [IMAGE_START]
    ...prompt...
    [IMAGE_END]
    [SONG_START]
    ...song...
    [SONG_END]
    [SOCIAL_START]
    Option 1: ...
    Option 2: ...
    Option 3: ...
    [SOCIAL_END]
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        greeting = text.split("[GREETING_START]")[1].split("[GREETING_END]")[0].strip()
        img_prompt = text.split("[IMAGE_START]")[1].split("[IMAGE_END]")[0].strip()
        song = text.split("[SONG_START]")[1].split("[SONG_END]")[0].strip()
        social = text.split("[SOCIAL_START]")[1].split("[SOCIAL_END]")[0].strip()
        
        return greeting, img_prompt, song, social
    except:
        return None, None, None, None

def get_whatsapp_link(text):
    encoded_text = urllib.parse.quote(text)
    return f"https://wa.me/?text={encoded_text}"

# --- 3. ממשק משתמש (UI) ---

st.markdown('<div class="main-title">LoveFlow</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #9d174d;">מילים שנוגעות בלב. בול בזמן.</p>', unsafe_allow_html=True)

api_key = get_api_key()

# --- טופס הקלט (Form) ---
with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        recipient = st.text_input("למי כותבים?", placeholder="שם או כינוי")
        relation = st.selectbox("מי זה בשבילך?", [
            "בן/בת זוג (נשואים)", "דייט / התחלה חדשה", 
            "חבר/ה הכי טוב/ה", "אמא/אבא", 
            "גננת / מורה (סוף שנה)", "מפקד/ת או חייל/ת",
            "קולגה לעבודה", "אקס/ית (סגירת מעגל)", "לעצמי (חיזוק)"
        ])
        
    with col2:
        occasion = st.selectbox("מה הטריגר?", [
            "יום הולדת", "יום אהבה", "סתם געגוע", 
            "בקשת סליחה (פישלתי)", "עידוד וחיזוק", 
            "יום נישואין", "פרידה / שחרור", "תודה על הכל"
        ])
        tone = st.selectbox("באיזה וייב?", [
            "אמיתי וחשוף (בלי מסיכות)", 
            "קליל, קצר וקולע", 
            "הומוריסטי ושנון", 
            "חם, עוטף ומשפחתי", 
            "רוחני / מסורתי"
        ])

    details = st.text_area("התבלין הסודי (פרטים אישיים)", 
                           placeholder="דוגמה: הבדיחה שלנו על הפיצה, איך הוא תמיד נרדם בסרטים, העזרה שלו במעבר דירה...",
                           help="ככל שתכתוב יותר ספציפי, התוצאה תהיה פחות 'רובוטית'.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    generate = st.button("✨ צור לי קסם עכשיו")

# --- תוצאה ---
if generate:
    if not api_key or not recipient:
        st.warning("חסרים פרטים! נא למלא הכל.")
    else:
        with st.spinner('בוחר את המילים הכי נכונות...'):
            greeting, img_prompt, song, social = generate_full_package(api_key, recipient, occasion, tone, details, relation)
            
            if greeting:
                # יצירת תמונה
                encoded_prompt = urllib.parse.quote(img_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&model=flux&nologo=true"
                
                # --- הצגת התוצאה המרכזית (פולארויד) ---
                col_res1, col_res2 = st.columns([2, 1])
                
                with col_res1:
                    st.markdown(f"""
                    <div class="polaroid">
                        <img src="{image_url}">
                        <div class="handwritten-text">{greeting.replace(chr(10), '<br>')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_res2:
                    st.markdown("### 🎁 החבילה המלאה")
                    
                    # המלצת שיר
                    st.info(f"🎵 **שיר לאווירה:**\n{song}")
                    
                    # כפתור וואטסאפ
                    wa_link = get_whatsapp_link(greeting)
                    st.markdown(f"""
                    <a href="{wa_link}" target="_blank">
                        <button style="background-color:#25D366; color:white; border:none; padding:10px; width:100%; border-radius:10px; font-weight:bold; cursor:pointer; margin-bottom:10px;">
                             שלח בוואטסאפ עכשיו 📱
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                    
                    # פוסטים מוכנים
                    with st.expander("📲 פוסטים מוכנים לאינסטה/פייסבוק"):
                        st.text(social)
                    
                    # אפשרות שיווקית (Affiliate Mockup)
                    st.markdown("---")
                    st.caption("💡 רעיון:")
                    st.markdown(f"לשלוח ל{recipient} גם **שובר מפנק**?")
                    st.markdown("[לחץ כאן לרכישת BuyMe >>](#)")

            else:
                st.error("משהו נתקע ביצירתיות... נסה שוב.")

# --- Footer נסתר לקידום עתידי ---
st.markdown("<br><br><div style='text-align:center; color:#aaa; font-size:0.8em;'>Powered by LoveFlow AI</div>", unsafe_allow_html=True)
