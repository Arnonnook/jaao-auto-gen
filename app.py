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
    div.stButton > button:first-child {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 15px;
        width: 100%;
        height: 55px;
        font-size: 18px;
        font-weight: bold;
    }
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
        1. **เลือกโหมด:** เลือกงานที่ต้องการ
        2. **ใส่รายละเอียด:** พิมพ์โจทย์ที่ต้องการ
        3. **กดปุ่มรัน:** รอ AI ประมวลผล
        4. **เช็คประวัติ:** ดูงานเก่าได้ที่นี่
        """)
    
    with st.expander("💡 เทคนิคการสั่ง (Prompt)"):
        st.write("""
        - **แต่งเพลง:** ระบุแนวเพลงและอารมณ์
        - **ภาพถ่าย:** ระบุ แสง, มุมกล้อง, ฉากหลัง
        """)
    
    st.write("---")
    st.title("📜 ประวัติการสร้าง")
    if st.button("ล้างประวัติ"):
        st.session_state.history = []
        st.rerun()
    
    for item in reversed(st.session_state.history):
        with st.expander(f"📌 {item['time']} - {item['type']}"):
            st.write(f"**โจทย์:** {item['prompt']}")
            st.info(item['result'])

# --- ส่วนปุ่มลัด (Quick Prompts) ---
st.write("✨ **กดเพื่อเลือกตัวอย่างคำสั่ง:**")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🎵 เพลงลูกทุ่ง", kind="secondary"):
        st.session_state.input_text = "แต่งเพลงลูกทุ่งร่วมสมัย หนุ่มโรงงานอกหัก ขอจังหวะสนุกๆ"
with c2:
    if st.button("📷 ภาพ Portrait", kind="secondary"):
        st.session_state.input_text = "Prompt: Thai woman, silk dress, sunlit garden, 8k, bokeh"
with c3:
    if st.button("🎤 เพลงแร็ป", kind="secondary"):
        st.session_state.input_text = "เขียนไรม์แร็ปเล่าชีวิตคนทำ AI ชื่อ JAAO ขอแบบดุดัน"

# --- ส่วนรับข้อมูล ---
option = st.selectbox('🎨 เลือกโหมด:', ('🎵 แต่งเนื้อเพลง', '📷 พร้อมถ่ายภาพบุคคล', '📹 สคริปต์วิดีโอ'))
# ใช้ key เพื่อให้การอัปเดตค่าจากปุ่มลัดทำงานสมบูรณ์
user_input = st.text_area("รายละเอียดงานของคุณ:", value=st.session_state.input_text, height=120)

# 4. ปุ่มรันงาน
if st.button("เริ่มสร้างความปัง ✨"):
    if user_input:
        with st.spinner("AI กำลังสร้างสรรค์งานให้คุณ..."):
            try:
                response = model.generate_content(f"ช่วย {user_input} ในฐานะ {option} ขอแบบเจ๋งๆ พร้อมอีโมจิ 🤩")
                st.balloons()
                st.success("สร้างเสร็จแล้ว! 🎉")
                st.info(response.text)
                
                # บันทึกประวัติ
                now = datetime.datetime.now().strftime("%H:%M")
                st.session_state.history.append({"type": option, "prompt": user_input, "result": response.text, "time": now})
                st.session_state.input_text = "" 
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณากรอกข้อมูลก่อนครับ")

st.write("---")
st.caption("Developed by JAAO | 2026 Edition")
