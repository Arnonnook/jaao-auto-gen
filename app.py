import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าตาเว็บ (ใส่ Icon และสี)
st.set_page_config(page_title="JAAO AI STUDIO", page_icon="🎵", layout="centered")

# 2. ใส่ API Key ของคุณ
API_KEY = "AIzaSyD7PL5ugkzzVGn00Sy8rzwdiMqis7mIjQQ"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. ส่วนหัวของเว็บ
st.title("🚀 JAAO AI Auto-Gen v.1")
st.markdown("---")

# 4. เมนูเลือกประเภทงาน (ทำให้ใช้งานง่ายขึ้น)
option = st.selectbox(
    'วันนี้อยากให้ AI ช่วยทำอะไรดีครับ?',
    ('แต่งเนื้อเพลง (Lyrics)', 'เขียนสคริปต์ YouTube', 'คิดไอเดียทำคลิป', 'ช่วยเขียน Code Python')
)

# 5. ช่องกรอกคำสั่ง
user_prompt = st.text_area(f"รายละเอียดสำหรับ {option}:", placeholder="เช่น แต่งเพลงรักซึ้งๆ แนวลูกทุ่ง...")

# 6. ปุ่มกดและแสดงผล
if st.button("เริ่มสร้างสรรค์ ✨", use_container_width=True):
    if user_prompt:
        with st.spinner("กำลังประมวลผลด้วย Gemini 2.5..."):
            try:
                # ปรับแต่งคำสั่งให้ AI เข้าใจบริบทมากขึ้น
                full_prompt = f"ในฐานะผู้เชี่ยวชาญด้าน {option} ช่วย {user_prompt} ให้หน่อยครับ"
                response = model.generate_content(full_prompt)
                
                st.success("สร้างเสร็จเรียบร้อย!")
                st.markdown("### 📝 ผลลัพธ์ของคุณ:")
                st.info(response.text)
                
                # ปุ่มก๊อปปี้ (กดที่ไอคอนมุมขวาของกล่องข้อความได้เลย)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณาใส่รายละเอียดก่อนนะครับ")

# 7. ส่วนท้ายเว็บ
st.markdown("---")
st.caption("Developed by JAAO | Powered by Google Gemini 2.5")
