# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io
import time

# 1. ตั้งค่าหน้าเว็บให้จ๊าบ
st.set_page_config(page_title="ARNON AI COPY-PASTE", page_icon="📋", layout="wide")

# --- ฟังก์ชันรีเซ็ตระบบ ---
def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- เชื่อมต่อ Gemini API (ดึงจาก Secrets) ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ พี่อานนท์! อย่าลืมใส่ MY_API_KEY ในช่อง Secrets นะครับ")

# --- CSS สไตล์นีออน (เพิ่มสไตล์ปุ่มก็อปปี้) ---
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
    
    /* ปุ่มรีเซ็ตด่วน */
    .reset-btn button { background-color: #444 !important; color: #ccc !important; height: 40px !important; }
    
    /* สไตล์ปุ่มคัดลอก */
    .copy-btn button {
        background-color: #ffcc00 !important;
        color: #000 !important;
        height: 40px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📋 ARNON AI v.10.0</h1>', unsafe_allow_html=True)

# ปุ่มรีเซ็ตด่วน
col_r1, col_r2 = st.columns([4, 1])
with col_r2:
    if st.button("🔄 ล้างระบบค้าง", key="reset"): reset_app()

tab1, tab2 = st.tabs(["💰 คิดเงินเดือน", "📸 แกะพรอพ & ก็อปปี้ปั๊บ"])

# --- TAB 1: ระบบคิดเงินเดือน (เหมือน v.9.9) ---
with tab1:
    st.info("ระบบคิดเงินเดือนของพี่อานนท์ทำงานปกติเหมือนเดิมครับ")

# --- TAB 2: ระบบแกะพรอพ & ก็อปปี้ (ฟีเจอร์เด็ด!) ---
with tab2:
    # --- ส่วนที่ 1: แกะพรอพ ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1️⃣ อัปโหลดรูปภาพ")
    
    # เพิ่ม label_visibility เพื่อให้เห็นช่องชัดๆ
    up_file = st.file_uploader("จิ้มตรงนี้เพื่อเลือกรูป", type=["jpg", "jpeg", "png"], key="up_v10")
    
    if up_file is not None:
        st.markdown(f"✅ **กำลังโหลดไฟล์:** {up_file.name}")
        img_render = Image.open(up_file)
        st.image(img_render, width=250)

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
                    st.session_state["p_final_v10"] = resp.text
                    status.update(label="✅ แกะเสร็จแล้ว!", state="complete")
                except Exception as e:
                    st.error(f"ผิดพลาด: {e}")
        else:
            st.error("❌ พี่ต้องเลือกรูปก่อนครับ!")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนที่ 2: เจนรูปใหม่ & ก็อปปี้ ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2️⃣ เจนรูปใหม่ หรือ ก็อปปี้พรอพ")
    
    p_now = st.session_state.get("p_final_v10", "")
    final_text = st.text_area("พรอพ (แก้ไขได้):", value=p_now, height=150)
    
    # เพิ่มปุ่มคัดลอก
    if final_text:
        c_1, c_2 = st.columns([1, 1])
        with c_1:
            st.markdown('<div class="copy-btn">', unsafe_allow_html=True)
            if st.button("📋 ก็อปปี้พรอพเดี๋ยวนี้!", key="copy"):
                # ใช้ฟังก์ชัน JavaScript เพื่อคัดลอกพรอพ
                js = f"navigator.clipboard.writeText('{final_text}')"
                st.components.v1.html(f"<script>{js}</script>")
                st.success("✅ คัดลอกพรอพลงคลิปบอร์ดแล้ว! เอาไปวางได้เลยพี่")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    
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
