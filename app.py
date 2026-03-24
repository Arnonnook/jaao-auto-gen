import streamlit as st
import google.generativeai as genai
import datetime
import time
import random

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO MUSE STUDIO v.7.8", page_icon="🔴", layout="wide")

# ระบบเก็บข้อมูลใน Session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# --- การตกแต่งด้วย CSS (Dark Mode & Copy Button Style) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .app-title {
        color: #ff4b4b !important;
        text-align: center;
        font-size: 50px !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(255, 75, 75, 0.5);
    }
    .song-card {
        background-color: #1a1c24;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #333;
        margin-bottom: 10px;
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
    /* ปุ่มลิงก์ Suno (สีม่วงฟ้าแบบ Suno) */
    .suno-link {
        display: inline-block;
        padding: 10px 20px;
        background-color: #2b2d42;
        color: #00f2ff !important;
        text-decoration: none;
        border-radius: 10px;
        font-weight: bold;
        border: 1px solid #00f2ff;
        margin-top: 10px;
        text-align: center;
    }
    .special-box {
        background-color: #262730;
        color: #ffda5f;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffda5f;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. ดึง Key จาก Secrets
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key ใน Secrets!")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="app-title">🔴 JAAO MUSE STUDIO</h1>', unsafe_allow_html=True)

col_input, col_history = st.columns([1.1, 0.9])

with col_input:
    st.subheader("🎨 สร้างสรรค์ผลงาน")
    
    # ปุ่มลัด
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🎵 ลูกทุ่ง"): st.session_state.input_text = "แต่งเนื้อเพลงลูกทุ่งร่วมสมัย หนุ่มโรงงานอกหัก"; st.rerun()
    with c2:
        if st.button("🎸 ร็อก"): st.session_state.input_text = "แต่งเพลงร็อกดุดัน ปลุกใจสู้ชีวิต"; st.rerun()
    with c3:
        if st.button("🎤 ป็อป"): st.session_state.input_text = "เพลงป็อปฟังสบาย แอบรักคนในออฟฟิศ"; st.rerun()
    with c4:
        if st.button("🎲 สุ่มรูป"): 
            st.session_state.input_text = random.choice(["Cyberpunk Bangkok 8k", "Thai Dragon over Temple", "Retro Beach House"])
            st.rerun()

    option = st.selectbox('ประเภทงาน:', ('🎵 แต่งเนื้อเพลง', '📷 พร้อมท์ภาพ Portrait', '📹 สคริปต์วิดีโอ'))
    user_input = st.text_area("รายละเอียด:", value=st.session_state.input_text, height=130)
    
    status_p = st.empty()
    progress_p = st.empty()

    if st.button("🚀 เริ่มสร้างความปัง (RUN)"):
        if user_input:
            progress_bar = progress_p.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
                if i % 25 == 0: status_p.warning("AI กำลังคิดงานระดับเทพให้คุณ...")
            
            try:
                # สั่ง AI แยกผลลัพธ์ชัดเจน
                prompt_to_ai = f"ช่วย {user_input} ในฐานะ {option} โดยแยกเป็น [RESULT]: เนื้อหาหลัก และ [SPECIAL_INFO]: เทคนิคเชิงลึก"
                response = model.generate_content(prompt_to_ai)
                full_text = response.text
                
                status_p.empty(); progress_p.empty(); st.balloons()
                
                # แยกเนื้อหา
                if "[SPECIAL_INFO]" in full_text:
                    parts = full_text.split("[SPECIAL_INFO]")
                    res_part = parts[0].replace("[RESULT]", "").strip()
                    spec_part = parts[1].strip()
                else:
                    res_part = full_text
                    spec_part = "ไม่มีข้อมูลเทคนิคเพิ่มเติม"

                st.success("สร้างเสร็จแล้ว! 🎉")
                
                # --- ส่วนแสดงผลลัพธ์หลัก ---
                st.markdown("### 📝 ผลลัพธ์หลัก:")
                st.info(res_part)
                
                # 📋 ปุ่มก๊อปปี้ (ใช้ st.code เพื่อให้กดก๊อปปี้ได้ง่ายที่สุด)
                st.write("คัดลอกไปใช้ต่อ:")
                st.code(res_part, language="text")

                # 💡 ข้อมูลพิเศษ
                st.markdown(f'<div class="special-box"><b>💡 ข้อมูลพิเศษ & เทคนิค:</b><br>{spec_part}</div>', unsafe_allow_html=True)
                
                # 🔗 ปุ่มทางลัดไป Suno
                if "เพลง" in option:
                    st.markdown('<a href="https://suno.com/create" target="_blank" class="suno-link">🔗 ไปสร้างเพลงต่อที่ Suno.com</a>', unsafe_allow_html=True)

                # บันทึกประวัติ
                st.session_state.history.append({
                    "time": datetime.datetime.now().strftime("%H:%M"),
                    "type": option,
                    "result": res_part
                })
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาใส่รายละเอียดก่อนนะครับ")

with col_history:
    st.subheader("📂 ผลงานที่เคยสร้าง")
    if not st.session_state.history:
        st.write("ยังไม่มีประวัติในขณะนี้")
    else:
        for item in reversed(st.session_state.history):
            with st.container():
                st.markdown(f"""
                <div class="song-card">
                    <small>🕒 {item['time']} | {item['type']}</small>
                    <div style="margin-top:5px; font-size:14px; color:#ccc;">{item['result'][:100]}...</div>
                </div>
                """, unsafe_allow_html=True)

st.caption("© 2026 JAAO MUSE STUDIO | AI Creative Workflow")
