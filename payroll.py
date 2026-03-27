# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON AI FAST", page_icon="⚡", layout="wide")

# --- ดึง API Key จาก Secrets ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ อย่าลืมใส่ MY_API_KEY ใน Secrets นะ!")

# --- CSS ปรับปรุงปุ่มให้จ๊าบและตัวหนังสืออ่านง่าย ---
st.markdown("""
<style>
    header {visibility: hidden;} .stDeployButton {display:none;}
    footer {visibility: hidden;} #MainMenu {visibility: hidden;}
    .stApp { background-color: #000; color: #fff; }
    .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
    .card { background-color: #1a1a1a; padding: 20px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 15px; }
    
    /* ปุ่มเจนรูปยักษ์ */
    .stButton>button { 
        background-color: #00ffcc !important; 
        color: #000 !important; 
        border-radius: 20px !important; 
        height: 70px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        box-shadow: 0 0 15px #00ffcc !important;
    }
    
    /* ปุ่มแกะพรอพสีชมพู */
    .pink-button button {
        background-color: #ff00ff !important;
        color: white !important;
        height: 50px !important;
        font-size: 18px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">⚡ ARNON AI FAST v.9.4</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💰 คิดเงินเดือน", "📸 แกะพรอพ & เจนรูป (เร็วพิเศษ)"])

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📸 STEP 1: อัปโหลดรูป (ระบบจะย่อรูปให้เร็วขึ้น)")
    
    uploaded_file = st.file_uploader("เลือกรูปต้นฉบับ:", type=["png", "jpg", "jpeg"])
    
    st.markdown('<div class="pink-button">', unsafe_allow_html=True)
    btn_analyze = st.button("🔍 1. สั่ง AI แกะพรอพ (โหมดด่วน)")
    st.markdown('</div>', unsafe_allow_html=True)

    if btn_analyze:
        if uploaded_file:
            with st.spinner('🚀 กำลังบีบอัดรูปและส่งให้ AI...'):
                # --- โค้ดลดขนาดรูปเพื่อความเร็ว ---
                img_input = Image.open(uploaded_file)
                # ย่อรูปให้เหลือด้านยาวสุดแค่ 800px (ประหยัดเน็ตและเร็วขึ้นมาก)
                img_input.thumbnail((800, 800)) 
                
                # แปลงรูปเป็นไบต์เพื่อส่งให้ AI
                img_byte_arr = io.BytesIO()
                img_input.save(img_byte_arr, format='JPEG', quality=80)
                processed_img = Image.open(img_byte_arr)

                st.image(processed_img, caption="รูปที่ย่อแล้ว (ส่งไวขึ้น)", width=250)
                
                # สั่ง Gemini แกะพรอพ
                model = genai.GenerativeModel('gemini-1.5-flash')
                resp = model.generate_content([
                    "Describe this image briefly but detailed for AI prompt generation. Style, lighting, character. Max 100 words.", 
                    processed_img
                ])
                st.session_state["p_extracted"] = resp.text
                st.success("✅ แกะเสร็จแล้วครับ!")
        else:
            st.warning("พี่ต้องเลือกรูปก่อนนะ!")

    st.write("---")
    st.subheader("📝 STEP 2: เจนรูปใหม่")
    
    current_p = st.session_state.get("p_extracted", "")
    final_p = st.text_area("พรอพ:", value=current_p, height=120)
    
    if st.button("🚀 2. สั่งเจนรูปใหม่ทันที!"):
        if final_p:
            with st.spinner('กำลังเนรมิตรูปใหม่...'):
                encoded_p = final_p.replace(" ", "%20").replace("\n", "%20")
                # ใช้โมเดล Flux ที่เร็วกว่าเดิม
                gen_url = f"https://pollinations.ai/p/{encoded_p}?width=1024&height=1024&seed=42&model=flux"
                st.image(gen_url, use_container_width=True)
        else:
            st.error("ใส่พรอพก่อนนะพี่!")
    st.markdown('</div>', unsafe_allow_html=True)
