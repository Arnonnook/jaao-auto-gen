import streamlit as st
import google.generativeai as genai
from groq import Groq
import re

# --- 1. SETTINGS & THEME (Dark Modern Luxury) ---
st.set_page_config(page_title="JAAO Music Studio", page_icon="🎵", layout="wide")

st.markdown("""
<style>
    /* พื้นหลังหลักโทน Deep Blue */
    .stApp {
        background: radial-gradient(circle at top right, #0a192f, #050a14);
        color: #e6f1ff;
    }

    /* ตกแต่ง Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 25, 47, 0.9);
        border-right: 1px solid #1e3a5f;
    }

    /* หัวข้อใหญ่สไตล์ในรูป */
    .hero-title {
        font-size: clamp(40px, 8vw, 70px);
        font-weight: 850;
        line-height: 1.1;
        background: linear-gradient(to bottom, #ffffff, #8892b0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    /* การ์ดกระจก Glassmorphism */
    .music-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(15px);
        margin-bottom: 20px;
    }

    /* ปุ่มสไตล์ Blue Neon */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1e3a5f, #3366ff);
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 12px;
        font-weight: bold;
        transition: 0.3s;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(51, 102, 255, 0.5);
        transform: translateY(-2px);
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
        margin-right: 5px;
        background: rgba(0, 68, 204, 0.3);
        color: #00f2fe;
        border: 1px solid #00f2fe;
    }

    /* ลิงก์ Suno */
    .suno-link {
        display: block;
        text-align: center;
        padding: 15px;
        background: #3366ff;
        color: white !important;
        text-decoration: none;
        border-radius: 12px;
        font-weight: bold;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def extract_content(text, tag):
    pattern = f"{tag}:(.*?)(?=(TITLE:|STYLE:|LYRICS:|$))"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe;'>⚙️ Studio Config</h2>", unsafe_allow_html=True)
    ai_choice = st.radio("AI Engine", ["Gemini", "Groq"])
    api_key = st.text_input("API Key", type="password", placeholder="Paste Key Here")
    
    st.divider()
    artist = st.text_input("Artist Name", value="JAAO Official")
    topic = st.text_area("Song Concept / Story", placeholder="Describe your music idea...")
    
    style = st.selectbox("Genre", ["EDM", "Pop", "Rock", "LUK THUNG", "HIPHOP", "Indie"])
    generate_btn = st.button("Generate Masterpiece")

# --- 4. HERO SECTION ---
col_hero, col_img = st.columns([1.2, 1])

with col_hero:
    st.markdown("<h1 class='hero-title'>Dive Into<br>Deep Blue<br>Sound</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8892b0; font-size:18px;'>สร้างและคำนวณบทเพลงระดับพรีเมียมสำหรับ Suno AI โดยเฉพาะ</p>", unsafe_allow_html=True)
    st.markdown("""
        <span class='badge'>Exclusive License</span>
        <span class='badge'>Full Mix MP3</span>
        <span class='badge'>Crystal UI Theme</span>
        <span class='badge'>PromptPay</span>
    """, unsafe_allow_html=True)

with col_img:
    # รูปบรรยากาศสตูดิโอ/คอนเสิร์ต
    st.image("
