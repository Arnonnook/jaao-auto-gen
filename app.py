import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าตาเว็บ
st.set_page_config(page_title="JAAO AI", page_icon="🎨")

# --- CSS แบบใหม่: เน้นให้ปุ่มเด่นเห็นชัดเจน ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    h1 { color: #ff4b4b; text-align: center; font-weight: bold; }
    
    /* สไตล์ปุ่มกด: สีแดงเข้ม ตัวหนังสือขาว ขนาดใหญ่ */
    div.stButton > button:first-child {
        background-color: #ff4b4b !important;
        color: white !important;
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. ใส่ API Key (ใส่รหัสของคุณที่นี่)
API_KEY = "AIzaSyD7PL5ugkzzVGn00Sy8rzwdiMqis7mIjQQ"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. หน้าจอเว็บ
st.markdown("<h1>🌟 JAAO AI AUTO-GEN</h1>", unsafe_allow_html=True)

# เลือกโหมด
option = st.selectbox('🚀 เลือกสิ่งที่ต้องการสร้าง:', 
    ('🎵 แต่งเนื้อเพลง', '📹 เขียนสคริปต์วิดีโอ', '💡 คิดไอเดียคอนเทนต์'))

# --- ขยับปุ่มมาไว้ตรงนี้ เพื่อให้เห็นชัดๆ ก่อนช่องพิมพ์ยาวๆ ---
submit_button = st.button("กดที่นี่เพื่อเริ่มรัน ✨")

# ช่องรับคำสั่ง
user_input = st.text_area("รายละเอียดงาน:", placeholder="พิมพ์รายละเอียดที่นี่...")

# 4. การประมวลผล
if submit_button:
    if user_input:
        with st.spinner("AI กำลังคิดให้ครับ..."):
            try:
                response = model.generate_content(f"ช่วย {user_input} ในฐานะ {option}")
                st.balloons()
                st.success("สำเร็จแล้ว!")
                st.info(response.text)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณาพิมพ์รายละเอียดก่อนกดปุ่มครับ")
