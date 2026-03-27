# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import requests
import io

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON Payroll & AI", page_icon="🎨", layout="wide")

# --- ดึง API Key จาก Secrets (พี่ต้องไปใส่ใน Streamlit Cloud Secrets นะครับ) ---
# ชื่อตัวแปรใน Secrets ต้องชื่อ "MY_API_KEY"
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ พี่อานนท์อย่าลืมเอา API Key ไปใส่ในช่อง Secrets บน Streamlit Cloud นะครับ!")

# --- CSS สไตล์นีออนจ๊าบๆ ---
st.markdown("""
<style>
    header {visibility: hidden;} .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #000; color: #fff; }
    .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
    .card { background-color: #1a1a1a; padding: 20px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 15px; }
    label { color: #00ffcc !important; font-weight: bold; }
    .stButton>button { background-color: #ff00ff; color: white; border-radius: 10px; border: none; width: 100%; }
    .gen-button>button { background-color: #00ffcc; color: #000 !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🎨 ARNON PAYROLL & AI v.9.1</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💰 คิดเงินเดือน", "📸 แกะพรอพ & เจนรูปใหม่"])

# --- TAB 1: ระบบคิดเงินเดือน ---
with tab1:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🏢 รายได้หลัก")
            daily_rate = st.number_input("ค่าแรงพื้นฐานต่อวัน (฿):", value=350)
            c_p, c_l = st.columns(2)
            with c_p: pos_allowance = st.number_input("ค่าตำแหน่ง:", value=0)
            with c_l: liv_allowance = st.number_input("ค่าครองชีพ:", value=0)
            st.markdown('</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📅 วันทำงาน/ลา")
            total_days = st.number_input("จำนวนวันทำงานในเดือน:", value=26)
            leave_dates = st.multiselect("จิ้มเลือก 'วันที่ลา':", options=[d for d in range(1, 32)])
            actual_work_days = total_days - len(leave_dates)
            st.write(f"✨ ทำงานจริง: {actual_work_days} วัน")
            c_i1, c_i2 = st.columns(2)
            with c_i1: inc1 = st.checkbox("วิกแรก ✅", value=True)
            with c_i2: inc2 = st.checkbox("วิกสอง ✅", value=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🕒 โอที (OT)")
            ot_mode = st.radio("โหมดโอที:", ["วัน (2.5 ชม.)", "ชั่วโมง"])
            hr_rate = daily_rate / 8
            if ot_mode == "วัน (2.5 ชม.)":
                d1, d2, d3 = st.columns(3)
                with d1: ot_n_d = st.number_input("1.5x (วัน):", value=0)
                with d2: ot_h_d = st.number_input("2x (วัน):", value=0)
                with d3: ot_s_d = st.number_input("3x (วัน):", value=0)
                p_ot_n = ot_n_d * 2.5 * (hr_rate * 1.5)
                p_ot_h = ot_h_d * 8 * (hr_rate * 2.0)
                p_ot_s = ot_s_d * 8 * (hr_rate * 3.0)
            else:
                h1, h2, h3 = st.columns(3)
                with h1: ot_n_h = st.number_input("1.5x (ชม.):", value=0.0)
                with h2: ot_h_h = st.number_input("2x (ชม.):", value=0.0)
                with h3: ot_s_h = st.number_input("3x (ชม.):", value=0.0)
                p_ot_n = ot_n_h * (hr_rate * 1.5)
                p_ot_h = ot_h_h * (hr_rate * 2.0)
                p_ot_s = ot_s_h * (hr_rate * 3.0)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- คำนวณรายได้ ---
    total_base = (daily_rate * total_days) + pos_allowance + liv_allowance
    total_inc = (350 if inc1 else 0) + (350 if inc2 else 0)
    total_welfare = (50 + 60) * actual_work_days
    gross = total_base + p_ot_n + p_ot_h + p_ot_s + total_inc + total_welfare
    
    sso_p = st.sidebar.slider("ประกันสังคม (%)", 0.0, 5.0, 4.0, 0.1)
    sso_val = int(gross * (sso_p / 100))
    if sso_val > 750: sso_val = 750
    net = gross - sso_val

    with col2:
        st.subheader("📑 รายละเอียดสลิป")
        res = {"รายการ": ["ค่าแรงพื้นฐาน", "ตำแหน่ง+ครองชีพ", "โอทีรวม", "เบี้ยขยัน", "ข้าว+รถ"],
               "เงิน (฿)": [f"{total_base:,.2f}", f"{(pos_allowance+liv_allowance):,.2f}", f"{(p_ot_n+p_ot_h+p_ot_s):,.2f}", f"{total_inc:,.2f}", f"{total_welfare:,.2f}"]}
        st.table(pd.DataFrame(res))
        st.markdown(f"**หักประกันสังคม ({sso_p}% จากยอดรวม):** -{sso_val:,.0f} ฿")
        st.markdown(f'<div class="total-box"><h1 style="color:#fff;">฿ {net:,.2f}</h1></div>', unsafe_allow_html=True)

# --- TAB 2: ระบบแกะพรอพ & เจนรูป ---
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📸 STEP 1: แกะพรอพจากรูป")
    
    img_size_choice = st.selectbox("ขนาดรูปที่จะเจนใหม่:", ["1024x1024", "1920x1080", "1080x1920"])
    uploaded_file = st.file_uploader("อัปโหลดรูปต้นฉบับ:", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        img_input = Image.open(uploaded_file)
        st.image(img_input, width=250)
        
        if st.button("🔍 1. สั่ง AI แกะพรอพ"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt_text = "Analyze this image and write a highly detailed English prompt for image generation. Style, lighting, background. Text only."
            with st.spinner('กำลังแกะพรอพ...'):
                resp = model.generate_content([prompt_text, img_input])
                st.session_state["p_extracted"] = resp.text

    if "p_extracted" in st.session_state:
        st.write("---")
        st.subheader("📝 STEP 2: เจนรูปใหม่")
        final_p = st.text_area("พรอพที่แกะได้ (แก้ได้นะ):", value=st.session_state["p_extracted"], height=100)
        
        st.markdown('<div class="gen-button">', unsafe_allow_html=True)
        if st.button("🚀 2. สั่งเจนรูปใหม่ทันที!"):
            with st.spinner('กำลังเจนรูป...'):
                encoded_p = final_p.replace(" ", "%20")
                w, h = (1024, 1024)
                if "1920x1080" in img_size_choice: w, h = (1920, 1080)
                if "1080x1920" in img_size_choice: w, h = (1080, 1920)
                
                gen_url = f"https://pollinations.ai/p/{encoded_p}?width={w}&height={h}&seed=42&model=flux"
                st.image(gen_url, use_container_width=True)
                st.success("จ๊าบมากครับพี่อานนท์!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
