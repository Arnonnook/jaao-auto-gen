import streamlit as st
import google.generativeai as genai
import datetime
import time
import random # เพิ่มไลบรารีสำหรับสุ่ม

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Creative Studio v.7", page_icon="🔴", layout="centered")

# ระบบเก็บข้อมูลใน Session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# --- 🎨 คลังพร้อมท์สำหรับสุ่ม (เพิ่ม/แก้ไข ตรงนี้ได้เลย) ---
PROMPT_LIBRARY = [
    "A majestic Thai dragon flying over Wat Arun at sunset, hyper-realistic, 8k, golden hour lighting",
    "Cyberpunk Bangkok 2077 style, neon lights, rain on the street, Tuk Tuk flying, cinematic lighting",
    "Cute 3D baby elephant wearing a traditional Thai hat, Pixar style, soft lighting, vibrant colors",
    "Futuristic Thai kitchen with a robot chef cooking Pad Thai, high-tech, clean aesthetic, 4k",
    "Portrait of a beautiful Thai woman in traditional silk, floating in a galaxy of stars, ethereal, dreamlike",
    "Retro 80s synthwave style of a beach in Southern Thailand, purple and pink neon, VHS effect",
    "Steampunk version of a traditional Thai long-tail boat, brass and steam details, river background"
]

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #fdfcf5; }
    .app-title { color: #e63946 !important; text-align: center; font-size: 45px !important; font-weight: 900 !important; }
    .app-version { color: #555; text-align: center; font-size: 16px; margin-bottom: 20px; }
    
    /* ปุ่มรันสีแดง */
    div.stButton > button:first-child {
        background-color: #e63946 !important; color: white !important;
        height: 60px; font-size: 20px; font-weight: bold; border-radius: 15px; width: 100%;
    }
    
    /* ปุ่มสุ่มสีเหลืองทอง */
    .random-btn > div > button {
        background-color: #fab005 !important; color: #2d3436 !important;
        font-weight: bold; border-radius: 10px; border: none;
    }
    
    .special-info { background-color: #2d3436; color: #ffffff !important; padding: 20px; border-radius: 12px; border-left: 8px solid #fab005; margin-top: 15px; }
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

# 3. หน้าจอหลัก
st.markdown('<h1 class="app-title">🔴 JAAO Creative Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-version">Version 7.6 | Random Prompt Edition</p>', unsafe_allow_html=True)

with st.sidebar:
    st.title("📜 ประวัติ")
    if st.button("🗑️ ล้างประวัติ"):
        st.session_state.history = []
        st.rerun()
    for item in reversed(st.session_state.history):
        with st.expander(f"📌 {item['time']}"):
            st.write(item['result'])

# --- ส่วนสุ่มพร้อมท์ด่วน ---
st.write("🎲 **นึกไม่ออก? ลองสุ่มดูครับ:**")
st.markdown('<div class="random-btn">', unsafe_allow_html=True)
if st.button("✨ สุ่มพร้อมท์สร้างรูป"):
    st.session_state.input_text = random.choice(PROMPT_LIBRARY)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- ปุ่มลัดเลือกสไตล์หลัก ---
st.write("🎵 **สไตล์เพลงยอดฮิต:**")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("🎵ลูกทุ่ง"): st.session_state.input_text = "แต่งเพลงลูกทุ่งร่วมสมัย หนุ่มโรงงานอกหัก"; st.rerun()
with c2:
    if st.button("🎸ร็อก"): st.session_state.input_text = "แต่งเพลงร็อกดุดัน สู้ชีวิตไม่ยอมแพ้"; st.rerun()
with c3:
    if st.button("🎤ป็อป"): st.session_state.input_text = "แต่งเพลงป็อปใสๆ แอบรักเพื่อนสนิท"; st.rerun()
with c4:
    if st.button("🔥แร็ป"): st.session_state.input_text = "เขียนไรม์แร็ปดุดัน เล่าความสำเร็จของ JAAO AI"; st.rerun()

# --- ส่วนรับข้อมูล ---
st.write("---")
option = st.selectbox('🎨 เลือกประเภทงาน:', ('📷 พร้อมถ่ายภาพบุคคล', '🎵 แต่งเนื้อเพลง', '📹 สคริปต์วิดีโอ'))
user_input = st.text_area("รายละเอียดงาน (หรือข้อความที่สุ่มมา):", value=st.session_state.input_text, height=120)

status_placeholder = st.empty()
progress_placeholder = st.empty()

# 4. ปุ่มรันงาน
if st.button("🚀 เริ่มสร้างความปัง (RUN)"):
    if user_input:
        progress_bar = progress_placeholder.progress(0)
        messages = ["🔍 วิเคราะห์โจทย์...", "🧠 AI กำลังใช้ความคิด...", "✍️ เรียบเรียงเนื้อหา...", "✨ เพิ่มเทคนิคพิเศษ..."]
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            if i % 25 == 0: status_placeholder.warning(f"สถานะ: {messages[i//25]}")
        
        try:
            prompt_to_ai = f"ช่วย {user_input} ในฐานะ {option} โดยแยกเป็น [RESULT]: เนื้อหาหลัก และ [SPECIAL_INFO]: ข้อมูลเทคนิค สไตล์ อารมณ์ หรือการจัดแสง"
            response = model.generate_content(prompt_to_ai)
            
            status_placeholder.empty()
            progress_placeholder.empty()
            
            st.balloons()
            st.success("เสร็จเรียบร้อย! 🎉")
            
            full_text = response.text
            if "[SPECIAL_INFO]" in full_text:
                parts = full_text.split("[SPECIAL_INFO]")
                res_part = parts[0].replace("[RESULT]", "").strip()
                spec_part = parts[1].strip()
                st.markdown("### 📝 ผลลัพธ์หลัก:")
                st.info(res_part)
                st.markdown("### 💡 ข้อมูลพิเศษ & เทคนิคเพิ่มเติม:")
                st.markdown(f'<div class="special-info">{spec_part}</div>', unsafe_allow_html=True)
            else:
                st.info(full_text)
            
            st.session_state.history.append({"time": datetime.datetime.now().strftime("%H:%M"), "result": full_text})
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
            status_placeholder.empty()
            progress_placeholder.empty()
    else:
        st.warning("กรุณาใส่รายละเอียดงานก่อนนะครับ")

st.caption("© 2026 JAAO Creative Studio v.7.6")
