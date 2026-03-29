import streamlit as st
import google.generativeai as genai
from groq import Groq
import re

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="JAAO Auto-Suno Pro", page_icon="🌈", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #ffffff; }
    [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.05); }
    .rainbow-title { font-weight: 800; background: linear-gradient(to right, #00f2fe, #4facfe, #9933ff, #ff3366); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 38px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00f2fe, #4facfe); color: #000; border-radius: 12px; font-weight: bold; border: none; padding: 10px; }
    .copy-section { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 15px; }
    .label-tag { background: #4facfe; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-bottom: 5px; display: inline-block; }
    .suno-button { 
        display: inline-block; padding: 12px 24px; background: linear-gradient(90deg, #ff00cc, #3333ff); 
        color: white !important; text-decoration: none; border-radius: 10px; font-weight: bold; 
        text-align: center; margin-top: 10px; width: 100%; transition: 0.3s;
    }
    .suno-button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(255, 0, 204, 0.4); }
</style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def extract_content(text, tag):
    pattern = f"{tag}:(.*?)(?=(TITLE:|STYLE:|LYRICS:|$))"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='rainbow-title'>JAAO Studio</h1>", unsafe_allow_html=True)
    ai_choice = st.radio("เลือก AI Engine:", ["Gemini (Google)", "Groq (Llama 3.1)"])
    
    if ai_choice == "Gemini (Google)":
        api_key = st.text_input("Gemini API Key:", type="password")
        model_option = "gemini-1.5-flash"
    else:
        api_key = st.text_input("Groq API Key:", type="password")
        model_option = "llama-3.1-8b-instant"

    st.divider()
    artist_name = st.text_input("Artist Name:", value="JAAO")
    song_topic = st.text_area("หัวข้อเพลง (Story):", placeholder="ใส่เรื่องราวที่อยากให้ AI คำนวณ...")
    
    main_style = st.selectbox("แนวเพลงหลัก:", ["Pop", "Country / Folk", "Indie / Rock", "Hip Hop / R&B"])
    selected_style = st.selectbox("สไตล์เฉพาะ:", ["T-Pop", "Modern Ballad", "Trap", "Folk Song", "Thai Rock"])
    
    generate_btn = st.button("🚀 คำนวณและสร้างเพลง")

# --- 4. MAIN CONTENT ---
if generate_btn:
    if not api_key:
        st.warning(f"⚠️ กรุณาใส่ API Key ของ {ai_choice}")
    elif not song_topic:
        st.error("⚠️ บอกเรื่องราวของเพลงก่อนครับ")
    else:
        prompt = f"""Task: Create a song for Suno AI. Artist: {artist_name}, Topic: {song_topic}, Genre: {selected_style}. 
        Output Format: TITLE: [Thai Title], STYLE: [English Tags], LYRICS: [Thai with Chords]"""
        try:
            with st.spinner(f'🪄 {ai_choice} กำลังคำนวณ...'):
                if ai_choice == "Gemini (Google)":
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_option)
                    response = model.generate_content(prompt)
                    res_text = response.text
                else:
                    client = Groq(api_key=api_key)
                    completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=model_option)
                    res_text = completion.choices[0].message.content

                st.balloons()
                title = extract_content(res_text, "TITLE")
                style_tags = extract_content(res_text, "STYLE")
                lyrics = extract_content(res_text, "LYRICS")

                st.success(f"✅ AI คำนวณเสร็จแล้ว: **{title}**")
                
                # --- ส่วนแสดงผลและปุ่มลิงก์ ---
                col1, col2 = st.columns([1, 1.5])
                with col1:
                    st.markdown("<div class='copy-section'><span class='label-tag'>📌 1. SONG TITLE</span>", unsafe_allow_html=True)
                    st.code(title)
                    st.markdown("<span class='label-tag'>🎹 2. STYLE PROMPT</span>", unsafe_allow_html=True)
                    st.code(f"Thai, {style_tags}")
                    
                    # เพิ่มปุ่มลิงก์ไป Suno
                    st.markdown(f"""
                        <a href="https://suno.com/create" target="_blank" class="suno-button">
                            🎨 เปิด Suno.com (สร้างเพลงเลย)
                        </a>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                with col2:
                    st.markdown("<div class='copy-section'><span class='label-tag'>📝 3. LYRICS & CHORDS</span>", unsafe_allow_html=True)
                    st.code(lyrics if lyrics else res_text)
                    st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
else:
    # --- หน้า Welcome / Guide ---
    st.markdown("### 🎼 ยินดีต้อนรับสู่ JAAO Auto-Suno")
    st.write("กรอกข้อมูลด้านซ้ายเพื่อเริ่มงาน หรือดูวิธีขอ Key ได้ที่ปุ่มด้านล่าง")
    
    with st.expander("📖 วิธีขอ API Key (ฟรี)"):
        col_g, col_q = st.columns(2)
        with col_g:
            st.info("**Gemini Key:** ขอได้ที่ [Google AI Studio](https://aistudio.google.com/)")
        with col_q:
            st.info("**Groq Key:** ขอได้ที่ [Groq Console](https://console.groq.com/keys)")

st.markdown("---")
st.caption("Developed by JAAO Studio | 🚀 Engine: Hybrid v2.7")
