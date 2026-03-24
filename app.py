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

# --- การตกแต่งด้วย CSS (เน้นชื่อแอปสีแดงชัดเจน) ---
st.markdown("""
<style>
    .stApp { background-color: #fdfcf5; }
    
    /* แก้ไขชื่อแอปให้เป็นสีแดงสดและตัวหนาพิเศษ */
    .app-title {
        color: #e63946 !important; /* สีแดงเข้มสด */
        text-align: center;
        font-size: 42px !important;
        font-weight: 900 !important;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1); /* เพิ่มเงาบางๆ ให้ดูมีมิติ */
    }
    
    .main-button > div > button {
        background-color: #e63946 !important;
        color: white !important;
        border-radius: 15px;
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
    }
    
    .special-info {
        background-color: #2d3436;
        color: #ffffff !important;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #fab005;
        margin-top: 15px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# 2. ดึง Key จาก Secrets
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key ใน Secrets!")
    st.stop()

# 3. หน้าจอหลัก (ใช้ Class app-title ที่สร้างไว้)
st.markdown('<h1 class="app-title">🔴 JAAO Creative Studio</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.title("📜 ประวัติการสร้าง")
    if st.button("ล้างประวัติ"):
        st.session_state.history = []
        st.rerun()
    st.write("---")
    for item in reversed(st.session_state.history):
        with st.expander(f"📌 {item['time']} - {item['type']}"):
            st.write(item['result'])

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

option = st.selectbox('🎨 เลือกโหมด:', ('🎵 แต่งเนื้อเพลง', '📷 พร้อมถ่ายภาพบุคคล', '📹 สคริปต์วิดีโอ'))
user_input = st.text_area("รายละเอียดงานของคุณ:", value=st.session_state.input_text, height=150)

# 4. ปุ่มรันงาน
st.markdown('<div class="main-button">', unsafe_allow_html=True)
if st.button("เริ่มสร้างความปัง ✨"):
    if user_input:
        with st.spinner("AI กำลังวิเคราะห์ข้อมูลเทคนิคให้คุณ..."):
            try:
                prompt_to_ai = f"ในฐานะผู้เชี่ยวชาญด้าน {option} ช่วย {user_input} โดยแบ่งคำตอบเป็น 2 ส่วนคือ [RESULT]: เนื้อหาหลัก และ [SPECIAL_INFO]: ข้อมูลพิเศษเชิงเทคนิค สไตล์ อารมณ์ หรือการจัดแสง"
                
                response = model.generate_content(prompt_to_ai)
                full_text = response.text
                
                if "[SPECIAL_INFO]" in full_text:
                    parts = full_text.split("[SPECIAL_INFO]")
                    main_result = parts[0].replace("[RESULT]", "").strip()
                    special_info = parts[1].strip()
                else:
                    main_result = full_text
                    special_info = "AI ไม่ได้ระบุข้อมูลพิเศษในครั้งนี้"

                st.balloons()
                st.success("สร้างเสร็จแล้ว! 🎉")
                st.markdown("### 📝 ผลลัพธ์หลัก:")
                st.info(main_result)
                st.markdown("### 💡 ข้อมูลพิเศษ & เทคนิคเพิ่มเติม:")
                st.markdown(f'<div class="special-info">{special_info}</div>', unsafe_allow_html=True)
                
                now = datetime.datetime.now().strftime("%H:%M")
                st.session_state.history.append({"type": option, "result": full_text, "time": now})
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณากรอกข้อมูลก่อนครับ")
st.markdown('</div>', unsafe_allow_html=True)
