import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าตาเว็บ
st.set_page_config(page_title="JAAO COLORFUL AI", page_icon="🎨", layout="centered")

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #f0f8ff; }
    h1 {
        color: #ff4b4b;
        text-align: center;
        background: -webkit-linear-gradient(#ff4b4b, #ffda5f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True) # <--- แก้ตรงนี้จาก stdio เป็น html

# 2. ใส่ API Key ของคุณ (อย่าลืมใส่รหัสของคุณตรงนี้)
API_KEY = "ใส่_API_KEY_ของคุณที่นี่"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. ส่วนหัวของเว็บ
st.markdown("<h1>🌈 JAAO Creative Studio v.2</h1>", unsafe_allow_html=True) # <--- ตรงนี้ด้วยครับ
st.markdown("---")

option = st.selectbox('🎨 เลือกโหมดการสร้างสรรค์:', ('🎵 แต่งเนื้อเพลง', '📹 เขียนสคริปต์ YouTube', '💡 คิดไอเดียคลิปสั้น', '🐍 ช่วยเขียน Code Python'))
user_prompt = st.text_area(f"รายละเอียดสำหรับ {option}:", placeholder="พิมพ์รายละเอียดที่นี่...")

if st.button("เริ่มสร้างความปัง ✨", use_container_width=True):
    if user_prompt:
        with st.spinner("กำลังประมวลผล..."):
            try:
                system_prompt = f"ช่วย {user_prompt} ในฐานะ {option} โดยใช้ emoji เยอะๆ"
                response = model.generate_content(system_prompt)
                st.balloons()
                st.success("สร้างเสร็จเรียบร้อย! 🎉")
                st.info(response.text)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
