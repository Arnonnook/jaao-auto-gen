import streamlit as st
import google.generativeai as genai

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO FAST AI", page_icon="⚡")

# ตกแต่ง CSS เล็กน้อย (ตัดส่วนที่ทำให้โหลดช้าออก)
st.markdown("""
<style>
    .stApp { background-color: #fafafa; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ใส่ API Key
API_KEY = "AIzaSyD7PL5ugkzzVGn00Sy8rzwdiMqis7mIjQQ"
genai.configure(api_key=API_KEY)

# ใช้รุ่น Flash-Latest (ตัวที่เร็วที่สุด)
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("⚡ JAAO Fast Gen")

user_input = st.text_input("พิมพ์คำสั่งสั้นๆ เพื่อทดสอบความเร็ว:", placeholder="เช่น แต่งกลอน 2 บรรทัด")

if st.button("ส่งคำสั่ง"):
    if user_input:
        # สร้างกล่องว่างไว้รอรับข้อความที่กำลังพิมพ์
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("AI กำลังพิมพ์..."):
            try:
                # ใช้ stream=True เพื่อให้ส่งข้อมูลมาทีละนิด
                response = model.generate_content(user_input, stream=True)
                
                for chunk in response:
                    full_response += chunk.text
                    # อัปเดตข้อความบนหน้าเว็บทันทีที่ได้ข้อมูลใหม่
                    message_placeholder.markdown(full_response + "▌")
                
                # เมื่อเสร็จแล้วเอาตัวขีดออก
                message_placeholder.markdown(full_response)
                st.balloons()
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
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
