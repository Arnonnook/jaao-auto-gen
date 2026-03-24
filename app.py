import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าตาเว็บ (Colorful & Fast)
st.set_page_config(page_title="JAAO AI STUDIO", page_icon="🎨", layout="centered")

# --- ส่วนตกแต่งหน้าเว็บด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #f0faff; }
    h1 {
        color: #ff4b4b;
        text-align: center;
        background: -webkit-linear-gradient(#ff4b4b, #ffda5f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Arial Black', sans-serif;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 12px;
        font-weight: bold;
        height: 3em;
        width: 100%;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .result-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ff4b4b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# 2. ตั้งค่า API Key (ใส่รหัสของคุณแทนที่จุดนี้)
API_KEY = "AIzaSyD7PL5ugkzzVGn00Sy8rzwdiMqis7mIjQQ"
genai.configure(api_key=API_KEY)

# ใช้รุ่น 2.5 Flash ตามที่ระบบคุณแนะนำ (เร็วและฉลาดสุด)
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. ส่วนการแสดงผลหน้าเว็บ
st.markdown("<h1>🌟 JAAO AI AUTO-GEN</h1>", unsafe_allow_html=True)
st.write("---")

# เลือกโหมดการทำงาน
option = st.selectbox(
    '🚀 เลือกสิ่งที่ต้องการสร้าง:',
    ('🎵 แต่งเนื้อเพลงสุดปัง', '📹 เขียนสคริปต์วิดีโอ', '💡 คิดไอเดียคอนเทนต์', '🐍 เขียนโค้ด Python')
)

# ช่องรับคำสั่ง (ใช้ชื่อตัวแปร user_input ให้ตรงกัน)
user_input = st.text_area(f"รายละเอียดสำหรับ {option}:", placeholder="พิมพ์รายละเอียดที่นี่ เช่น อยากได้เพลงรักแนวลูกทุ่งซึ้งๆ...")

# 4. ส่วน
