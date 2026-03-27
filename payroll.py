# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON AI COPY-SAFE", page_icon="📋", layout="wide")

# --- เชื่อมต่อ Gemini API ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ อย่าลืมใส่ MY_API_KEY ในช่อง Secrets นะครับ!")

# --- CSS สไตล์นีออน ---
st.markdown("""
<style>
    header {visibility: hidden;} .stDeployButton {display:none;}
    footer {visibility: hidden;} #MainMenu {visibility: hidden;}
    .stApp { background-color: #000; color: #fff; }
    .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
    .card { background-color: #1a1a1a; padding: 25px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 20px; }
    
    /* ปุ่มชมพู */
    .stButton>button[kind="primary"] {
        background-color: #ff00ff !important;
        color: white !important;
        height: 60px !important;
        font-size: 20px !important;
    }
    
    /* ปุ่มเขียวยักษ์ */
    .stButton>button[kind="secondary"] { 
        background-color: #00ffcc !important; 
        color: #000 !important; 
        height: 80px !important;
        font-size: 25px !important;
        font-weight: 900 !important;
        box-shadow: 0 0 20px #00ffcc !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📋 ARNON AI v.10.1</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💰 คิดเงินเดือน", "📸 แกะพรอพ & ก๊อปปี้"])

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1️⃣ อัปโหลดและแกะพรอพ")
    
    up_file = st.file_uploader("เลือกรูปภาพ:", type=["jpg", "jpeg", "png"], key="up_v101")
    
    if up_file:
        st.image(up_file, width=250)

    if st.button("🔍 สั่ง AI แกะพรอพ", type="primary", use_container_width=True):
        if up_file:
            with st.status("🚀 กำลังแกะพรอพ...", expanded=True):
                img = Image.open(up_file)
                img.thumbnail((600, 600))
                model = genai.GenerativeModel('gemini-1.5-flash')
                try:
                    resp = model.generate_content(["Describe this for AI image prompt. Text only.", img])
                    st.session_state["p_v101"] = resp.text
                except Exception as e:
                    st.error(f"ผิดพลาด: {e}")
        else:
            st.error("❌ เลือกรูปก่อนครับพี่!")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนที่ 2: ก๊อปปี้และเจนรูป ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2️⃣ ตรวจสอบและก๊อปปี้พรอพ")
    
    p_now = st.session_state.get("p_v101", "")
    
    if p_now:
        st.write("📋 **วิธีส่งออก:** พี่กดที่ปุ่มรูป 'กระดาษซ้อนกัน' ตรงมุมขวาของกล่องข้างล่างนี้ เพื่อก๊อปปี้ได้เลยครับ!")
        # ใช้ st.code เพราะมันมีปุ่ม Copy มาให้ในตัวเลย ชัวร์กว่า!
        st.code(p_now, language="text")
        
        st.write("---")
        st.write("✍️ **ถ้าอยากแก้พรอพก่อนเจนรูป:**")
        final_text = st.text_area("แก้ไขพรอพตรงนี้:", value=p_now, height=100)
        
        if st.button("🚀 สั่งเจนรูปใหม่ยักษ์!", type="secondary", use_container_width=True):
            with st.spinner('🎨 กำลังวาด...'):
                clean_p = final_text.replace(" ", "%20").replace("\n", "%20")
                gen_url = f"https://pollinations.ai/p/{clean_p}?width=1024&height=1024&seed={int(time.time())}&model=flux"
                st.image(gen_url, use_container_width=True)
    else:
        st.info("💡 แกะพรอพจากด้านบนก่อนครับ ปุ่มก๊อปปี้ถึงจะขึ้น")
    
    st.markdown('</div>', unsafe_allow_html=True)
