import streamlit as st
# เปลี่ยนมาใช้ตัวใหม่ตามคำเตือน
import google.generativeai as genai 
from groq import Groq
import re

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="JAAO Music Studio", page_icon="🎵", layout="wide")

st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at top right, #0a192f, #050a14); color: #e6f1ff; }
    [data-testid="stSidebar"] { background-color: rgba(10, 25, 47, 0.9); border-right: 1px solid #1e3a5f; }
    .hero-title { font-size: clamp(40px, 8vw, 70px); font-weight: 850; line-height: 1.1; background: linear-gradient(to bottom, #ffffff, #8892b0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .music-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 25px; backdrop-filter: blur(15px); margin-bottom: 20px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #1e3a5f, #3366ff); color: white !important; border-radius: 50px; border: none; padding: 12px; font-weight: bold; }
    .badge { display: inline-block; padding: 4px 12px; border-radius: 4px; font-size: 10px; font-weight: bold; margin-right: 5px; background: rgba(0, 68, 204, 0.3); color: #00f2fe; border: 1px solid #00f2fe; }
    .suno-link { display: block; text-align: center; padding: 15px; background: #3366ff; color: white !important; text-decoration: none; border-radius: 12px; font-weight: bold; margin-top: 20px; }
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
    api_key = st.text_input("API Key", type="password")
    st.divider()
    artist = st.text_input("Artist Name", value="JAAO Official")
    topic = st.text_area("Song Concept")
    style = st.selectbox("Genre", ["EDM", "Pop", "Rock", "LUK THUNG", "HIPHOP"])
    generate_btn = st.button("Generate Masterpiece")

# --- 3. HERO SECTION ---
col_hero, col_img = st.columns([1.2, 1])
with col_hero:
    st.markdown("<h1 class='hero-title'>Dive Into<br>Deep Blue<br>Sound</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8892b0;'>สร้างและคำนวณบทเพลงระดับพรีเมียมสำหรับ Suno AI</p>", unsafe_allow_html=True)
    st.markdown("<span class='badge'>Exclusive License</span><span class='badge'>Full Mix MP3</span>", unsafe_allow_html=True)

with col_img:
    # แก้ไขตรงนี้: เปลี่ยน use_container_width เป็น width='stretch' ตามคำเตือน
    st.image("https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1000&auto=format&fit=crop", width='stretch')

# --- 4. LOGIC ---
if generate_btn:
    if not api_key or not topic:
        st.error("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน")
    else:
        try:
            with st.spinner('🪄 Harmony in Progress...'):
                prompt = f"Create a Suno song. Artist: {artist}, Topic: {topic}, Genre: {style}. TITLE: [Thai], STYLE: [English Tags], LYRICS: [Thai with Chords]"
                if ai_choice == "Gemini":
                    genai.configure(api_key=api_key)
                    res_text = genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt).text
                else:
                    res_text = Groq(api_key=api_key).chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.1-8b-instant").choices[0].message.content

                title = extract_content(res_text, "TITLE")
                style_tags = extract_content(res_text, "STYLE")
                lyrics = extract_content(res_text, "LYRICS")

                st.balloons()
                st.markdown(f"""
                <div class='music-card'>
                    <h3 style='color:#ffffff;'>{title}</h3>
                    <p style='color:#8892b0;'>{style} | {artist}</p>
                    <hr style='opacity:0.1;'>
                    <p><b style='color:#00f2fe;'>STYLE:</b> {style_tags}</p>
                    <a href='https://suno.com/create' target='_blank' class='suno-link'>GO TO SUNO.COM</a>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<div class='music-card'>", unsafe_allow_html=True)
                st.code(lyrics if lyrics else res_text, language="markdown")
                st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    # ส่วนล่างที่เป็นการ์ดโชว์
    st.markdown("### Featured Tracks")
    c1, c2, c3 = st.columns(3)
    for col in [c1, c2, c3]:
        with col:
            st.markdown("<div class='music-card' style='text-align:center;'>🎧<br>Ready to Compose</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; opacity:0.2;'>JAAO STUDIO x MuseGen UI</p>", unsafe_allow_html=True)
