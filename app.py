import streamlit as st
import google.generativeai as genai
import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Creative Studio", page_icon="🌈", layout="centered")

# ระบบเก็บข้อมูลใน Session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# --- การตกแต่งด้วย CSS (เน้นความชัดเจนของตัวหนังสือ) ---
st.markdown("""
<style>
    .stApp { background-color: #fdfcf5; }
    h1 { color: #ff4b4b; text-align: center; font-weight: bold; }
    
    /* สไตล์ปุ่มกดหลัก */
    .main-button > div > button {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 15px;
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
    }
    
    /* กล่องข้อมูลพิเศษ (ปรับใหม่: พื้นหลังเข้ม ตัวหนังสือขาว) */
    .special-info {
        background-color: #2d3436; /* สีเทาเข้มเกือบดำ */
        color: #ffffff !important; /* ตัวหนังสือสีขาวบริสุทธิ์ */
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #fab005; /* ขอบสีเหลืองทองเพิ่มความเด่น */
        margin-top: 15px;
        line-height: 1.6;
        font-size: 16px;
    }
    .special-info b, .special-info strong {
        color: #fab005 !important; /* เน้นตัวหนาด้วยสีเหลืองทอง */
    }
</style>
""", unsafe_allow_html=True)

# 2. ดึง Key จาก Secrets
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key! กรุณาตรวจสอบ Secrets")
    st.stop()

# 3. ส่วนหน้าจอหลัก
st.markdown("<h1>🌈 JAAO Creative Studio</h1>", unsafe_allow_html=True)

# --- แถบด้านข้าง (Sidebar) ---
with st.sidebar:
    st.title("📜 ประวัติการสร้าง")
    if st.button("ล้างประวัติ"):
        st.session_state.history = []
        st.rerun()
    st.write("---")
    for item in reversed(st.session_state.history):
        with st.expander(f"📌 {item['time']} - {item['type']}"):
            st.write(item['result'])

# --- ส่วนปุ่มลัด (Quick Prompts) ---
st.write("✨ **เลือกตัวอย่างคำสั่ง:**")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🎵 เพลงลูกทุ่ง"):
        st.session_state.input_text = "แต่งเพลงลูกทุ่งร่วมสมัย หนุ่มโรงงานอกหัก ขอจังหวะสนุกๆ"
        st.rerun()
with c2:
    if st.button("📷 ภาพ Portrait"):
        st.session_state.input_text = "Prompt: Thai woman, silk dress, sunlit garden, 8k, bokeh"
        st.rerun()
with c3:
    if st.button("🎤 เพลงแร็ป"):
        st.session_state.input_text = "เขียนไรม์แร็ปเล่าชีวิตคนทำ AI ชื่อ JAAO ขอแบบดุดัน"
        st.rerun()

# --- ส่วนรับข้อมูล ---
option = st.selectbox('🎨 เลือกโหมด:', ('🎵 แต่งเนื้อเพลง', '📷 พร้อมถ่ายภาพบุคคล', '📹 สคริปต์วิดีโอ'))
user_input = st.text_area("รายละเอียดงานของคุณ:", value=st.session_state.input_text, height=150)

# 4. ปุ่มรันงาน
st.markdown('<div class="main-button">', unsafe_allow_html=True)
if st.button("เริ่มสร้างความปัง ✨"):
    if user_input:
        with st.spinner("AI กำลังวิเคราะห์ข้อมูลเทคนิคให้คุณ..."):
            try:
                prompt_to_ai = f"""
                ในฐานะผู้เชี่ยวชาญด้าน {option} ช่วย {user_input} โดยแบ่งคำตอบเป็น 2 ส่วนชัดเจน:
                1. [RESULT]: เนื้อหาหลัก
                2. [SPECIAL_INFO]: ข้อมูลพิเศษ (Style/Tempo/Mood หรือ Lighting/Lens/Tips)
                ขอแบบมือโปรและ
