import streamlit as st
import google.generativeai as genai

# --- ดึง Key จาก Secrets (ปลอดภัย 100% บอต GitHub จะไม่เจอ) ---
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("กรุณาใส่ API Key ในช่อง Secrets ก่อนนะครับ!")

# ใช้รุ่น 2.5 ตามที่คุณมีสิทธิ์ (เร็วและฉลาด)
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🌟 JAAO AI AUTO-GEN")

user_input = st.text_area("พิมพ์รายละเอียดที่นี่:")

if st.button("เริ่มรัน ✨"):
    if user_input:
        with st.spinner("AI กำลังทำงาน..."):
            try:
                response = model.generate_content(user_input)
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
