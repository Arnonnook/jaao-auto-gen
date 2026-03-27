# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON AI CREATIVE", page_icon="🌈", layout="wide")

# --- เชื่อมต่อ Gemini API ---
try:
    genai.configure(api_key=st.secrets["MY_API_KEY"])
except:
    st.error("⚠️ อย่าลืมใส่ MY_API_KEY ในช่อง Secrets นะครับพี่อานนท์!")

# --- CSS สไตล์สีสดใส + แอนิเมชันพื้นหลัง ---
st.markdown("""
<style>
    /* พื้นหลังแบบไล่เฉดสีและเคลื่อนไหว */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    header {visibility: hidden;} .stDeployButton {display:none;}
    footer {visibility: hidden;} #MainMenu {visibility: hidden;}

    /* หัวข้อโปร่งแสงสวยๆ */
    .main-title {
        background: rgba(255, 255, 255, 0.2);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        font-weight: 900;
        font-size: 50px;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        border: 2px solid white;
        margin-bottom: 30px;
    }

    /* การ์ดแบบกระจกใส (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin-bottom: 25px;
    }

    /* ปุ่มกดสีสดใสและขยายใหญ่ */
    .stButton>button {
        width: 100%;
        border-radius: 50px !important;
        height: 70px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        transition: 0.3s;
        border: none !important;
        text-transform: uppercase;
    }

    /* ปุ่มแกะพรอพสีส้ม-ชมพู */
    .stButton>button[kind="primary"] {
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%) !important;
        color: white !important;
    }

    /* ปุ่มเจนรูปสีเขียว-ฟ้า */
    .stButton>button[kind="secondary"] {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        color: white !important;
        height: 100px !important;
        font-size: 30px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
    }

    /* กล่องข้อความและ Code */
    .stTextArea textarea { border-radius: 15px !important; }
    .stCode { border-radius: 15px !important; }
</style>
""", unsafe_allow_html=True)

# --- ส่วนหัวแอป ---
st.markdown('<div class="main-title">🌈 ARNON AI CREATIVE v.11</div>', unsafe_allow_html=True)

# --- พื้นที่ทำงานหลัก ---
col_main = st.columns([1])[0]

with col_main:
    # --- 1. ส่วนอัปโหลด ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📸 STEP 1: อัปโหลดรูปภาพสุดจ๊าบ")
    
    up_file = st.file_uploader("เลือกรูปจากมือถือพี่:", type=["jpg", "jpeg", "png"], key="v11_up")
    
    if up_file:
        st.image(up_file, width=300, caption="รูปที่พี่เลือก")
        
        if st.button("🚀 สั่ง AI แกะพรอพทันที!", type="primary"):
            with st.status("🔮 กำลังใช้พลัง AI วิเคราะห์...", expanded=True):
                try:
                    img = Image.open(up_file)
                    img.thumbnail((700, 700))
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    resp = model.generate_content(["Create a highly detailed English image prompt based on this image. Text only.", img])
                    st.session_state["p_v11"] = resp.text
                    st.balloons() # แอนิเมชันลูกโป่งฉลอง
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. ส่วนผลลัพธ์และปุ่มคัดลอก ---
    p_val = st.session_state.get("p_v11", "")
    if p_val:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 STEP 2: พรอพที่ได้ (กดปุ่มขวาบนเพื่อก็อปปี้)")
        
        # ใช้ st.code เพื่อปุ่มก๊อปปี้มาตรฐานที่เสถียรที่สุด
        st.code(p_val, language="text")
        
        st.write("---")
        st.subheader("🎨 STEP 3: เจนรูปใหม่หรือแก้ไขพรอพ")
        final_text = st.text_area("ปรับแต่งพรอพของพี่ตรงนี้:", value=p_val, height=150)
        
        if st.button("✨ สั่งเจนรูปใหม่ยักษ์!", type="secondary"):
            with st.spinner('🎨 กำลังร่ายมนตร์สร้างรูป...'):
                clean_p = final_text.replace(" ", "%20").replace("\n", "%20")
                # ใช้โมเดล Flux รุ่นล่าสุด
                gen_url = f"https://pollinations.ai/p/{clean_p}?width=1024&height=1024&seed={int(time.time())}&model=flux"
                st.image(gen_url, caption="✨ ผลงานใหม่ล่าสุดของพี่อานนท์", use_container_width=True)
                st.snow() # แอนิเมชันหิมะตก สวยๆ
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 อัปโหลดรูปแล้วกดปุ่มสีส้มเพื่อเริ่มแกะพรอพนะครับพี่!")

# ปุ่มรีเซ็ตสวยๆ ด้านล่าง
if st.button("🔄 เริ่มต้นใหม่ทั้งหมด"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
