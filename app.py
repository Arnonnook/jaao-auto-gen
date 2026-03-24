import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บ (Colorful & Creative)
st.set_page_config(page_title="JAAO Creative Studio", page_icon="🎨", layout="centered")

# --- การตกแต่งด้วย CSS (ส่วนสำคัญที่ทำให้สดใส) ---
st.markdown("""
<style>
    /* พื้นหลังโดยรวม */
    .stApp {
        background-color: #fdfcf5; /* สีครีมอ่อนสดใส */
    }
    
    /* สไตล์ของหัวข้อหลัก */
    h1 {
        color: #ff4b4b; /* สีแดงส้มสดใส */
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        background: -webkit-linear-gradient(#ff4b4b, #ffda5f); /* ไล่สีทอง */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* สไตล์ของปุ่มกด */
    div.stButton > button {
        background-color: #ff4b4b !important; /* สีแดงสด */
        color: white !important;
        border-radius: 20px;
        border: none;
        padding: 15px 30px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 6px 10px rgba(0,0,0,0.1);
        width: 100%;
        height: 60px;
    }
    div.stButton > button:hover {
        background-color: #e04343 !important; /* แดงเข้มขึ้นเมื่อเอาเมาส์ชี้ */
        transform: translateY(-2px);
    }
    
    /* สไตล์ของกล่องข้อมูลผลลัพธ์ */
    .result-box {
        background-color: white; /* ขาวสะอาด */
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #ff4b4b; /* ขอบแดงเข้ม */
        color: #333; /* ตัวหนังสือดำเข้ม */
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# 2. ตั้งค่า API Key จาก Secrets (ปลอดภัย 100%)
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("กรุณาใส่ API Key ในช่อง Secrets ก่อนนะครับ!")
    st.stop() # หยุดการทำงานถ้าไม่มี Key

# ใช้รุ่น 2.5 Flash ตามที่ระบบคุณแนะนำ (เร็วและฉลาดสุด)
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. ส่วนการแสดงผลหน้าเว็บ
st.markdown("<h1>🌈 JAAO Creative Studio v.3</h1>", unsafe_allow_html=True)
st.write("---")

# เลือกโหมดการทำงาน
option = st.selectbox(
    '🎨 เลือกโหมดการสร้างสรรค์:',
    ('🎵 แต่งเนื้อเพลง (Lyrics Genius)', '📷 สร้างพร้อมทำภาพถ่ายบุคคล (Portrait Prompt)', '📹 เขียนสคริปต์วิดีโอ (Content Creator)', '💡 คิดไอเดียคอนเทนต์ (TikTok/Reels)')
)

# ช่องรับคำสั่ง
user_input = st.text_area(f"รายละเอียดสำหรับ {option}:", placeholder="เช่น แต่งเพลงรักซึ้งๆ แนวลูกทุ่ง...", height=150)
# --- แถบด้านข้าง (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3858/3858902.png", width=100)
    st.title("คู่มือการใช้งาน 📖")
    st.info("""
    1. เลือกโหมดที่ต้องการ
    2. พิมพ์รายละเอียด (ภาษาไทยหรืออังกฤษก็ได้)
    3. กดปุ่ม 'เริ่มสร้างความปัง'
    4. รอ AI ประมวลผลสักครู่...
    """)
    st.warning("⚠️ หากขึ้น Error ให้รอ 1 นาทีแล้วกดใหม่นะครับ (เนื่องจากเป็นเวอร์ชันฟรี)")
with st.expander("💡 ดูตัวอย่างคำสั่งที่น่าสนใจ"):
    st.write("**สำหรับแต่งเพลง:**")
    st.code("แต่งเพลงแนว Lo-fi นั่งเหงาๆ ในร้านกาแฟตอนฝนตก")
    
    st.write("**สำหรับสร้างพร้อมภาพ:**")
    st.code("Portrait ผู้ชายสไตล์เกาหลี หน้าใส แสงธรรมชาติ ในสตูดิโอขาว")
    
    st.write("**สำหรับสคริปต์คลิป:**")
    st.code("สคริปต์รีวิวแอป AI ตัวใหม่ภายใน 30 วินาที")
# 4. ปุ่มกดและแสดงผล
if st.button("เริ่มสร้างความปัง ✨"):
    if user_input:
        with st.spinner("กำลังประมวลผลด้วย Gemini AI..."):
            try:
                # ปรับแต่งคำสั่งให้ AI ตอบแบบมีสไตล์และน่าอ่าน
                system_prompt = f"คุณคือผู้เชี่ยวชาญด้าน {option} ที่เก่งที่สุดในโลก ช่วย {user_input} ให้หน่อยครับ โดยขอให้จัดรูปแบบคำตอบให้อ่านง่าย มีการใช้หัวข้อ และอีโมจิ 🤩 เยอะๆ เพื่อความสดใส"
                response = model.generate_content(system_prompt)
                
                st.balloons() # เพิ่มลูกเล่นลูกโป่งลอย
                st.success("สร้างเสร็จเรียบร้อย! 🎉")
                st.markdown("### 📝 ผลลัพธ์สุดปังของคุณ:")
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True) # แสดงผลในกล่องสีขาวที่ตกแต่งไว้
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณาใส่รายละเอียดก่อนนะครับ")

# 5. ส่วนท้ายเว็บ
st.markdown("---")
st.caption("Developed with ❤️ by JAAO | Powered by Google Gemini AI")
