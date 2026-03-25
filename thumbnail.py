import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Thumbnail Master v.2.1", page_icon="🖼️", layout="wide")

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e0e0e; color: #ffffff; }
    .studio-title { color: #fab005 !important; text-align: center; font-size: 40px !important; font-weight: 900 !important; }
    
    /* กล่องข้อมูลขนาดรูป */
    .size-info {
        background-color: #2d3436;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #fab005;
        margin-bottom: 20px;
        text-align: center;
    }
    
    div.stButton > button:first-child {
        background-color: #fab005 !important; color: #0e0e0e !important;
        height: 60px; font-size: 20px; font-weight: bold; border-radius: 30px; width: 100%;
    }
    .concept-card { background-color: #1a1a1a; padding: 20px; border-radius: 15px; border-left: 5px solid #fab005; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อ Gemini
try:
    API_KEY = st.secrets["MY_API_KEY"] 
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key!")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="studio-title">🖼️ JAAO THUMBNAIL MASTER v.2.1</h1>', unsafe_allow_html=True)

# --- ส่วนระบุขนาดมาตรฐานที่พี่ต้องการ ---
st.markdown("""
<div class="size-info">
    <h3 style="margin:0; color:#fab005;">📐 ขนาดมาตรฐานสำหรับ YouTube Thumbnail</h3>
    <p style="font-size:20px; margin:5px 0;"><b>1280 x 720 พิกเซล</b> (สัดส่วน 16:9)</p>
    <small style="color:#ccc;">ไฟล์ควรเป็น JPG, PNG หรือ GIF และขนาดไม่เกิน 2MB</small>
</div>
""", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("✍️ รายละเอียดหน้าปก")
    video_topic = st.text_input("หัวข้อคลิป:", placeholder="เช่น เพลงลูกทุ่งใหม่ล่าสุด...")
    video_detail = st.text_area("สรุปเนื้อหา/เนื้อเพลง:", height=150)
    
    # เพิ่มตัวเลือกขนาด (เผื่อพี่อยากทำปก Facebook หรือ TikTok)
    target_platform = st.selectbox("เลือกแพลตฟอร์ม:", ["YouTube (16:9)", "Facebook Post (1:1)", "TikTok/Reels (9:16)"])
    
    gen_btn = st.button("🚀 ออกแบบและสร้างพร้อมท์ภาพ")

with col_out:
    if gen_btn:
        if video_topic or video_detail:
            with st.spinner("⏳ AI กำลังคำนวณสัดส่วนและออกแบบภาพ..."):
                try:
                    prompt = f"""
                    ออกแบบหน้าปกสำหรับแพลตฟอร์ม: {target_platform}
                    หัวข้อ: {video_topic} เนื้อหา: {video_detail}
                    
                    ภารกิจ:
                    1. [SIZE_GUIDE]: ระบุขนาดความกว้างxยาว และสัดส่วนที่ต้องใช้
                    2. [CORE_CONCEPT]: สรุปแก่นของภาพในประโยคเดียว
                    3. [TEXT_ON_IMAGE]: ประโยคพาดหัวที่ควรอยู่บนภาพ (ใหญ่และชัด)
                    4. [IMAGE_PROMPT]: พร้อมท์ภาษาอังกฤษสำหรับ AI สร้างรูป (ระบุสัดส่วนในพร้อมท์ด้วย)
                    """
                    
                    response = model.generate_content(prompt)
                    res = response.text
                    
                    try:
                        size_val = res.split("[SIZE_GUIDE]")[1].split("[CORE_CONCEPT]")[0].strip()
                        core_val = res.split("[CORE_CONCEPT]")[1].split("[TEXT_ON_IMAGE]")[0].strip()
                        txt_val = res.split("[TEXT_ON_IMAGE]")[1].split("[IMAGE_PROMPT]")[0].strip()
                        img_prompt = res.split("[IMAGE_PROMPT]")[1].strip()
                        
                        st.markdown('<div class="concept-card">', unsafe_allow_html=True)
                        st.subheader("📏 ขนาดที่ต้องตั้งค่าในแอปแต่งรูป:")
                        st.warning(size_val)
                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('<div class="concept-card">', unsafe_allow_html=True)
                        st.subheader("🧠 ใจความสำคัญของภาพ:")
                        st.write(core_val)
                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('<p style="color:#fab005; font-weight:bold;">📋 พร้อมท์ภาษาอังกฤษ (Copy ไปใส่ AI สร้างรูป):</p>', unsafe_allow_html=True)
                        st.code(img_prompt, language="text")
                        
                        st.markdown(f"**💡 ข้อความบนปก:** {txt_val}")
                        
                    except:
                        st.write(res)

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาใส่รายละเอียดก่อนครับ")

st.caption("© 2026 JAAO Studio | ออกแบบสัดส่วนแม่นยำ 100%")
