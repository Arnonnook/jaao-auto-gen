import streamlit as st
import google.generativeai as genai
import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Creative Studio", page_icon="🌈", layout="centered")

# สร้างระบบเก็บข้อมูลใน Session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #fdfcf5; }
    h1 { color: #ff4b4b; text-align: center; font-weight: bold; }
    
    /* สไตล์ปุ่มกดหลัก */
    div.stButton > button:first-child {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 15px;
        width: 100%;
        height: 55px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* สไตล์ปุ่มตัวอย่าง */
    .stButton > button[kind="secondary"] {
        font-size: 13px !important;
        background-color: #ffeaea !important;
        color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. ดึง Key จาก Secrets
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key! กรุณาตั้งค่าใน Streamlit Cloud Secrets")
    st.stop()

# 3. ส่วนแสดงผลหลัก
st.markdown("<h1>🌈 JAAO Creative Studio</h1>", unsafe_allow_html=True)

# --- แถบด้านข้าง (Sidebar): คู่มือ & ประวัติ ---
with st.sidebar:
    st.title("📖 คู่มือการใช้งาน")
    with st.expander("📝 ขั้นตอนเริ่มต้น", expanded=True):
        st.write("""
        1. **เลือกโหมด:** เลือกงานที่ต้องการ (แต่งเพลง/ทำภาพ)
        2. **ใส่รายละเอียด:** พิมพ์โจทย์ที่ต้องการ ยิ่งละเอียดยิ่งดี
        3. **กดปุ่มรัน:** รอ AI ประมวลผลสักครู่
        4. **เช็คประวัติ:** งานเก่าจะถูกเก็บ
