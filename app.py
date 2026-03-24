import streamlit as st
import google.generativeai as genai
import datetime
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Creative Studio v.7", page_icon="🔴", layout="centered")

# ระบบเก็บข้อมูลใน Session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# --- การตกแต่งด้วย CSS (เน้นชื่อแอปสีแดงและปุ่มที่ชัดเจน) ---
st.markdown("""
<style>
    .stApp { background-color: #fdfcf5; }
    
    /* ชื่อแอป v.7 สีแดงสด ตัวหนาพิเศษ */
    .app-title {
        color: #e63946 !important;
        text-align: center;
        font-size: 45px !important;
        font-weight: 900 !important;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .app-version {
        color: #555;
        text-align: center;
        font-size: 18px;
        margin-bottom: 20px;
    }
    
    /* ปุ่มรันสีแดงยักษ์ */
    div.stButton > button:first-child {
        background-color: #e63946 !important;
        color: white !important;
        height: 65px;
        font-size: 22px;
        font-weight: bold;
        border-radius: 15px;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #c1121f !important;
        transform: scale(1.02);
    }
    
    /* กล่องข้อมูลพิเศษสีเข้ม */
    .special-info {
        background-color: #2d3436;
        color: #ffffff !important;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #fab005;
        margin-top: 15px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# 2. ดึง Key จาก Secrets
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key! โปรดเช็คที่หน้า Settings > Secrets")
    st.stop()

# 3. ส่วนหน้าจอหลัก
st.markdown('<h1 class="app-title">🔴 JAAO Creative Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-version">Version 7.0 | AI Powerhouse</p>', unsafe_allow_html=True)

# แถบด้านข้าง (Sidebar)
with st.sidebar:
    st.title("📜 ประวัติการใช้งาน")
    if st.button("🗑️ ล้างประวัติ"):
        st.session_state.history = []
        st.rerun()
    st.write("---")
    for item in reversed(st.session_state.history):
        with st.expander(f"📌 {item['time']} - {item['type']}"):
            st.write(item['result'])

# --- ปุ่มลัด Quick Prompts (5 ปุ่ม) ---
st.write("✨ **กดเลือกสไตล์ด่วน:**")
c1, c2, c3, c4, c5 = st.columns
