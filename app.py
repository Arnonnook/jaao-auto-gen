import streamlit as st
import google.generativeai as genai

# --- ดึง Key จากระบบ Secrets (ปลอดภัย 100%) ---
API_KEY = st.secrets["MY_API_KEY"]
genai.configure(api_key=API_KEY)

# ใช้รุ่นที่ระบบคุณอนุญาต (จากที่ดูรูปก่อนหน้า แนะนำ 2.5 flash)
model = genai.GenerativeModel('gemini-2.5-flash')

# ส่วนที่เหลือของโค้ดคงเดิม...
st.title("🌟 JAAO AI AUTO-GEN")
user_input = st.text_area("รายละเอียดงาน:")

if st.button("เริ่มสร้างความปัง ✨"):
    if user_input:
        try:
            response = model.generate_content(user_input)
            st.write(response.text)
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
