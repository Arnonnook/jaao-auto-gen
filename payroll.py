# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON AI ULTIMATE", page_icon="🚀", layout="wide")

# --- ฟังก์ชันล้างค่า (ถ้าค้างให้กดปุ่มนี้) ---
def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# --- ดึง API Key จาก Secrets ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ อย่าลืมใส่ MY_API_KEY ใน Secrets นะครับ!")

# --- CSS สไตล์นีออน (ปรับปรุงให้เห็นสถานะชัดๆ) ---
st.markdown("""
<style>
    header {visibility: hidden;} .stDeployButton {display:none;}
    footer {visibility: hidden;} #MainMenu {visibility: hidden;}
    .stApp { background-color: #000; color: #fff; }
    .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
    .card { background-color: #1a1a1a; padding: 25px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 20px; }
    
    /* ปุ่มชมพู */
    .stButton>button[kind="primary"] { background-color: #ff00ff !important; color: white !important; height: 60px !important; font-size: 20px !important; }
    
    /* ปุ่มเขียวยักษ์ */
    .stButton>button[kind="secondary"] { background-color: #00ffcc !important; color: #000 !important; height: 90px !important; font-size: 28px !important; font-weight: 900 !important; }
    
    /* ปุ่มรีเซ็ต */
    .reset-btn button { background-color: #444 !important; color: #ccc !important; height: 40px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🚀 ARNON AI ULTIMATE v.9.9</h1>', unsafe_allow_html=True)

# ปุ่มรีเซ็ตกรณีค้าง
col_r1, col_r2 = st.columns([4, 1])
with col_r2:
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("🔄 ล้างระบบ (ถ้าค้าง)"): reset_app()
    st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💰 คิดเงินเดือน", "📸 แกะพรอพ & เจนรูป"])

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1️⃣ อัปโหลดรูปภาพ")
    
    up_file = st.file_uploader("เลือกรูปภาพ:", type=["png", "jpg", "jpeg"], key="ultimate_up")
    
    if up_file:
        st.success(f"✔️ ไฟล์ {up_file.name} พร้อมแกะ!")
        st.image(Image.open(up_file), width=200)

    # ปุ่มแกะพรอพ
    if st.button("🔍 สั่ง AI แกะพรอพทันที", type="primary", use_container_width=True):
        if up_file:
            # ใช้ st.empty เพื่อแสดงข้อความที่เปลี่ยนไปเรื่อยๆ จะได้รู้ว่าไม่ค้าง
            status_msg = st.empty()
            try:
                status_msg.info("⏳ กำลังย่อรูปให้เล็กลง...")
                img = Image.open(up_file)
                img.thumbnail((500, 500)) # ย่อให้เล็กสุดๆ เพื่อความไว
                
                status_msg.warning("📡 กำลังส่งให้ Gemini (รอประมาณ 10 วิ)...")
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # ส่งคำสั่งแบบเน้นผลลัพธ์สั้นๆ เพื่อไม่ให้ค้าง
                response = model.generate_content(["What is in this image? Provide a short prompt for AI art.", img])
                
                if response and response.text:
                    st.session_state["p_final"] = response.text
                    status_msg.success("✅ แกะสำเร็จ! เลื่อนลงไปดูข้างล่างครับ")
                else:
                    status_msg.error("❌ AI ไม่ยอมตอบ! ลองกด 'ล้างระบบ' แล้วทำใหม่ครับ")
            except Exception as e:
                status_msg.error(f"❌ ระบบค้าง/ผิดพลาด: {str(e)}")
        else:
            st.error("❌ เลือกรูปก่อนครับพี่!")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนที่ 2: เจนรูป ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2️⃣ สร้างรูปใหม่")
    
    p_val = st.session_state.get("p_final", "")
    final_p = st.text_area("พรอพ (ตรวจสอบที่นี่):", value=p_val, height=120)
    
    if st.button("🚀 สั่งเจนรูปใหม่ยักษ์!", type="secondary", use_container_width=True):
        if final_p:
            with st.spinner('🎨 กำลังวาด...'):
                clean_p = final_p.replace(" ", "%20").replace("\n", "%20")
                # เพิ่ม timestamp ป้องกันการจำรูปเก่า
                gen_url = f"https://pollinations.ai/p/{clean_p}?width=1024&height=1024&seed={int(time.time())}&model=flux"
                st.image(gen_url, caption="✨ รูปใหม่ล่าสุด", use_container_width=True)
        else:
            st.error("❌ ยังไม่มีพรอพครับ!")
    st.markdown('</div>', unsafe_allow_html=True)
