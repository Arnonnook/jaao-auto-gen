# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io
import time

# 1. ตั้งค่าหน้าเว็บให้จ๊าบ
st.set_page_config(page_title="ARNON AI ULTIMATE", page_icon="🚀", layout="wide")

# --- ฟังก์ชันรีเซ็ตระบบ ---
def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- เชื่อมต่อ Gemini API ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ พี่อานนท์! อย่าลืมใส่ MY_API_KEY ในช่อง Secrets นะครับ")

# --- CSS สไตล์นีออน (บังคับโชว์ปุ่มยักษ์) ---
st.markdown("""
<style>
    header {visibility: hidden;} .stDeployButton {display:none;}
    footer {visibility: hidden;} #MainMenu {visibility: hidden;}
    .stApp { background-color: #000; color: #fff; }
    .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
    .card { background-color: #1a1a1a; padding: 25px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 20px; }
    
    /* ปุ่มแกะพรอพสีชมพู */
    .stButton>button[kind="primary"] {
        background-color: #ff00ff !important;
        color: white !important;
        height: 65px !important;
        font-size: 22px !important;
        border-radius: 15px !important;
    }
    
    /* ปุ่มเจนรูปยักษ์สีเขียวนีออน */
    .stButton>button[kind="secondary"] { 
        background-color: #00ffcc !important; 
        color: #000 !important; 
        border-radius: 20px !important; 
        height: 100px !important;
        font-size: 30px !important;
        font-weight: 900 !important;
        box-shadow: 0 0 30px #00ffcc !important;
    }
    label { color: #00ffcc !important; font-size: 18px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🚀 ARNON AI ULTIMATE v.9.9</h1>', unsafe_allow_html=True)

# ปุ่มรีเซ็ตด่วน
col_a, col_b = st.columns([4, 1])
with col_b:
    if st.button("🔄 ล้างระบบค้าง"): reset_app()

tab1, tab2 = st.tabs(["💰 คิดเงินเดือน", "📸 แกะพรอพ & เจนรูปยักษ์"])

# --- TAB 1: ระบบคิดเงินเดือน ---
with tab1:
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        daily_rate = st.number_input("ค่าแรงต่อวัน (฿):", value=350)
        total_days = st.number_input("วันทำงานในเดือน:", value=26)
        leave_dates = st.multiselect("วันที่ลา:", options=[d for d in range(1, 32)])
        actual_days = total_days - len(leave_dates)
        c1, c2 = st.columns(2)
        with c1: inc1 = st.checkbox("วิกแรก ✅", value=True)
        with c2: inc2 = st.checkbox("วิกสอง ✅", value=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # คำนวณเงิน (แบบย่อเพื่อประหยัดพื้นที่)
    total_base = daily_rate * total_days
    total_inc = (350 if inc1 else 0) + (350 if inc2 else 0)
    gross = total_base + total_inc + ((50+60) * actual_days)
    sso = int(gross * 0.04) if gross * 0.04 < 750 else 750
    net = gross - sso

    with col_r:
        st.markdown(f'<div class="card" style="text-align:center;"><h2>ยอดโอนสุทธิ</h2><h1 style="font-size:60px; color:#00ffcc;">฿ {net:,.2f}</h1></div>', unsafe_allow_html=True)

# --- TAB 2: ระบบแกะพรอพ & เจนรูป ---
with tab2:
    # --- ส่วนที่ 1: แกะพรอพ ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1️⃣ อัปโหลดรูปเพื่อแกะพรอพ")
    
    up_file = st.file_uploader("เลือกรูปภาพจากมือถือพี่:", type=["png", "jpg", "jpeg"])
    
    if up_file:
        st.image(up_file, width=250, caption="รูปที่พี่เลือก")

    if st.button("🔍 สั่ง AI แกะพรอพเดี๋ยวนี้!", type="primary", use_container_width=True):
        if up_file:
            with st.status("🚀 กำลังทำงาน...", expanded=True) as status:
                st.write("📡 ย่อขนาดรูปเพื่อความเร็ว...")
                img = Image.open(up_file)
                img.thumbnail((600, 600))
                
                st.write("🤖 ส่งให้ Gemini วิเคราะห์...")
                model = genai.GenerativeModel('gemini-2.5-flash')
                try:
                    resp = model.generate_content(["Describe this for AI image prompt. Text only.", img])
                    st.session_state["p_final"] = resp.text
                    status.update(label="✅ แกะเสร็จแล้ว!", state="complete")
                except Exception as e:
                    st.error(f"ผิดพลาด: {e}")
        else:
            st.error("❌ พี่ต้องเลือกรูปก่อนครับ!")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนที่ 2: เจนรูปใหม่ ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2️⃣ ตรวจสอบและสร้างรูปใหม่")
    
    p_now = st.session_state.get("p_final", "")
    final_text = st.text_area("พรอพ (แก้ไขได้ตามใจพี่):", value=p_now, height=150)
    
    if st.button("🚀 สั่งเจนรูปใหม่ยักษ์!", type="secondary", use_container_width=True):
        if final_text:
            with st.spinner('🎨 กำลังวาดรูปใหม่...'):
                clean_p = final_text.replace(" ", "%20").replace("\n", "%20")
                # ใช้โมเดลคุณภาพสูง Flux
                gen_url = f"https://pollinations.ai/p/{clean_p}?width=1024&height=1024&seed={int(time.time())}&model=flux"
                st.image(gen_url, caption="✨ รูปใหม่ของพี่อานนท์", use_container_width=True)
                st.success("จ๊าบมากครับพี่!")
        else:
            st.error("❌ ยังไม่มีพรอพครับ!")
    st.markdown('</div>', unsafe_allow_html=True)
