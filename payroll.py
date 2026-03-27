# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON Payroll & AI", page_icon="🎨", layout="wide")

# --- ดึง API Key จาก Secrets ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ อย่าลืมใส่ MY_API_KEY ใน Secrets บน Streamlit Cloud นะครับ!")

# --- CSS ปรับปรุงปุ่มให้โชว์เด่นชัด ---
st.markdown("""
<style>
    header {visibility: hidden;} .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #000; color: #fff; }
    .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
    .card { background-color: #1a1a1a; padding: 20px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 15px; }
    
    /* ปุ่มเจนรูปยักษ์สีเขียวนีออน */
    .stButton>button { 
        background-color: #00ffcc !important; 
        color: #000 !important; 
        border-radius: 20px !important; 
        height: 80px !important;
        font-size: 25px !important;
        font-weight: 900 !important;
        box-shadow: 0 0 20px #00ffcc !important;
        margin-top: 20px;
    }
    
    /* ปุ่มแกะพรอพสีชมพู */
    .pink-button button {
        background-color: #ff00ff !important;
        color: white !important;
        height: 60px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🎨 ARNON AI v.9.3</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💰 คิดเงินเดือน", "📸 แกะพรอพ & เจนรูป"])

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📸 STEP 1: แกะพรอพ")
    
    img_size = st.selectbox("ขนาดรูปที่จะเจนใหม่:", ["1024x1024", "1920x1080", "1080x1920"])
    uploaded_file = st.file_uploader("อัปโหลดรูปตรงนี้:", type=["png", "jpg", "jpeg"])
    
    # ปุ่มแกะพรอพ (โชว์ตลอดเวลา)
    st.markdown('<div class="pink-button">', unsafe_allow_html=True)
    btn_analyze = st.button("🔍 1. สั่ง AI แกะพรอพจากรูป")
    st.markdown('</div>', unsafe_allow_html=True)

    if btn_analyze:
        if uploaded_file:
            img_input = Image.open(uploaded_file)
            st.image(img_input, width=250)
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner('กำลังแกะพรอพ...'):
                resp = model.generate_content(["Describe this image for AI art generation. Text only.", img_input])
                st.session_state["p_extracted"] = resp.text
        else:
            st.warning("พี่ต้องอัปโหลดรูปก่อนกดแกะพรอพนะ!")

    st.write("---")
    st.subheader("📝 STEP 2: เจนรูปใหม่")
    
    # ดึงค่าพรอพที่แกะได้ หรือให้พี่พิมพ์เอง
    current_p = st.session_state.get("p_extracted", "")
    final_p = st.text_area("พรอพ (พิมพ์เองหรือแก้ที่ AI แกะมาได้):", value=current_p, height=150)
    
    # ปุ่มเจนรูปใหญ่ยักษ์ (โชว์ตลอดเวลา)
    if st.button("🚀 2. สั่งเจนรูปใหม่ทันที!"):
        if final_p:
            with st.spinner('กำลังเจนรูปสุดจ๊าบ...'):
                encoded_p = final_p.replace(" ", "%20")
                w, h = (1024, 1024)
                if "1920x1080" in img_size: w, h = (1920, 1080)
                if "1080x1920" in img_size: w, h = (1080, 1920)
                
                gen_url = f"https://pollinations.ai/p/{encoded_p}?width={w}&height={h}&seed=42&model=flux"
                st.image(gen_url, use_container_width=True)
                st.success("จ๊าบมากครับพี่อานนท์!")
        else:
            st.error("พี่ต้องใส่พรอพก่อนนะถึงจะเจนได้!")
    st.markdown('</div>', unsafe_allow_html=True)
