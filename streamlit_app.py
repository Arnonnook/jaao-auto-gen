import streamlit as st
import google.generativeai as genai
from groq import Groq
import re

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="JAAO Hybrid Suno", page_icon="🌈", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #ffffff; }
    [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.05); }
    .rainbow-title { font-weight: 800; background: linear-gradient(to right, #00f2fe, #4facfe, #9933ff, #ff3366); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 38px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00f2fe, #4facfe); color: #000; border-radius: 12px; font-weight: bold; border: none; padding: 10px; }
    .copy-section { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; }
    .label-tag { background: #ff3366; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; margin-bottom: 5px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def extract_content(text, tag):
    # ปรับปรุง Regex ให้ดึงข้อมูลได้แม่นยำขึ้น
    pattern = f"{tag}:(.*?)(?=(TITLE:|STYLE:|LYRICS:|$))"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='rainbow-title'>JAAO Studio</h1>", unsafe_allow_html=True)
    
    # --- จุดที่เลือก AI และใส่ KEY ---
    ai_choice = st.radio("เลือก AI Engine:", ["Gemini (Google)", "Groq (Llama 3.1)"])
    
    if ai_choice == "Gemini (Google)":
        api_key = st.text_input("ใส่ Gemini API Key:", type="password")
        model_option = "gemini-1.5-flash"
    else:
        # ช่องใส่ KEY GROQ จะอยู่ตรงนี้เมื่อเลือก Groq ครับ
        api_key = st.text_input("ใส่ Groq API Key (gsk_...):", type="password")
        model_option = "llama-3.1-8b-instant"

    st.divider()
    artist_name = st.text_input("Artist Name:", value="JAAO")
    song_topic = st.text_area("หัวข้อ/เรื่องราวเพลง:", placeholder="เช่น แอบรักเพื่อนแต่ไม่กล้าบอก...")
    
    main_style = st.selectbox("แนวเพลงหลัก:", ["Pop", "Country / Folk", "Indie / Rock", "Hip Hop / R&B"])
    selected_style = st.selectbox("สไตล์เฉพาะ:", ["T-Pop", "Modern Ballad", "Trap", "Folk Song", "Thai Rock"])
    
    generate_btn = st.button("🚀 รังสรรค์เพลง")

# --- 4. MAIN LOGIC ---
if generate_btn:
    if not api_key:
        st.warning(f"⚠️ กรุณาใส่ API Key ของ {ai_choice}")
    elif not song_topic:
        st.error("⚠️ กรุณาใส่หัวข้อเพลงก่อนครับ")
    else:
        # เตรียม Prompt
        prompt = f"""
        Task: Create a song for Suno AI.
        Artist: {artist_name}
        Topic: {song_topic}
        Style: {selected_style}
        
        Output format:
        TITLE: [ชื่อเพลงภาษาไทย]
        STYLE: [English Suno tags เช่น genre, mood, tempo]
        LYRICS:
        [Verse 1]
        [Chorus]
        (Include Thai lyrics with chords [C][G] above lyrics)
        """

        try:
            with st.spinner(f'กำลังใช้ {ai_choice} ปรุงแต่งเพลง...'):
                res_text = ""
                if ai_choice == "Gemini (Google)":
                    genai.configure(api_key=api_key)
                    # แก้ไขการเรียก Model ให้รองรับหลายชื่อ
                    try:
                        model = genai.GenerativeModel(model_option)
                        response = model.generate_content(prompt)
                    except:
                        model = genai.GenerativeModel(f"models/{model_option}")
                        response = model.generate_content(prompt)
                    res_text = response.text
                else:
                    # ส่วนของ Groq
                    client = Groq(api_key=api_key)
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model_option,
                    )
                    res_text = chat_completion.choices[0].message.content

                # --- 5. DISPLAY RESULTS ---
                st.balloons()
                
                # ดึงข้อมูลมาแยกส่วน (แก้ SyntaxError วงเล็บแล้ว)
                title = extract_content(res_text, "TITLE")
                style_tags = extract_content(res_text, "STYLE")
                lyrics = extract_content(res_text, "LYRICS")

                col1, col2 = st.columns([1, 1.5])

                with col1:
                    st.markdown("<div class='copy-section'>", unsafe_allow_html=True)
                    st.markdown("<span class='label-tag'>SONG TITLE</span>", unsafe_allow_html=True)
                    st.code(title if title else "ไม่ได้ระบุชื่อ")
                    
                    st.markdown("<span class='label-tag'>SUNO STYLE PROMPT</span>", unsafe_allow_html=True)
                    st.code(f"Thai, {style_tags}", language="markdown")
                    st.info("💡 ก๊อปปี้ช่องนี้ไปวางใน 'Style of Music' ของ Suno")
                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='copy-section'>", unsafe_allow_html=True)
                    st.markdown("<span class='label-tag'>LYRICS & CHORDS</span>", unsafe_allow_html=True)
                    st.code(lyrics if lyrics else res_text, language="markdown")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.success("สร้างสำเร็จ! ลองเอาไปใช้ใน Suno ดูนะครับ")

        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดทางเทคนิค: {str(e)}")

else:
    st.info("กรอกข้อมูลและ Key ด้านซ้ายเพื่อเริ่มงานครับ")

st.markdown("---")
st.caption("🌈 JAAO Studio x Suno AI | Hybrid Engine v2.5")
