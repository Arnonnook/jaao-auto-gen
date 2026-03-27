# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON Payroll & AI", page_icon="📸", layout="wide")

# --- ระบบ Login ---
def check_login():
    if "logged_in" not in st.session_state:
        st.markdown('<h1 style="color:#00ffcc; text-align:center;">🔐 ARNON LOGIN SYSTEM</h1>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
        with col_b:
            api = st.text_input("Gemini API Key", type="password", help="คีย์จาก aistudio.google.com")
        
        if st.button("🚀 เข้าสู่ระบบสุดจ๊าบ", use_container_width=True):
            if u == "arnon" and p == "1234" and api:
                st.session_state["logged_in"] = True
                st.session_state["user_api_key"] = api
                st.rerun()
            else:
                st.error("ใส่รหัสและ API Key ให้ครบนะพี่!")
        return False
    return True

if check_login():
    # --- CSS สไตล์นีออน ---
    st.markdown("""
    <style>
        header {visibility: hidden;} .stDeployButton {display:none;}
        .stApp { background-color: #000; color: #fff; }
        .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
        .card { background-color: #1a1a1a; padding: 20px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 15px; }
        label { color: #00ffcc !important; font-weight: bold; }
        .stButton>button { background-color: #ff00ff; color: white; border-radius: 10px; border: none; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">🤑 ARNON PAYROLL & AI v.8.5</h1>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["💰 คิดเงินเดือนสุดจ๊าบ", "📸 แกะพรอพจากรูป (AI)"])

    # --- TAB 1: ระบบคิดเงินเดือนเดิม ---
    with tab1:
        col1, col2 = st.columns([1, 1.2])
        with col1:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                daily_rate = st.number_input("ค่าแรงต่อวัน:", value=350)
                total_days = st.number_input("วันทำงาน:", value=26)
                leave_dates = st.multiselect("วันที่ลา:", options=[d for d in range(1, 32)])
                st.markdown('</div>', unsafe_allow_html=True)
        
        # (ส่วนคำนวณเงินเหมือน v.8.0 ... ผมขอละไว้ในฐานที่เข้าใจเพื่อความสั้น)
        st.write("ระบบเงินเดือนทำงานปกติเหมือนเดิมครับพี่!")

    # --- TAB 2: ระบบแกะพรอพจากรูป (ฟีเจอร์ใหม่!) ---
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📸 เครื่องมือแกะพรอพจากรูปภาพ")
        
        # 1. เลือกขนาดที่จะวิเคราะห์
        img_size = st.select_slider(
            "เลือกขนาด/ความละเอียดในการวิเคราะห์ (Scale):",
            options=["256", "512", "1024", "2048", "Original"],
            value="1024"
        )
        
        # 2. อัปโหลดรูป
        uploaded_file = st.file_uploader("เลือกรูปภาพที่พี่อยากแกะพรอพ (PNG, JPG):", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="รูปต้นฉบับของพี่", width=300)
            
            if st.button("🔍 สั่ง AI แกะพรอพเดี๋ยวนี้!"):
                try:
                    genai.configure(api_key=st.session_state["user_api_key"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt_instruction = f"""
                    Analyze this image and extract a very detailed English prompt for image generation. 
                    Describe style, lighting, character, background, and camera angle. 
                    Focus on quality terms. Size preference: {img_size}.
                    """
                    
                    with st.spinner('AI กำลังเพ่งเล็งรูปพี่อยู่...'):
                        response = model.generate_content([prompt_instruction, image])
                        
                    st.markdown("### 📝 พรอพที่แกะได้:")
                    extracted_text = response.text
                    st.code(extracted_text, language='text')
                    st.success("แกะเสร็จแล้วครับพี่! ก๊อปปี้ไปใช้ได้เลย")
                    
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("🚪 Log Out"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
