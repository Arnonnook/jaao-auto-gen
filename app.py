import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO AI", page_icon="🎨")

# 2. ใส่ API Key (ใส่รหัสของคุณที่นี่)
API_KEY = "AIzaSyD7PL5ugkzzVGn00Sy8rzwdiMqis7mIjQQ"
genai.configure(api_key=API_KEY)

# --- ฟังก์ชันเลือก Model แบบกันพลาด ---
try:
    # พยายามใช้ 2.5 flash ก่อนเพราะในรูปคุณมันโชว์ตัวนี้
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    try:
        # ถ้าไม่ได้ให้ถอยไปใช้ 1.5 flash รุ่นมาตรฐาน
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        # ถ้ายังไม่ได้อีก ให้ใช้รุ่น pro
        model = genai.GenerativeModel('gemini-pro')

# 3. หน้าจอเว็บ
st.title("🌟 JAAO AI AUTO-GEN")

user_input = st.text_area("รายละเอียดงาน:", placeholder="พิมพ์สิ่งที่ต้องการให้ AI ทำ...")

if st.button("เริ่มสร้างความปัง ✨"):
    if user_input:
        with st.spinner("AI กำลังประมวลผล..."):
            try:
                # บรรทัดสำคัญ: สั่งเจนเนื้อหา
                response = model.generate_content(user_input)
                st.balloons()
                st.success("สำเร็จแล้ว!")
                st.write(response.text)
            except Exception as e:
                # ถ้าพลาดยังไง ให้มันฟ้อง Error ออกมาตรงๆ
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณาพิมพ์รายละเอียดก่อนครับ")
