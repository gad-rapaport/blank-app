import streamlit as st
import google.generativeai as genai
import urllib.parse
import time

# --- Phase 1: Configuration & Setup ---
st.set_page_config(page_title="LoveFlow | לב-לי", page_icon="❤️", layout="centered")

# --- Phase 2: Design System (Glassmorphism & RTL) ---
st.markdown("""
<style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 99%, #FECFEF 100%);
        background-attachment: fixed;
    }
    
    /* Global Text Settings */
    body, .stMarkdown, .stButton, .stTextInput, .stTextArea, .stSelectbox {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #4A0404;
    }

    /* Glassmorphism Card Style */
    .glass-card {
        background: rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 25px;
        margin-bottom: 20px;
        text-align: right;
        direction: rtl;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%); 
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(221, 36, 118, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(221, 36, 118, 0.6);
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Input Fields Styling */
    .stTextInput>div>div, .stTextArea>div>div, .stSelectbox>div>div {
        background-color: rgba(255, 255, 255, 0.6);
        border-radius: 10px;
        border: 1px solid #ffb6c1;
    }
</style>
""", unsafe_allow_html=True)

# --- Phase 3: Logic Functions ---

def get_api_key():
    """Handles API key retrieval securely."""
    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]
    return st.sidebar.text_input("🔑 הכנס מפתח Gemini API", type="password")

def generate_content(api_key, recipient, occasion, tone, details, relation):
    """Generates the text and the image prompt using Gemini."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Combined prompt for efficiency: Generate Hebrew text AND an English image prompt
    full_prompt = f"""
    You are a romantic content expert. Perform two tasks:
    
    Task 1: Write a touching, personalized greeting in HEBREW.
    Recipient: {recipient}
    Occasion: {occasion}
    Relation: {relation}
    Tone: {tone}
    Details to include: {details}
    Output requirements: Beautiful Hebrew, spacing between paragraphs, add emojis.
    
    Task 2: Write a short, artistic image generation prompt in ENGLISH that captures the mood of this greeting. 
    Style: {tone} (e.g., if funny -> cartoon style, if romantic -> watercolor or cinematic lighting).
    Do NOT include text in the image prompt.
    
    RESPONSE FORMAT:
    [HEBREW_START]
    ... the hebrew greeting here ...
    [HEBREW_END]
    [IMAGE_PROMPT_START]
    ... the english image prompt here ...
    [IMAGE_PROMPT_END]
    """
    
    try:
        response = model.generate_content(full_prompt)
        text = response.text
        
        # Parsing the response
        hebrew_text = text.split("[HEBREW_START]")[1].split("[HEBREW_END]")[0].strip()
        image_prompt = text.split("[IMAGE_PROMPT_START]")[1].split("[IMAGE_PROMPT_END]")[0].strip()
        
        return hebrew_text, image_prompt
    except Exception as e:
        return None, None

def get_pollinations_url(prompt):
    """Generates a direct URL for the image based on the prompt."""
    if not prompt:
        return "https://image.pollinations.ai/prompt/love%20heart%20flowers?width=800&height=600&nologo=true"
    
    encoded_prompt = urllib.parse.quote(prompt)
    # Adding 'nologo' to remove watermarks, setting seed for consistency if needed
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&model=flux&nologo=true"
    return url

# --- Phase 4: UI Structure ---

def main():
    st.markdown("<h1 style='text-align: center; color: #880e4f; font-weight: 800;'>❤️ LoveFlow</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #880e4f; font-size: 1.2em;'>המילים שלך, הרגש שלנו.</p>", unsafe_allow_html=True)

    api_key = get_api_key()

    # --- Input Section (Inside a Glass Card) ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        recipient = st.text_input("למי כותבים?", placeholder="למשל: נועה / בעלי היקר")
        relation = st.selectbox("מה הקשר?", ["בני זוג", "דייט ראשון", "חברות הכי טובות", "משפחה", "בקשת סליחה"])
    with col2:
        occasion = st.selectbox("מה האירוע?", ["יום אהבה / ולנטיין", "יום הולדת", "סתם כי בא לי לפרגן", "יום נישואין", "בוקר טוב רומנטי"])
        tone = st.selectbox("באיזה וייב?", ["רומנטי ומרגש (דמעות)", "קליל ומצחיק", "חרוזים קלאסי", "שנון ומקורי", "פסוקים ומסורתי"])

    details = st.text_area("פרטים שחובה להזכיר (כדי שירגיש אישי)", placeholder="למשל: הטיול שעשינו ברומא, זה שהיא מכורה לשוקולד, הכינוי שלה 'בובי'...")
    
    st.markdown('</div>', unsafe_allow_html=True)

    generate_btn = st.button("✨ צור לי כרטיס ברכה מושלם")

    # --- Output Section ---
    if generate_btn:
        if not api_key:
            st.error("⚠️ חסר מפתח API. נא להגדיר אותו בהגדרות או בסרגל הצד.")
        elif not recipient or not details:
            st.warning("⚠️ חסר מידע! נא למלא למי הברכה ופרטים אישיים.")
        else:
            with st.spinner('🎨 ה-AI מלחין מילים ומצייר עבורך...'):
                
                # 1. Generate Text & Image Prompt
                hebrew_greeting, img_prompt = generate_content(api_key, recipient, occasion, tone, details, relation)
                
                if hebrew_greeting:
                    # 2. Generate Image URL
                    image_url = get_pollinations_url(img_prompt)
                    
                    # 3. Display Result in a "Shareable Card"
                    st.markdown("---")
                    
                    # Container for the result
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <img src="{image_url}" style="width: 100%; border-radius: 15px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                        <div style="font-size: 1.1em; line-height: 1.6; white-space: pre-wrap; font-weight: 500; color: #2c0b0e;">
                            {hebrew_greeting}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # 4. Monetization / Affiliate Slot (Non-intrusive)
                    st.markdown(f"""
                    <div style="background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; text-align: center; margin-top: 10px; border: 1px dashed #FF512F;">
                        <strong>🎁 רוצה לשדרג את הברכה?</strong><br>
                        <a href="https://zer4u.co.il" target="_blank" style="text-decoration: none; color: #DD2476; font-weight: bold; font-size: 1.1em;">
                            לחץ כאן כדי לשלוח ל{recipient} פרחים אמיתיים יחד עם הברכה! 💐
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 5. Copy Helper
                    st.caption("👇 העתק את הטקסט מכאן לשליחה בוואטסאפ:")
                    st.text_area("Label", value=hebrew_greeting, height=150, label_visibility="collapsed")
                    
                else:
                    st.error("אירעה שגיאה ביצירת התוכן. נסה שוב או בדוק את המפתח.")

if __name__ == "__main__":
    main()
