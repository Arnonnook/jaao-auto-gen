import streamlit as st
import google.generativeai as genai
import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Thumbnail Master", page_icon="🖼️", layout="wide")

# --- การตกแต่งด้วย CSS (สไตล์สตูดิโอออกแบบ) ---
st.markdown("""
<style>
    .stApp { background-color: #121212; color: #ffffff; }
    .studio-title {
        color: #fab005 !important; /* สีเหลืองทอง */
        text-align: center;
        font-size: 40px !important;
        font-weight: 900 !important;
        text-shadow: 0 0 10px rgba(250, 176, 5, 0.3);
    }
    div.stButton > button:first-child {
        background-color: #fab005 !important; /* ปุ่มสีเหลืองทอง */
        color: #121212 !important;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 30px;
        width: 100%;
        border: none;
    }
    .concept-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #fab005;
        margin-bottom: 20px;
    }
    .text-idea { color: #ffeb3b; font-weight: bold; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อ Gemini API
try:
    API_KEY = st.secrets["MY_API_KEY"] 
    genai.configure(api_key=API_KEY)
    # ใช้รุ่น 1.5-flash เพื่อความเร็วและเสถียร
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ ไม่พบ MY_API_KEY ใน Secrets ครับ!")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="studio-title">🖼️ JAAO THUMBNAIL MASTER</h1>', unsafe_allow_html=True)
st.write("---")

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("✍️ ข้อมูลคลิป/เพลงของคุณ")
    video_topic = st.text_input("หัวข้อคลิป:", placeholder="เช่น เพลงลูกทุ่งอกหักซึ้งๆ, สอนใช้ AI...")
    video_detail = st.text_area("สรุปเนื้อหา หรือ เนื้อเพลง:", placeholder="ใส่รายละเอียดเพื่อให้ AI เข้าใจอารมณ์คลิป...", height=150)
    
    st.write("---")
    mood = st.selectbox("อารมณ์ที่ต้องการ:", ["ดึงดูดใจ/น่าสนใจ", "สนุกสนาน/ตื่นเต้น", "เศร้า/ซึ้ง", "จริงจัง/น่าเชื่อถือ", "แปลกใหม่/หลุดโลก"])
    
    gen_concept = st.button("🚀 สร้างแนวทางหน้าปก Masterpiece")

with col_out:
    if gen_concept:
        if video_topic or video_detail:
            with st.spinner("⏳ ผมกำลังวิเคราะห์อารมณ์คลิปและออกแบบแนวทางหน้าปกให้พี่..."):
                try:
                    # สั่ง AI ให้วิเคราะห์และออกแบบหน้าปกอย่างละเอียด
                    prompt = f"""
                    คุณคือผู้เชี่ยวชาญด้าน Graphic Design และ Marketing สำหรับ YouTube
                    ช่วยออกแบบแนวทางภาพหน้าปก (Thumbnail) สำหรับคลิปหัวข้อ: "{video_topic}"
                    เนื้อหา: "{video_detail}"
                    อารมณ์ที่ต้องการ: {mood}
                    
                    ให้ข้อมูลที่เป็นรูปธรรมตามหมวดหมู่ดังนี้:
                    1. [VISUAL_CONCEPT]: บรรยายภาพองค์ประกอบหลักที่ควรมีบนปก (ตัวละคร, ฉากหลัง, ท่าทาง)
                    2. [TEXT_ON_IMAGE]: เสนอข้อความพาดหัวสั้นๆ 1-2 ประโยค ที่ต้องอยู่บนปก (ต้องใหญ่และเด่น)
                    3. [COLOR_PALETTE]: แนะนำโทนสีหลักที่ควรใช้เพื่อให้ดึงดูดสายตาตามอารมณ์ที่เลือก
                    4. [COMPOSITION]: แนะนำการจัดวางองค์ประกอบภาพ (เช่น กฎสามส่วน, การเน้นจุดเด่น)
                    5. [TIPS]: เทคนิคพิเศษเฉพาะคลิปนี้เพื่อให้คนกดดูเยอะขึ้น
                    """
                    
                    response = model.generate_content(prompt)
                    res = response.text
                    
                    st.success("ออกแบบเสร็จเรียบร้อย! นำแนวทางนี้ไปสร้างปกได้เลย")
                    
                    # แสดงผลแบบแยกหมวดหมู่
                    try:
                        vis_val = res.split("[VISUAL_CONCEPT]")[1].split("[TEXT_ON_IMAGE]")[0].strip()
                        txt_val = res.split("[TEXT_ON_IMAGE]")[1].split("[COLOR_PALETTE]")[0].strip()
                        col_val = res.split("[COLOR_PALETTE]")[1].split("[COMPOSITION]")[0].strip()
                        com_val = res.split("[COMPOSITION]")[1].split("[TIPS]")[0].strip()
                        tip_val = res.split("[TIPS]")[1].strip()
                        
                        st.markdown('<div class="concept-card">', unsafe_allow_html=True)
                        st.subheader("🖼️ แนวทางภาพหลัก:")
                        st.write(vis_val)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('<div class="concept-card">', unsafe_allow_html=True)
                        st.subheader("🔠 ข้อความบนปก (ก๊อปไปวางได้เลย):")
                        st.info(txt_val)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('<div class="concept-card">', unsafe_allow_html=True)
                        st.subheader("🎨 โทนสีและเทคนิค:")
                        st.write(f"**โทนสีแนะนำ:** {col_val}")
                        st.write(f"**การจัดวาง:** {com_val}")
                        st.write(f"**เทคนิคพิเศษ:** {tip_val}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    except:
                        st.write(res) # กรณี AI รูปแบบเพี้ยน

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาใส่หัวข้อคลิปหรือรายละเอียดก่อนครับพี่ JAAO")

st.write("---")
st.caption("© 2026 JAAO Studio | ออกแบบหน้าปกให้ดึงดูดสายตา")
