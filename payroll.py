# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON AI FIX", page_icon="🛠️", layout="wide")

# --- ดึง API Key จาก Secrets ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ อย่าลืมใส่ MY_API_KEY ใน Secrets บนเว็บ Streamlit นะครับ!")

# --- CSS บังคับโชว์ปุ่มให้ใหญ่และชัดเจน ---
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
        height: 60px !important;
        font-size: 20px !important;
        border-radius: 15px !important;
    }
    
    /* ปุ่มเจนรูปยักษ์สีเขียวนีออน */
    .stButton>button[kind="secondary"] { 
        background-color: #00ffcc !important; 
        color: #000 !important; 
        border-radius: 20px !important; 
        height: 100px !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        box-shadow: 0 0 25px #00ffcc !important;
        margin-top: 10px;
    }
    label { color: #00ffcc !important; font-size: 18px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🛠 ARNON AI FIXED v.9.5</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💰 คิดเงินเดือน", "📸 ระบบแกะพรอพ & เจนรูป"])

with tab2:
    # --- ส่วนที่ 1: อัปโหลดและแกะพรอพ ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1️⃣ ขั้นตอนการแกะพรอพ")
    
    up_file = st.file_uploader("เลือกรูปจากมือถือพี่ตรงนี้:", type=["png", "jpg", "jpeg"])
    
    if up_file:
        st.image(up_file, width=200, caption="รูปที่เลือก")

    # ปุ่มแกะพรอพ (ใช้สีชมพู)
    if st.button("🔍 กดเพื่อสั่ง AI แกะพรอพจากรูป", type="primary", use_container_width=True):
        if up_file:
            with st.spinner('🚀 กำลังแกะ...'):
                img = Image.open(up_file)
                img.thumbnail((800, 800)) # ย่อรูปให้เร็ว
                model = genai.GenerativeModel('gemini-1.5-flash')
                resp = model.generate_content(["Describe this image briefly for AI prompt. Text only.", img])
                st.session_state["arnon_p"] = resp.text
                st.success("✅ แกะเสร็จแล้ว! คำจะโผล่ในช่องข้างล่างครับ")
        else:
            st.error("❌ พี่ต้องเลือกรูปก่อนกดปุ่มนี้นะครับ!")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนที่ 2: ตรวจสอบและเจนรูป ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2️⃣ ขั้นตอนการสร้างรูปใหม่")
    
    # ช่องใส่พรอพ (จะโชว์พรอพที่แกะได้ หรือพิมพ์เองก็ได้)
    saved_p = st.session_state.get("arnon_p", "")
    final_text = st.text_area("พรอพสำหรับเจนรูป (แก้ไขได้):", value=saved_p, height=150)
    
    # ปุ่มเจนรูปยักษ์ (ใช้สีเขียว)
    if st.button("🚀 สั่งเจนรูปใหม่ทันที!", type="secondary", use_container_width=True):
        if final_text:
            with st.spinner('🎨 กำลังวาดรูปใหม่...'):
                clean_p = final_text.replace(" ", "%20").replace("\n", "%20")
                # ส่งไปเจนรูป
                gen_url = f"https://pollinations.ai/p/{clean_p}?width=1024&height=1024&seed=99&model=flux"
                st.image(gen_url, caption="✨ รูปใหม่ของพี่อานนท์", use_container_width=True)
        else:
            st.error("❌ พี่ต้องมีพรอพก่อน (แกะจากรูปด้านบนหรือพิมพ์เองก็ได้)")
    st.markdown('</div>', unsafe_allow_html=True)
