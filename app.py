import streamlit as st
import google.generativeai as genai
import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Creative Studio", page_icon="🌈", layout="centered")

# ระบบเก็บข้อมูลใน Session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #fdfcf5; }
    h1 { color: #ff4b4b; text-align: center; font-weight: bold; }
    
    /* สไตล์ปุ่มกดหลัก */
    .main-button > div > button {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 15px;
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
    }
    
    /* กล่องข้อมูลพิเศษ */
    .special-info {
        background-color: #fff4e6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ff922b;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 2. ดึง Key จาก Secrets
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key! กรุณาตรวจสอบ Secrets")
    st.stop()

# 3. ส่วนหน้าจอหลัก
st.markdown("<h1>🌈 JAAO Creative Studio v.6</h1>", unsafe_allow_html=True)

# --- แถบด้านข้าง (Sidebar) ---
with st.sidebar:
    st.title("📜 ประวัติการสร้าง")
    if st.button("ล้างประวัติ"):
        st.session_state.history = []
        st.rerun()
    st.write("---")
    for item in reversed(st.session_state.history):
        with st.expander(f"📌 {item['time']} - {item['type']}"):
            st.write(item['result'])

# --- ส่วนปุ่มลัด (Quick Prompts) ---
st.write("✨ **เลือกตัวอย่างคำสั่ง:**")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🎵 เพลงลูกทุ่ง"):
        st.session_state.input_text = "แต่งเพลงลูกทุ่งร่วมสมัย หนุ่มโรงงานอกหัก ขอจังหวะสนุกๆ"
        st.rerun()
with c2:
    if st.button("📷 ภาพ Portrait"):
        st.session_state.input_text = "Prompt: Thai woman, silk dress, sunlit garden, 8k, bokeh"
        st.rerun()
with c3:
    if st.button("🎤 เพลงแร็ป"):
        st.session_state.input_text = "เขียนไรม์แร็ปเล่าชีวิตคนทำ AI ชื่อ JAAO ขอแบบดุดัน"
        st.rerun()

# --- ส่วนรับข้อมูล ---
option = st.selectbox('🎨 เลือกโหมด:', ('🎵 แต่งเนื้อเพลง', '📷 พร้อมถ่ายภาพบุคคล', '📹 สคริปต์วิดีโอ'))
user_input = st.text_area("รายละเอียดงานของคุณ:", value=st.session_state.input_text, height=150)

# 4. ปุ่มรันงาน
st.markdown('<div class="main-button">', unsafe_allow_html=True)
if st.button("เริ่มสร้างความปัง ✨"):
    if user_input:
        with st.spinner("AI กำลังคิดข้อมูลพิเศษให้คุณ..."):
            try:
                # สั่ง AI ให้แยกส่วนคำตอบชัดเจน
                prompt_to_ai = f"""
                ในฐานะผู้เชี่ยวชาญด้าน {option} ช่วย {user_input} โดยแบ่งคำตอบเป็น 2 ส่วนดังนี้:
                1. [RESULT]: เนื้อหาหลักที่คุณสร้าง (เช่น เนื้อเพลง หรือ Prompt)
                2. [SPECIAL_INFO]: ข้อมูลพิเศษ (ถ้าเป็นเพลงให้บอก Style, Tempo, Mood / ถ้าเป็นภาพให้บอกเทคนิคการจัดแสง, เลนส์ที่ควรใช้, และคำสั่งลับเพิ่มความสวย)
                ขอแบบเจ๋งๆ พร้อมอีโมจิ 🤩
                """
                
                response = model.generate_content(prompt_to_ai)
                full_text = response.text
                
                # แยกส่วนคำตอบ (ถ้า AI ทำตามสั่ง)
                parts = full_text.split("[SPECIAL_INFO]")
                main_result = parts[0].replace("[RESULT]", "").strip()
                special_info = parts[1].strip() if len(parts) > 1 else "ไม่มีข้อมูลพิเศษเพิ่มเติม"

                st.balloons()
                st.success("สร้างเสร็จแล้ว! 🎉")
                
                # แสดงเนื้อหาหลัก
                st.markdown("### 📝 ผลลัพธ์หลัก:")
                st.info(main_result)
                
                # แสดงข้อมูลพิเศษในกล่องสีส้ม
                st.markdown("### 💡 ข้อมูลพิเศษ & เทคนิคเพิ่มเติม:")
                st.markdown(f'<div class="special-info">{special_info}</div>', unsafe_allow_html=True)
                
                # บันทึกประวัติ
                now = datetime.datetime.now().strftime("%H:%M")
                st.session_state.history.append({"type": option, "result": full_text, "time": now})
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณากรอกข้อมูลก่อนครับ")
st.markdown('</div>', unsafe_allow_html=True)
