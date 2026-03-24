import streamlit as st
import google.generativeai as genai
import datetime
import time
import random

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Creative Studio v.7.7", page_icon="🔴", layout="wide")

# ระบบเก็บข้อมูลใน Session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# --- การตกแต่งด้วย CSS (แรงบันดาลใจจาก MuseGen: Dark Mode & Premium UI) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* หัวข้อแอปสีแดงสว่างบนพื้นดำ */
    .app-title {
        color: #ff4b4b !important;
        text-align: center;
        font-size: 50px !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(255, 75, 75, 0.5);
    }
    
    /* การ์ดผลงานแบบ MuseGen */
    .song-card {
        background-color: #1a1c24;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .song-card:hover { border-color: #ff4b4b; }
    
    /* ปุ่มรันสีแดงสด */
    div.stButton > button:first-child {
        background-color: #ff4b4b !important;
        color: white !important;
        height: 60px;
        font-size: 22px;
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
        border: none;
    }
    
    .special-box {
        background-color: #262730;
        color: #ffda5f;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffda5f;
    }
</style>
""", unsafe_allow_html=True)

# 2. ดึง Key จาก Secrets
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key! โปรดตั้งค่าใน Secrets")
    st.stop()

# 3. ส่วนหน้าจอหลัก (Layout แบ่งเป็น 2 ฝั่ง)
st.markdown('<h1 class="app-title">🔴 JAAO MUSE STUDIO</h1>', unsafe_allow_html=True)

col_input, col_history = st.columns([1.2, 0.8])

with col_input:
    st.subheader("🎨 สร้างสรรค์ผลงานใหม่")
    
    # ปุ่มลัดสไตล์ (แถวเดียว 5 ปุ่ม)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("🎵ลูกทุ่ง"): st.session_state.input_text = "แต่งเพลงลูกทุ่ง อกหักแต่โจ๊ะๆ"; st.rerun()
    with c2:
        if st.button("🎸ร็อก"): st.session_state.input_text = "เพลงร็อกสู้ชีวิต ดุดัน"; st.rerun()
    with c3:
        if st.button("🎤ป็อป"): st.session_state.input_text = "เพลงป็อปใสๆ แอบรักเพื่อน"; st.rerun()
    with c4:
        if st.button("🔥แแร็ป"): st.session_state.input_text = "แร็ปเล่าเรื่อง JAAO AI"; st.rerun()
    with c5:
        if st.button("🎲สุ่มรูป"): 
            st.session_state.input_text = random.choice(["Cyberpunk Bangkok", "Thai Dragon 8k", "Retro Thai Beach"])
            st.rerun()

    option = st.selectbox('โหมดการทำงาน:', ('🎵 แต่งเนื้อเพลง', '📷 สร้างพร้อมท์ภาพ Portrait', '📹 สคริปต์วิดีโอ'))
    user_input = st.text_area("อธิบายสิ่งที่ต้องการ:", value=st.session_state.input_text, height=150)
    
    status_p = st.empty()
    progress_p = st.empty()

    if st.button("🚀 เริ่มสร้างผลงาน (RUN)"):
        if user_input:
            progress_bar = progress_p.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
                if i % 25 == 0: status_p.warning("AI กำลังประมวลผล...")
            
            try:
                response = model.generate_content(f"ช่วย {user_input} ในฐานะ {option} แยก [RESULT] และ [SPECIAL_INFO]")
                full_text = response.text
                
                status_p.empty(); progress_p.empty(); st.balloons()
                
                # แสดงผล
                if "[SPECIAL_INFO]" in full_text:
                    parts = full_text.split("[SPECIAL_INFO]")
                    res = parts[0].replace("[RESULT]", "").strip()
                    spec = parts[1].strip()
                    st.info(res)
                    st.markdown(f'<div class="special-box">💡 <b>ข้อมูลเทคนิค:</b><br>{spec}</div>', unsafe_allow_html=True)
                else:
                    st.info(full_text)
                
                # บันทึกประวัติ
                st.session_state.history.append({
                    "time": datetime.datetime.now().strftime("%H:%M"),
                    "type": option,
                    "result": full_text
                })
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("ใส่รายละเอียดก่อนครับ")

with col_history:
    st.subheader("📂 ผลงานล่าสุด")
    if not st.session_state.history:
        st.write("ยังไม่มีประวัติการสร้าง")
    else:
        for item in reversed(st.session_state.history):
            with st.container():
                st.markdown(f"""
                <div class="song-card">
                    <small>🕒 {item['time']} | {item['type']}</small>
                    <p style="margin-top:10px;"><b>ผลงานชิ้นนี้ถูกบันทึกแล้ว</b></p>
                </div>
                """, unsafe_allow_html=True)
                # เพิ่มตัวเล่นเพลงจำลอง (สามารถเปลี่ยนลิงก์เป็นไฟล์จริงได้)
                if "เพลง" in item['type']:
                    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

st.write("---")
st.caption("Developed by JAAO | Inspired by AI Music SaaS UI")
