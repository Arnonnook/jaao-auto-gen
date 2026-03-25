import streamlit as st
from groq import Groq
import datetime
import time
import random

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO MUSE v.8.2", page_icon="🌐", layout="wide")

# ระบบเก็บข้อมูลใน Session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# --- การตกแต่งด้วย CSS (เน้นปุ่ม Chrome สีสันสดใส) ---
st.markdown("""
<style>
    .stApp { background-color: #0b0d11; color: #ffffff; }
    .app-title {
        color: #ff4b4b !important;
        text-align: center;
        font-size: 40px !important;
        font-weight: 900 !important;
    }
    /* ปุ่มรันหลัก */
    div.stButton > button:first-child {
        background-color: #ff4b4b !important;
        color: white !important;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
    }
    /* ปุ่มเปิด Chrome สไตล์ Suno + Chrome */
    .suno-chrome-btn {
        display: block;
        width: 100%;
        padding: 20px;
        background: linear-gradient(90deg, #4285F4, #34A853, #FBBC05, #EA4335);
        color: white !important;
        text-decoration: none;
        border-radius: 15px;
        font-weight: bold;
        text-align: center;
        font-size: 22px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: 0.3s;
    }
    .suno-chrome-btn:hover {
        transform: scale(1.02);
        filter: brightness(1.1);
    }
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อสมองกล Groq (หรือ Gemini)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ กรุณาเช็ค GROQ_API_KEY ใน Secrets ครับ")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="app-title">🌐 JAAO CHROME STUDIO v.8.2</h1>', unsafe_allow_html=True)

col_input, col_output = st.columns([1, 1])

with col_input:
    st.write("✨ **กดเลือกโหมดด่วน:**")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🎵 ลูกทุ่ง"): st.session_state.input_text = "แต่งเพลงลูกทุ่ง อกหักซึ้งๆ"; st.rerun()
    with c2:
        if st.button("🎸 ร็อก"): st.session_state.input_text = "แต่งเพลงร็อก สู้ชีวิต"; st.rerun()
    with c3:
        if st.button("🎤 ป็อป"): st.session_state.input_text = "เพลงป็อปใสๆ แอบรักเพื่อน"; st.rerun()

    user_input = st.text_area("รายละเอียดเนื้อเพลง:", value=st.session_state.input_text, height=150)
    
    # ปุ่มรัน AI
    run_btn = st.button("🔥 เริ่มแต่งเพลง (RUN)")

with col_output:
    if run_btn:
        if user_input:
            with st.spinner("🚀 กำลังแต่งเพลงด้วยความเร็วสูง..."):
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "คุณคือโปรดิวเซอร์เพลงมืออาชีพ แต่งเนื้อเพลงภาษาไทยตามโจทย์ แยก [RESULT] และ [SPECIAL_INFO]"},
                            {"role": "user", "content": user_input}
                        ],
                    )
                    full_text = completion.choices[0].message.content
                    
                    if "[SPECIAL_INFO]" in full_text:
                        parts = full_text.split("[SPECIAL_INFO]")
                        res_part = parts[0].replace("[RESULT]", "").strip()
                        st.info(res_part)
                        st.code(res_part, language="text") # ให้พี่กด Copy ตรงนี้
                    else:
                        st.info(full_text)
                        st.code(full_text, language="text")

                    st.success("สำเร็จ! 1.กด Copy ด้านบน 2.กดปุ่มเปิด Chrome ด้านล่างครับ")
                    
                    # --- ปุ่มเปิด Chrome ไปหน้า Suno ทันที ---
                    # สำหรับ Android/iOS: ใช้ googlechromes:// เพื่อบังคับเปิดแอป Chrome
                    # สำหรับคอม: ใช้ https:// ปกติแต่จะเปิดใน Browser หลัก
                    st.markdown('<a href="googlechromes://suno.com/create" target="_blank" class="suno-chrome-btn">🚀 เปิด SUNO ใน CHROME</a>', unsafe_allow_html=True)
                    st.markdown('<small style="color:#888;">*หากบนคอมไม่เด้ง ให้ใช้ปุ่มสำรองด้านล่าง</small>', unsafe_allow_html=True)
                    st.markdown('<a href="https://suno.com/create" target="_blank" style="color:#4285F4;">🔗 ลิงก์สำรอง (สำหรับคอมพิวเตอร์)</a>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาใส่รายละเอียดก่อนครับ")
