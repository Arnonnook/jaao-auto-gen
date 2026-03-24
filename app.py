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

# --- การตกแต่งด้วย CSS (ปรับให้ปลอดภัยขึ้น) ---
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
        height: 55px;
        font-size: 18px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 2. ดึง Key จาก Secrets
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("⚠️ ไม่พบ API Key ใน Secrets!")
    st.stop()

# 3. ส่วนแสดงผลหลัก
st.markdown("<h1>🌈 JAAO Creative Studio</h1>", unsafe_allow_html=True)

# --- แถบด้านข้าง (Sidebar) ---
with st.sidebar:
    st.title("📖 คู่มือ & ประวัติ")
    with st.expander("📝 วิธีใช้งาน"):
        st.write("1. กดปุ่มตัวอย่าง หรือพิมพ์เอง\n2. เลือกโหมด\n3. กดปุ่มรันด้านล่าง")
    
    st.write("---")
    if st.button("ล้างประวัติ"):
        st.session_state.history = []
        st.rerun()
    
    for item in reversed(st.session_state.history):
        with st.expander(f"📌 {item['time']} - {item['type']}"):
            st.write(item['result'])

# --- ส่วนปุ่มลัด (Quick Prompts) - ตัด kind="secondary" ออกเพื่อแก้ Error ---
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

# ช่องพิมพ์ข้อความ
user_input = st.text_area("รายละเอียดงานของคุณ:", value=st.session_state.input_text, height=150)

# 4. ปุ่มรันงาน (ใส่ Class เพื่อตกแต่ง)
st.markdown('<div class="main-button">', unsafe_allow_html=True)
if st.button("เริ่มสร้างความปัง ✨"):
    if user_input:
        with st.spinner("AI กำลังสร้างสรรค์งาน..."):
            try:
                response = model.generate_content(f"ช่วย {user_input} ในฐานะ {option} ขอแบบเจ๋งๆ พร้อมอีโมจิ")
                st.balloons()
                st.success("สร้างเสร็จแล้ว! 🎉")
                st.info(response.text)
                
                # บันทึกประวัติ
                now = datetime.datetime.now().strftime("%H:%M")
                st.session_state.history.append({"type": option, "result": response.text, "time": now})
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณากรอกข้อมูลก่อนครับ")
st.markdown('</div>', unsafe_allow_html=True)

st.caption("Developed by JAAO | 2026")
