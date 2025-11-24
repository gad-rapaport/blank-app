import streamlit as st
from config import PAGE_CONFIG, CUSTOM_CSS
from utils import init_session_state, sanitize_input, get_whatsapp_link, save_to_history
from logic import generate_perfect_content, generate_image_url

# --- אתחול ---
st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
init_session_state()

# --- פונקציית עזר למפתח ---
def get_api_key():
    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]
    return st.sidebar.text_input("🔑 Gemini API Key", type="password")

# --- ממשק משתמש ראשי ---
def main():
    st.markdown('<div class="glass-card"><h1 style="text-align:center;">💎 LoveFlow Ultimate</h1><p style="text-align:center;">AI Romantic Architect</p></div>', unsafe_allow_html=True)

    api_key = get_api_key()

    # --- Sidebar: History & Settings ---
    with st.sidebar:
        st.header("📜 History")
        if st.session_state.history:
            for i, item in enumerate(st.session_state.history[:5]):
                with st.expander(f"For: {item['recipient']} ({item['occasion']})"):
                    st.write(item['greeting'][:50] + "...")
        else:
            st.info("No history yet.")

    # --- Main Form ---
    with st.form("generation_form"):
        st.markdown("### 💌 Details")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            sender_gender = st.radio("I am:", ["Male 👨", "Female 👩"], horizontal=True)
        with col_g2:
            recipient_gender = st.radio("Writing to:", ["Male 👨", "Female 👩"], horizontal=True)

        col1, col2 = st.columns(2)
        with col1:
            recipient_name = st.text_input("Name", placeholder="e.g., Daniel")
            relation = st.selectbox("Relation", ["Partner", "Date", "Best Friend", "Family", "Colleague", "Ex"])
        
        with col2:
            occasion = st.selectbox("Occasion", ["Birthday", "Anniversary", "Apology", "Miss You", "Encouragement"])
            tone = st.selectbox("Tone", ["Romantic", "Funny", "Deep", "Rhyming", "Casual"])

        details = st.text_area("Personal Touch", placeholder="Loves sushi, always late, inside jokes...")
        
        submitted = st.form_submit_button("✨ Generate Magic")

    # --- Processing ---
    if submitted:
        if not api_key:
            st.error("⚠️ Please provide an API Key.")
            return
        
        if not recipient_name:
            st.warning("⚠️ Who is this for? Please enter a name.")
            return

        # Sanitization & Prep
        params = {
            "sender_gender": sender_gender,
            "recipient_gender": recipient_gender,
            "recipient_name": sanitize_input(recipient_name),
            "relation": relation,
            "occasion": occasion,
            "tone": tone,
            "details": sanitize_input(details)
        }

        with st.spinner("🔮 Weaving words & dreaming images..."):
            # קריאה ללוגיקה
            result_json = generate_perfect_content(api_key, params)

            if result_json:
                greeting = result_json.get("greeting")
                img_prompt = result_json.get("image_prompt")
                
                # יצירת תמונה
                image_url = generate_image_url(img_prompt)
                
                # שמירה להיסטוריה
                save_to_history({
                    "recipient": params['recipient_name'],
                    "occasion": params['occasion'],
                    "greeting": greeting
                })

                # --- הצגת התוצאה ---
                st.balloons()
                
                tab1, tab2, tab3 = st.tabs(["💌 The Card", "🚀 Social Kit", "⚙️ Raw Data"])

                with tab1:
                    col_img, col_txt = st.columns([1, 1])
                    with col_img:
                        st.image(image_url, use_container_width=True, caption="AI Generated Art")
                    with col_txt:
                        st.markdown(f"""
                        <div class="glass-card" style="direction:rtl; text-align:right;">
                        {greeting.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <a href="{get_whatsapp_link(greeting)}" target="_blank" style="text-decoration:none;">
                            <button style="width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">
                                Send via WhatsApp 🟢
                            </button>
                        </a>
                        """, unsafe_allow_html=True)

                with tab2:
                    st.success("🎥 TikTok Idea:")
                    st.write(result_json.get("tiktok_idea"))
                    st.info("🏷️ Hashtags:")
                    st.code(result_json.get("hashtags"))

                with tab3:
                    st.json(result_json)
                    
            else:
                st.error("❌ Generation failed. Please check your API key or try again.")

if __name__ == "__main__":
    main()
