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
    pre { white-space: pre-wrap !important; font-family: 'Courier New', Courier, monospace; color: #00f2fe; background: #000; padding: 15px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

def extract_content(text, tag):
    pattern = f"{tag}:(.*?)(?=(TITLE:|STYLE:|LYRICS:|$))"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe;'>⚙️ Studio Config</h2>", unsafe_allow_html=True)
    ai_choice = st.radio("AI Engine", ["Gemini", "Groq"])
    api_key = st.text_input("ใส่ API Key", type="password")
    
    st.divider()
    artist = st.text_input("ชื่อศิลปิน", value="JAAO Official")
    topic = st.text_area("หัวข้อเพลง", placeholder="เช่น แอบรักรุ่นพี่...")
    gender = st.selectbox("เพศนักร้อง", ["Male", "Female", "Duet"])
    vocal_tone = st.selectbox("โทนเสียง", ["High Pitch", "Warm/Deep", "Soft", "Power"])
    style = st.selectbox("แนวเพลง", ["EDM", "T-Pop", "Thai Rock", "LUK THUNG", "Indie"])
    
    generate_btn = st.button("🚀 รังสรรค์เพลงพร้อมคอร์ด")

# --- 3. MAIN ---
st.markdown("<h1 class='hero-title'>Deep Blue<br>Lyrics & Chords</h1>", unsafe_allow_html=True)

if generate_btn:
    if not api_key or not topic:
        st.warning("⚠️ กรุณากรอกข้อมูลให้ครบ")
    else:
        # ปรับ Prompt ให้เน้นคอร์ดเป็นพิเศษ
        prompt = f"""
        Task: Write a Thai song with GUITAR CHORDS for Suno AI.
        Artist: {artist}, Topic: {topic}, Genre: {style}, Vocal: {gender}, Tone: {vocal_tone}
        
        Mandatory Instructions:
        1. Place guitar chords like [C], [Am], [G7] EXACTLY above the lyrics.
        2. Chords must be on their own line above the text they belong to.
        3. Use full song structure: [Intro], [Verse], [Chorus], [Bridge], [Outro].
        
        Format:
        TITLE: [Song Name]
        STYLE: [Detailed English Tags]
        LYRICS:
        (Chords and Lyrics here)
        """

        try:
            with st.spinner('🪄 กำลังคำนวณเนื้อร้องและวางคอร์ดกีตาร์...'):
                if ai_choice == "Gemini":
                    genai.configure(api_key=api_key)
                    res_text = genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt).text
                else:
                    res_text = Groq(api_key=api_key).chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.1-8b-instant").choices[0].message.content

                title = extract_content(res_text, "TITLE")
                style_tags = extract_content(res_text, "STYLE")
                lyrics = extract_content(res_text, "LYRICS")

                # Fallback ถ้าดึงไม่ได้
                if not lyrics:
                    lyrics = res_text.split("LYRICS:")[-1].strip() if "LYRICS:" in res_text else res_text

                st.balloons()
                
                # แสดงผลการ์ดเพลง
                st.markdown(f"""
                <div class='music-card'>
                    <span class='label-tag'>📌 ชื่อเพลง</span>
                    <h2 style='margin:0;'>{title if title else "Untitled"}</h2>
                    <hr style='opacity:0.1; margin:15px 0;'>
                    <span class='label-tag'>🎹 STYLE (รายละเอียดเจาะลึก)</span>
                    <div style='background:rgba(0,0,0,0.3); padding:15px; border-radius:10px;'>
                        <code>{style_tags}</code>
                    </div>
                    <a href='https://suno.com/create' target='_blank' class='suno-link'>เปิด SUNO AI เพื่อใส่เนื้อร้อง</a>
                </div>
                """, unsafe_allow_html=True)

                # ส่วนเนื้อร้อง (ใช้ st.text แทน st.code เพื่อรักษาช่องว่างของคอร์ด)
                st.markdown("<div class='music-card'>", unsafe_allow_html=True)
                st.markdown("<span class='label-tag'>🎸 เนื้อร้องและคอร์ดกีตาร์ (ก๊อปปี้ไปวาง Suno)</span>", unsafe_allow_html=True)
                st.text(lyrics) # ใช้ st.text จะคงตำแหน่งช่องว่างได้ดีกว่าสำหรับคอร์ด
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("👈 กรอกรายละเอียดเพื่อรังสรรค์เพลงพร้อมคอร์ดกีตาร์ครับ")

st.markdown("<p style='text-align:center; opacity:0.3; font-size:12px;'>JAAO STUDIO x MuseGen UI | 2026 Edition</p>", unsafe_allow_html=True)
