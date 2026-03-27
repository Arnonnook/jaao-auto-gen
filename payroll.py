# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON AI STATUS", page_icon="📶", layout="wide")

# --- ดึง API Key จาก Secrets ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ อย่าลืมใส่ MY_API_KEY ใน Secrets นะครับ!")

# --- CSS สไตล์นีออน (เหมือนเดิมแต่ปรับปรุงการแจ้งเตือน) ---
st.markdown("""
<style>
    header {visibility: hidden;} .stDeployButton {display:none;}
    footer {visibility: hidden;} #MainMenu {visibility: hidden;}
    .stApp { background-color: #000; color: #fff; }
    .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
    .card { background-color: #1a1a1a; padding: 25px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 20px; }
    
    /* ปุ่มชมพู (แกะพรอพ) */
    .stButton>button[kind="primary"] {
        background-color: #ff00ff !important;
        color: white !important;
        height: 60px !important;
        font-size: 20px !important;
        border-radius: 15px !important;
    }
    
    /* ปุ่มเขียวยักษ์ (เจนรูป) */
    .stButton>button[kind="secondary"] { 
        background-color: #00ffcc !important; 
        color: #000 !important; 
        border-radius: 20px !important; 
        height: 80px !important;
        font-size: 25px !important;
        font-weight: 900 !important;
        box-shadow: 0 0 25px #00ffcc !important;
    }
    /* ปรับแต่งแถบสถานะ (Progress Bar) */
    .stProgress > div > div > div > div { background-color: #00ffcc; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📶 ARNON AI STATUS v.9.6</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💰 คิดเงินเดือน", "📸 แกะพรอพ & เจนรูป (มีแถบสถานะ)"])

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1️⃣ อัปโหลดรูปภาพ")
    
    up_file = st.file_uploader("เลือกรูป (ถ้าอัปไม่ขึ้นจะมีแจ้งเตือน):", type=["png", "jpg", "jpeg"])
    
    if up_file:
        # เช็คขนาดไฟล์ (ป้องกันไฟล์ใหญ่เกินไปจนค้าง)
        if up_file.size > 10 * 1024 * 1024: # ถ้าเกิน 10MB
            st.error("❌ ไฟล์ใหญ่เกินไปครับพี่! ขอไม่เกิน 10MB นะครับ")
        else:
            st.image(up_file, width=200, caption="รูปพร้อมใช้งาน")
            st.success("✅ อัปโหลดสำเร็จ! พร้อมแกะพรอพครับ")

    # ปุ่มแกะพรอพ
    if st.button("🔍 สั่ง AI แกะพรอพจากรูป", type="primary", use_container_width=True):
        if up_file:
            # --- แถบสถานะจำลองการส่งข้อมูล ---
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🚀 กำลังเตรียมไฟล์...")
                progress_bar.progress(20)
                
                img = Image.open(up_file)
                img.thumbnail((800, 800))
                
                status_text.text("📡 กำลังส่งข้อมูลให้ Gemini...")
                progress_bar.progress(50)
                
                model = genai.GenerativeModel('gemini-1.5-flash')
                resp = model.generate_content(["Describe this image for AI prompt. Text only.", img])
                
                progress_bar.progress(90)
                status_text.text("📝 กำลังสรุปผล...")
                time.sleep(0.5)
                
                st.session_state["arnon_p"] = resp.text
                progress_bar.progress(100)
                status_text.text("✅ แกะเสร็จเรียบร้อย!")
                
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาด: {str(e)}")
                st.warning("พี่ลองเช็คอินเทอร์เน็ต หรือ API Key ใน Secrets ดูนะครับ")
        else:
            st.error("❌ พี่ลืมเลือกรูปครับ! กรุณาเลือกรูปก่อนกดปุ่มชมพู")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนที่ 2: เจนรูป ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2️⃣ เจนรูปใหม่")
    
    saved_p = st.session_state.get("arnon_p", "")
    final_text = st.text_area("พรอพ (ตรวจสอบที่นี่ก่อนเจน):", value=saved_p, height=120)
    
    if st.button("🚀 สั่งเจนรูปใหม่ยักษ์!", type="secondary", use_container_width=True):
        if final_text:
            with st.spinner('🎨 กำลังวาดรูปใหม่... (กรุณารอสักครู่)'):
                clean_p = final_text.replace(" ", "%20").replace("\n", "%20")
                gen_url = f"https://pollinations.ai/p/{clean_p}?width=1024&height=1024&seed=42&model=flux"
                st.image(gen_url, use_container_width=True)
        else:
            st.error("❌ ไม่มีพรอพให้เจนครับพี่! กรุณาแกะพรอพจากด้านบนก่อน")
    st.markdown('</div>', unsafe_allow_html=True)
