import streamlit as st
import google.generativeai as genai
import datetime
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Thumbnail Master v.2.0", page_icon="🖼️", layout="wide")

# --- การตกแต่งด้วย CSS (สไตล์สตูดิโอออกแบบ & Neon Yellow) ---
st.markdown("""
<style>
    .stApp { background-color: #0e0e0e; color: #ffffff; }
    .studio-title {
        color: #fab005 !important;
        text-align: center;
        font-size: 45px !important;
        font-weight: 900 !important;
        text-shadow: 0 0 15px rgba(250, 176, 5, 0.5);
    }
    div.stButton > button:first-child {
        background-color: #fab005 !important;
        color: #0e0e0e !important;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 30px;
        width: 100%;
        border: none;
    }
    .concept-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #fab005;
        margin-bottom: 20px;
    }
    .prompt-box {
        background-color: #0e0e0e;
        color: #ffda5f;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #fab005;
        font-family: monospace;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อ Gemini API
try:
    API_KEY = st.secrets["MY_API_KEY"] 
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key!")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="studio-title">🖼️ JAAO THUMBNAIL MASTER v.2.0</h1>', unsafe_allow_html=True)
st.write("---")

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("✍️ ข้อมูลคลิป/เพลงของคุณ")
    video_topic = st.text_input("หัวข้อคลิป:", placeholder="เช่น เพลงลูกทุ่งอกหักซึ้งๆ...")
    video_detail = st.text_area("สรุปเนื้อหา หรือ เนื้อเพลง:", placeholder="ใส่รายละเอียด...", height=200)
    mood = st.selectbox("อารมณ์หน้าปก:", ["ดึงดูดใจ/น่าสนใจ", "สนุกสนาน/ตื่นเต้น", "เศร้า/ซึ้ง", "จริงจัง", "แปลกใหม่"])
    
    gen_btn = st.button("🚀 ออกแบบและสร้างพร้อมท์ภาพ Masterpiece")

with col_out:
    if gen_btn:
        if video_topic or video_detail:
            with st.spinner("⏳ ผมกำลังวิเคราะห์อารมณ์และออกแบบแนวทางหน้าปกให้พี่..."):
                try:
                    # สั่ง AI ให้วิเคราะห์ Design และสร้าง Image Prompt (ภาษาอังกฤษ)
                    prompt = f"""
                    วิเคราะห์คลิปหัวข้อ: "{video_topic}"
                    เนื้อหา: "{video_detail}"
                    อารมณ์: {mood}
                    
                    คุณคือผู้เชี่ยวชาญด้าน Graphics และ AI Image Generation ช่วยออกแบบแนวทางภาพหน้าปก:
                    [VISUAL_CONCEPT]: บรรยายภาพองค์ประกอบหลักบนปก
                    [TEXT_ON_IMAGE]: ข้อความพาดหัวสั้นๆ 1 ประโยค ที่โดนใจ (ภาษาไทย)
                    [CORE_CONCEPT]: สรุปใจความสำคัญของภาพปกในประโยคเดียว (ภาษาไทย)
                    [IMAGE_PROMPT]: สร้างพร้อมท์สร้างรูปภาษาอังกฤษแบบละเอียด (Hyper-realistic, 8k, golden hour, highly detailed) สำหรับ AI สร้างรูปตามCORE_CONCEPT
                    """
                    
                    response = model.generate_content(prompt)
                    res = response.text
                    
                    st.success("ออกแบบเสร็จเรียบร้อย! นำไปใช้ต่อได้เลยครับ")
                    
                    # สกัดข้อมูลมาโชว์
                    try:
                        vis_val = res.split("[VISUAL_CONCEPT]")[1].split("[TEXT_ON_IMAGE]")[0].strip()
                        txt_val = res.split("[TEXT_ON_IMAGE]")[1].split("[CORE_CONCEPT]")[0].strip()
                        core_val = res.split("[CORE_CONCEPT]")[1].split("[IMAGE_PROMPT]")[0].strip()
                        img_prompt = res.split("[IMAGE_PROMPT]")[1].strip()
                        
                        st.markdown('<div class="concept-card">', unsafe_allow_html=True)
                        st.subheader("🧠 แก่นความคิด (CORE CONCEPT):")
                        st.info(core_val)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('<div class="concept-card">', unsafe_allow_html=True)
                        st.subheader("🔠 ข้อความพาดหัวบนปก (ภาษาไทย):")
                        st.write(txt_val)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('<div class="concept-card">', unsafe_allow_html=True)
                        st.subheader("🎨 พร้อมท์ภาษาอังกฤษสำหรับ AI สร้างรูป (ก๊อปไปวางใน Midjourney/Canva AI ได้เลย):")
                        st.code(img_prompt, language="text") # ช่องนี้จะสะอาด มีแต่พร้อมท์ล้วนๆ
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # เพิ่มปุ่มจำลองการเจนรูป
                        if st.button("🎨 เริ่มเจนรูปจากพร้อมท์นี้"):
                            with st.spinner("⏳ ระบบกำลังเชื่อมต่อ AI สร้างรูป..."):
                                time.sleep(2) # จำลองเวลาเจนรูป
                                st.warning("⚠️ ตอนนี้ผมยังไม่ได้ต่อ Stable Diffusion API จริงๆ ครับ ถ้าพี่สมัคร Key แล้วผมจะทำให้มันเจนรูปโชว์ในแอปได้เลยครับ!")
                        
                    except:
                        st.write(res) # กรณี AI รูปแบบเพี้ยน

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาใส่หัวข้อคลิปหรือรายละเอียดก่อนครับพี่ JAAO")

st.write("---")
st.caption("Developed by JAAO | AI Thumbnail & Image Generator Studio")
