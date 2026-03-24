import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าตาเว็บ (ใส่ Icon และสีเริ่มต้น)
st.set_page_config(page_title="JAAO COLORFUL AI", page_icon="🎨", layout="centered")

# --- การตกแต่งด้วย CSS (ส่วนสำคัญที่ทำให้สดใส) ---
st.markdown("""
<style>
    /* พื้นหลังโดยรวม */
    .stApp {
        background-color: #f0f8ff; /* สีฟ้าอ่อนสดใส */
    }
    
    /* สไตล์ของหัวข้อหลัก */
    h1 {
        color: #ff4b4b; /* สีแดงส้มสดใส */
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(#ff4b4b, #ffda5f); /* ไล่สีทอง */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* สไตล์ของปุ่มกด */
    .stButton>button {
        background-color: #4CAF50; /* สีเขียวสดใส */
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049; /* เขียวเข้มขึ้นเมื่อเอาเมาส์ชี้ */
        transform: translateY(-2px);
    }
    
    /* สไตล์ของกล่องข้อมูลผลลัพธ์ */
    .stInfo {
        background-color: #e3f2fd; /* ฟ้าอ่อน */
        border-left: 5px solid #2196f3; /* ขอบฟ้าเข้ม */
        color: #0d47a1; /* ตัวหนังสือฟ้าเข้ม */
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_stdio=True)

# --- ส่วนควบคุม AI (เหมือนเดิม) ---
# 2. ใส่ API Key ของคุณ
API_KEY = "AIzaSyD7PL5ugkzzVGn00Sy8rzwdiMqis7mIjQQ"
genai.configure(api_key=API_KEY)

# ใช้รุ่นที่แรงและยืดหยุ่นที่สุดที่คุณมีสิทธิ์ใช้
# (ผมปรับเป็น gemini-1.5-flash เพื่อความเสถียร แต่คุณใช้ 2.5 ได้ถ้ามี)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- ส่วนหน้าเว็บ (Frontend) ---
# 3. ส่วนหัวของเว็บ
st.markdown("<h1>🌈 JAAO Creative Studio v.2</h1>", unsafe_allow_stdio=True)
st.markdown("---")

# 4. เมนูเลือกประเภทงาน (ปรับโจทย์ให้ชัดเจนขึ้น)
option = st.selectbox(
    '🎨 เลือกโหมดการสร้างสรรค์:',
    ('🎵 แต่งเนื้อเพลง (Lyrics Genius)', '📹 เขียนสคริปต์ YouTube (Content Creator)', '💡 คิดไอเดียคลิปสั้น (TikTok/Reels)', '🐍 ช่วยเขียน Code Python (Coding Buddy)')
)

# 5. ช่องกรอกคำสั่ง (ปรับสีพื้นหลังนิดหน่อยเพื่อให้เด่น)
user_prompt = st.text_area(f"รายละเอียดสำหรับ {option}:", placeholder="เช่น แต่งเพลงรักซึ้งๆ แนวลูกทุ่ง...", height=150)

# 6. ปุ่มกดและแสดงผล
# (ผมเพิ่มลูกเล่นให้ AI ตอบแบบมีสไตล์ด้วย Prompt Engineering)
if st.button("เริ่มสร้างความปัง ✨", use_container_width=True):
    if user_prompt:
        with st.spinner("กำลังประมวลผลด้วย Gemini AI..."):
            try:
                # ปรับแต่งคำสั่งให้ AI ตอบแบบมีสีสันและน่าอ่าน
                system_prompt = f"คุณคือผู้เชี่ยวชาญด้าน {option} ที่เก่งที่สุดในโลก ช่วย {user_prompt} ให้หน่อยครับ โดยขอให้จัดรูปแบบคำตอบให้อ่านง่าย มีการใช้หัวข้อ และอีโมจิ 🤩 เยอะๆ เพื่อความสดใส"
                response = model.generate_content(system_prompt)
                
                st.balloons() # เพิ่มลูกเล่นลูกโป่งลอย
                st.success("สร้างเสร็จเรียบร้อย! 🎉")
                st.markdown("### 📝 ผลลัพธ์สุดปังของคุณ:")
                
                # ใช้ st.info เพื่อแสดงผลในกล่องสีฟ้าที่ตกแต่งไว้
                st.info(response.text)
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณาใส่รายละเอียดก่อนนะครับ")

# 7. ส่วนท้ายเว็บ
st.markdown("---")
st.caption("Developed with ❤️ by JAAO | Powered by Google Gemini AI")
