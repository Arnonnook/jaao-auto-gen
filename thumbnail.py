import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Thumbnail Master v.2.2", page_icon="🖼️", layout="wide")

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e0e0e; color: #ffffff; }
    .studio-title { color: #fab005 !important; text-align: center; font-size: 40px !important; font-weight: 900 !important; }
    .size-info {
        background-color: #2d3436; padding: 15px; border-radius: 12px;
        border: 2px solid #fab005; margin-bottom: 20px; text-align: center;
    }
    div.stButton > button:first-child {
        background-color: #fab005 !important; color: #0e0e0e !important;
        height: 60px; font-size: 20px; font-weight: bold; border-radius: 30px; width: 100%;
    }
    .concept-card { background-color: #1a1a1a; padding: 20px; border-radius: 15px; border-left: 5px solid #fab005; margin-bottom: 20px; }
    .canva-btn {
        display: block; width: 100%; padding: 15px; background-color: #00c4cc;
        color: white !important; text-decoration: none; border-radius: 12px;
        text-align: center; font-weight: bold; margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อ Gemini
try:
    API_KEY = st.secrets["MY_API_KEY"] 
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key ใน Secrets!")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="studio-title">🖼️ JAAO THUMBNAIL & FONT v.2.2</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="size-info">
    <h3 style="margin:0; color:#fab005;">📐 ขนาดมาตรฐาน YouTube: 1280 x 720 (16:9)</h3>
</div>
""", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("✍️ รายละเอียดผลงาน")
    song_title = st.text_input("ชื่อเพลงของคุณ:", placeholder="เช่น ยิ้มให้ความทรงจำ...")
    video_detail = st.text_area("สรุปเนื้อหาเพลง/อารมณ์เพลง:", height=120)
    
    st.write("🎨 **เลือกสไตล์ฟอนต์ที่ชอบ:**")
    font_style = st.select_slider(
        'ระดับความทางการของฟอนต์',
        options=['ลูกทุ่งคลาสสิก', 'หวานละมุน', 'ทันสมัย/วัยรุ่น', 'ดุดัน/ร็อก', 'สยองขวัญ/ลึกลับ']
    )
    
    target_platform = st.selectbox("เลือกแพลตฟอร์ม:", ["YouTube (16:9)", "Facebook (1:1)", "TikTok (9:16)"])
    gen_btn = st.button("🚀 ออกแบบปกและเลือกฟอนต์")

    st.write("---")
    st.markdown('<a href="https://www.canva.com/" target="_blank" class="canva-btn">🎨 เปิดเว็บ Canva เพื่อทำรูปต่อ</a>', unsafe_allow_html=True)

with col_out:
    if gen_btn:
        if song_title or video_detail:
            with st.spinner("⏳ AI กำลังออกแบบภาพและเลือกฟอนต์ที่สวยที่สุด..."):
                try:
                    prompt = f"""
                    ออกแบบหน้าปกวิดีโอ YouTube
                    ชื่อเพลง: "{song_title}"
                    อารมณ์เพลง: {video_detail}
                    สไตล์ฟอนต์ที่ต้องการ: {font_style}
                    
                    ภารกิจ:
                    1. [CORE_CONCEPT]: สรุปแก่นของภาพปกในประโยคเดียว
                    2. [FONT_RECOMMEND]: แนะนำชื่อฟอนต์ไทย 2-3 ชื่อที่เข้ากับชื่อเพลงและสไตล์ {font_style} (เอาที่หาได้ใน Canva หรือ Google Fonts)
                    3. [TEXT_EFFECT]: แนะนำการแต่งตัวอักษร (เช่น ใส่ขอบสีขาว, เงาสีดำ, หรือทำตัวเอียง)
                    4. [IMAGE_PROMPT]: พร้อมท์ภาษาอังกฤษสำหรับ AI สร้างรูปฉากหลัง
                    """
                    
                    response = model.generate_content(prompt)
                    res = response.text
                    
                    if "[CORE_CONCEPT]" in res:
                        core_val = res.split("[CORE_CONCEPT]")[1].split("[FONT_RECOMMEND]")[0].strip()
                        font_val = res.split("[FONT_RECOMMEND]")[1].split("[TEXT_EFFECT]")[0].strip()
                        effect_val = res.split("[TEXT_EFFECT]")[1].split("[IMAGE_PROMPT]")[0].strip()
                        img_prompt = res.split("[IMAGE_PROMPT]")[1].strip()
                        
                        st.markdown('<div class="concept-card">', unsafe_allow_html=True)
                        st.subheader("🧠 ใจความสำคัญของภาพ:")
                        st.write(core_val)
                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('<div class="concept-card">', unsafe_allow_html=True)
                        st.subheader("🔠 ฟอนต์ที่แนะนำสำหรับเพลงนี้:")
                        st.warning(font_val)
                        st.info(f"✨ **เทคนิคการแต่งฟอนต์:** {effect_val}")
                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('<p style="color:#fab005; font-weight:bold;">🖼️ พร้อมท์สร้างรูปฉากหลัง (ก๊อปไปวาง AI):</p>', unsafe_allow_html=True)
                        st.code(img_prompt, language="text")
                        
                        st.success(f"ชื่อเพลง '{song_title}' เหมาะกับฟอนต์แนว {font_style} มากครับ!")
                    else:
                        st.write(res)
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาใส่ชื่อเพลงก่อนครับพี่ JAAO")

st.caption("© 2026 JAAO Studio | ออกแบบหน้าปกและฟอนต์ระดับมืออาชีพ")
