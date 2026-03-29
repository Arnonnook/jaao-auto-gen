import streamlit as st
import google.generativeai as genai 
from groq import Groq
import re

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="JAAO Music Studio", page_icon="🎵", layout="wide")

st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at top right, #0a192f, #050a14); color: #e6f1ff; }
    [data-testid="stSidebar"] { background-color: rgba(10, 25, 47, 0.9); border-right: 1px solid #1e3a5f; }
    .hero-title { font-size: clamp(30px, 5vw, 60px); font-weight: 850; background: linear-gradient(to bottom, #ffffff, #8892b0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .music-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 25px; backdrop-filter: blur(15px); margin-bottom: 20px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #1e3a5f, #3366ff); color: white !important; border-radius: 50px; font-weight: bold; border: none; padding: 12px; }
    .label-tag { background: rgba(0, 68, 204, 0.4); color: #00f2fe; padding: 4px 10px; border-radius: 5px; font-size: 12px; font-weight: bold; margin-bottom: 10px; display: inline-block; border: 1px solid #00f2fe; }
    .suno-link { display: block; text-align: center; padding: 15px; background: #3366ff; color: white !important; text-decoration: none; border-radius: 12px; font-weight: bold; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

def extract_content(text, tag):
    pattern = f"{tag}:(.*?)(?=(TITLE:|STYLE:|LYRICS:|$))"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe;'>⚙️ ตั้งค่าสตูดิโอ</h2>", unsafe_allow_html=True)
    ai_choice = st.radio("เลือก AI Engine", ["Gemini", "Groq"])
    api_key = st.text_input("ใส่ API Key", type="password")
    
    st.divider()
    artist = st.text_input("ชื่อศิลปิน", value="JAAO Official")
    topic = st.text_area("เนื้อหา/เรื่องราวของเพลง", placeholder="เช่น รักข้างเดียวในฤดูฝน...")
    
    gender = st.selectbox("เพศนักร้อง", ["Male (ชาย)", "Female (หญิง)", "Duet (คู่)"])
    vocal_tone = st.selectbox("โทนเสียง", ["High Pitch (เสียงสูง)", "Deep/Warm (ทุ้ม/อบอุ่น)", "Soft (นุ่มนวล)", "Powerful (ดุดัน)"])
    tempo_style = st.select_slider("จังหวะ (Tempo)", options=["Slow", "Moderate", "Fast"])
    
    style = st.selectbox("แนวเพลง", ["EDM", "T-Pop", "Thai Rock", "LUK THUNG", "Puea Chiwit", "R&B"])
    generate_btn = st.button("🚀 รังสรรค์เพลงแบบละเอียด")

# --- 3. MAIN CONTENT ---
st.markdown("<h1 class='hero-title'>Deep Blue<br>Sound Production</h1>", unsafe_allow_html=True)

if generate_btn:
    if not api_key or not topic:
        st.warning("⚠️ กรุณากรอก API Key และเนื้อหาเพลง")
    else:
        prompt = f"""
        Task: Create a highly detailed prompt for Suno AI.
        Artist: {artist}, Topic: {topic}, Main Genre: {style}
        Vocal: {gender}, Tone: {vocal_tone}, Tempo: {tempo_style}

        Output Format:
        TITLE: [ชื่อเพลงภาษาไทย]
        STYLE: [English tags: genre, BPM, vocal gender, vocal pitch, atmosphere, key, mood, instruments]
        LYRICS: [Thai lyrics with chords [C][G] and structure [Verse][Chorus]]
        """

        try:
            with st.spinner('🪄 กำลังคำนวณรายละเอียดเพลง...'):
                if ai_choice == "Gemini":
                    genai.configure(api_key=api_key)
                    res_text = genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt).text
                else:
                    res_text = Groq(api_key=api_key).chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.1-8b-instant").choices[0].message.content

                title = extract_content(res_text, "TITLE")
                style_tags = extract_content(res_text, "STYLE")
                lyrics = extract_content(res_text, "LYRICS")

                st.balloons()
                
                # แสดงผลส่วนที่ 1
                st.markdown(f"""
                <div class='music-card'>
                    <span class='label-tag'>📌 ชื่อเพลง</span>
                    <h2 style='margin:0;'>{title}</h2>
                    <hr style='opacity:0.1; margin:15px 0;'>
                    <span class='label-tag'>🎹 STYLE (รายละเอียดเจาะลึก)</span>
                    <div style='background:rgba(0,0,0,0.3); padding:15px; border-radius:10px; border:1px solid #1e3a5f;'>
                        <code style='color:#00f2fe;'>{style_tags}</code>
                    </div>
                    <a href='https://suno.com/create' target='_blank' class='suno-link'>เปิด SUNO AI (CUSTOM MODE)</a>
                </div>
                """, unsafe_allow_html=True)

                # แสดงเนื้อร้อง
                st.markdown("<div class='music-card'>", unsafe_allow_html=True)
                st.markdown("<span class='label-tag'>📝 เนื้อร้องและคอร์ด</span>", unsafe_allow_html=True)
                st.code(lyrics if lyrics else res_text, language="markdown")
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("👈 ปรับแต่งรายละเอียดนักร้องและจังหวะที่ด้านซ้าย เพื่อเริ่มการคำนวณครับ")

st.markdown("<p style='text-align:center; opacity:0.3; font-size:12px;'>JAAO STUDIO x MuseGen UI | 2026 Edition</p>", unsafe_allow_html=True)
