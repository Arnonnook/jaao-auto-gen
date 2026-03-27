# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON AI STABLE", page_icon="🛡️", layout="wide")

# --- ดึง API Key จาก Secrets ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ อย่าลืมใส่ MY_API_KEY ใน Secrets บนเว็บ Streamlit นะครับ!")

# --- CSS สไตล์นีออน (เน้นความชัดเจน) ---
st.markdown("""
<style>
    header {visibility: hidden;} .stDeployButton {display:none;}
    footer {visibility: hidden;} #MainMenu {visibility: hidden;}
    .stApp { background-color: #000; color: #fff; }
    .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
    .card { background-color: #1a1a1a; padding: 25px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 20px; }
    
    /* ปุ่มกดแกะพรอพ */
    .stButton>button[kind="primary"] {
        background-color: #ff00ff !important;
        color: white !important;
        height: 65px !important;
        font-size: 22px !important;
        font-weight: bold !important;
    }
    
    /* ปุ่มเจนรูปยักษ์ */
    .stButton>button[kind="secondary"] { 
        background-color: #00ffcc !important; 
        color: #000 !important; 
        height: 85px !important;
        font-size: 28px !important;
        font-weight: 900 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🛡️ ARNON AI STABLE v.9.8</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💰 คิดเงินเดือน", "📸 แกะพรอพ & เจนรูป"])

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1️⃣ อัปโหลดรูปภาพ")
    
    up_file = st.file_uploader("เลือกรูปภาพ:", type=["png", "jpg", "jpeg"], key="stable_uploader")
    
    if up_file:
        st.success(f"✔️ ได้รับไฟล์: {up_file.name}")
        img_view = Image.open(up_file)
        st.image(img_view, width=250)

    # ปุ่มแกะพรอพ (ใช้สีชมพู)
    if st.button("🔍 สั่ง AI แกะพรอพ (โหมดเสถียร)", type="primary", use_container_width=True):
        if up_file:
            with st.status("⌛ กำลังประมวลผล... (ห้ามปิดหน้าจอ)", expanded=True) as status:
                try:
                    # 1. ย่อรูปให้เล็กลงมากๆ เพื่อส่งไวขึ้น
                    st.write("📡 กำลังบีบอัดรูปภาพเพื่อความเร็ว...")
                    img = Image.open(up_file)
                    img.thumbnail((600, 600)) # ย่อเหลือ 600px พอครับ AI ยังเห็นชัด
                    
                    # 2. เรียกใช้ Gemini
                    st.write("🤖 Gemini กำลังวิเคราะห์รูป... (อาจใช้เวลา 5-10 วินาที)")
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # กำหนดเวลา Timeout ป้องกันค้าง
                    resp = model.generate_content(
                        ["Describe this image for AI prompt. Keywords only, short and simple.", img],
                        generation_config={"timeout": 15} # ถ้าเกิน 15 วิ ให้ตัดจบ
                    )
                    
                    if resp.text:
                        st.session_state["arnon_p"] = resp.text
                        status.update(label="✅ สำเร็จ!", state="complete")
                    else:
                        st.error("AI ไม่ตอบกลับ ลองกดใหม่อีกครั้งครับ")

                except Exception as e:
                    st.error(f"❌ ค้าง/ผิดพลาด: {str(e)}")
                    st.info("แนะนำ: ให้พี่ลองรีเฟรชหน้าเว็บแล้วอัปโหลดรูปใหม่อีกครั้งครับ")
        else:
            st.error("❌ พี่ต้องเลือกรูปก่อนครับ!")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนที่ 2: เจนรูป ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2️⃣ สร้างรูปใหม่")
    
    # ใช้ค่าว่างถ้ายังไม่มีการแกะพรอพ
    current_val = st.session_state.get("arnon_p", "")
    final_p = st.text_area("พรอพ:", value=current_val, height=120)
    
    if st.button("🚀 สั่งเจนรูปใหม่ยักษ์!", type="secondary", use_container_width=True):
        if final_p:
            with st.spinner('🎨 กำลังวาด...'):
                encoded_p = final_p.replace(" ", "%20").replace("\n", "%20")
                gen_url = f"https://pollinations.ai/p/{encoded_p}?width=1024&height=1024&seed={int(time.time())}&model=flux"
                st.image(gen_url, use_container_width=True)
        else:
            st.error("❌ ไม่มีพรอพครับ!")
    st.markdown('</div>', unsafe_allow_html=True)
