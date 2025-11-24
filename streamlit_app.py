import streamlit as st
from config import AppConfig, CUSTOM_CSS
from i18n import TRANSLATIONS
from utils import init_session_state, sanitize_input, get_whatsapp_link, save_to_history
from logic import generate_perfect_content, generate_image_url

# --- 1. אתחול האפליקציה ---
st.set_page_config(page_title=AppConfig.PAGE_TITLE, page_icon=AppConfig.PAGE_ICON, layout=AppConfig.LAYOUT)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
init_session_state()

# פונקציית עזר לשליפת טקסטים לפי שפה
def t(key):
    return TRANSLATIONS[st.session_state.lang][key]

# --- 2. Sidebar (הגדרות והיסטוריה) ---
with st.sidebar:
    st.header(t("settings"))
    
    # בחירת שפה
    selected_lang = st.selectbox("🌐 Language / שפה", ["he", "en"], index=0 if st.session_state.lang == 'he' else 1)
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

    # API Key
    api_key = st.text_input("Gemini API Key", type="password")
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]

    st.divider()
    
    # היסטוריה
    st.subheader(t("history"))
    if st.session_state.history:
        for item in st.session_state.history[:5]:
            with st.expander(f"{item['recipient']} - {item['occasion']}"):
                st.write(item['greeting'][:50] + "...")
    else:
        st.info(t("no_history"))

    st.caption(f"UI Variant: {st.session_state.ab_variant}")

# --- 3. Main UI ---
st.markdown(f'<div class="glass-card"><h1 style="text-align:center;">{AppConfig.PAGE_ICON} {t("page_title")}</h1><p style="text-align:center;">{t("subtitle")}</p></div>', unsafe_allow_html=True)

with st.form("main_form"):
    st.subheader(t("details_header"))
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        sender_gender = st.radio(t("sender_label"), [t("male"), t("female")], horizontal=True)
    with col_g2:
        recipient_gender = st.radio(t("recipient_label"), [t("male"), t("female")], horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        recipient_name = st.text_input(t("name_label"))
        # תיקון קטן לבחירת רשימות לפי שפה
        relations_en = ["Partner", "Date", "Friend", "Family", "Ex"]
        relations_he = ["בן/בת זוג", "דייט", "חבר/ה", "משפחה", "אקס/ית"]
        relation = st.selectbox(t("relation_label"), relations_en if st.session_state.lang == 'en' else relations_he)
    
    with col2:
        occasions_en = ["Birthday", "Anniversary", "Apology"]
        occasions_he = ["יום הולדת", "יום נישואין", "סליחה", "געגוע", "עידוד"]
        occasion = st.selectbox(t("occasion_label"), occasions_en if st.session_state.lang == 'en' else occasions_he)
        
        tones_en = ["Romantic", "Funny", "Deep"]
        tones_he = ["רומנטי", "מצחיק", "עמוק", "חרוזים", "סחבק"]
        tone = st.selectbox(t("tone_label"), tones_en if st.session_state.lang == 'en' else tones_he)

    details = st.text_area(t("details_label"), placeholder=t("details_placeholder"))
    
    submitted = st.form_submit_button(t("generate_btn"), help="Click to generate AI content")

# --- 4. לוגיקה ותצוגה ---
if submitted:
    if not api_key:
        st.error(t("error_api"))
    elif not recipient_name:
        st.warning(t("error_name"))
    else:
        clean_name = sanitize_input(recipient_name)
        clean_details = sanitize_input(details)
        
        params = {
            "sender_gender": sender_gender,
            "recipient_gender": recipient_gender,
            "recipient_name": clean_name,
            "relation": relation,
            "occasion": occasion,
            "tone": tone,
            "details": clean_details
        }

        with st.spinner(t("loading")):
            result = generate_perfect_content(api_key, params, st.session_state.lang)

            if result:
                greeting = result.get("greeting")
                img_prompt = result.get("image_prompt")
                image_url = generate_image_url(img_prompt)
                
                save_to_history({"recipient": clean_name, "occasion": occasion, "greeting": greeting})
                
                st.balloons()
                
                if st.session_state.ab_variant == 'A':
                    tab1, tab2, tab3 = st.tabs([t("tab_card"), t("tab_social"), t("tab_raw")])
                    
                    with tab1:
                        # --- התיקון בוצע כאן: הוחלף use_container_width ב-use_column_width ---
                        st.image(image_url, use_column_width=True, alt=f"AI generated: {img_prompt}")
                        
                        st.markdown(f'<div class="glass-card" style="direction:{"rtl" if st.session_state.lang=="he" else "ltr"};">{greeting.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<a href="{get_whatsapp_link(greeting)}" target="_blank" style="text-decoration:none;"><button style="width:100%; padding:12px; background:#25D366; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">{t("whatsapp_btn")}</button></a>', unsafe_allow_html=True)
                    
                    with tab2:
                        st.info(result.get("tiktok_idea"))
                        st.code(result.get("hashtags"))
                    
                    with tab3:
                        st.json(result)

                else: # Variant B
                    # --- גם כאן בוצע התיקון ---
                    st.image(image_url, use_column_width=True)
                    
                    st.success(greeting)
                    st.caption("Variant B: Simplified View")
                    with st.expander(t("tab_social")):
                         st.write(result.get("tiktok_idea"))

                st.divider()
                st.markdown(f"### {t('gift_title')}")
                st.markdown(t('gift_desc'))
                st.link_button("Zer4U 💐", "https://zer4u.co.il")

            else:
                st.error("Error generating content.")
