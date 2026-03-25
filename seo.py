import streamlit as st
from groq import Groq
import datetime
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO YouTube SEO Pro", page_icon="🚀", layout="wide")

# --- การตกแต่งด้วย CSS (สไตล์ YouTube Dark Mode) ---
st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; color: #ffffff; }
    .seo-title {
        color: #ff0000 !important; /* แดง YouTube */
        text-align: center;
        font-size: 40px !important;
        font-weight: 900 !important;
        text-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
    }
    div.stButton > button:first-child {
        background-color: #ff0000 !important;
        color: white !important;
        height: 55px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 30px; /* ปุ่มมนสไตล์ YouTube */
        width: 100%;
        border: none;
    }
    .result-box {
        background-color: #212121;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-top: 15px;
    }
    .tag-style {
        background-color: #3f3f3f;
        color: #ffffff;
        padding: 5px 12px;
        border-radius: 15px;
        display: inline-block;
        margin: 3px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อ Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ กรุณาตั้งค่า GROQ_API_KEY ใน Secrets ก่อนครับ")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="seo-title">🎥 JAAO YOUTUBE SEO PRO</h1>', unsafe_allow_html=True)
st.write("---")

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📊 วิเคราะห์คลิปของคุณ")
    video_topic = st.text_input("หัวข้อคลิป หรือ เนื้อหาเพลง:", placeholder="เช่น เพลงลูกทุ่งอกหักสู้ชีวิต, สอนใช้ AI สร้างภาพ")
    target_group = st.selectbox("กลุ่มเป้าหมาย:", ["คนฟังเพลงทั่วไป", "วัยรุ่น/วัยทำงาน", "สายเทคโนโลยี/AI", "เด็ก/ครอบครัว"])
    
    st.write("🔍 **ตัวเลือกเสริม:**")
    include_emoji = st.checkbox("ใส่ Emoji ในชื่อคลิปด้วย", value=True)
    high_click = st.checkbox("เน้นชื่อคลิปแบบ Clickbait (เน้นยอดคลิก)", value=False)

    run_seo = st.button("🚀 วิเคราะห์และตั้งค่า SEO")

with col_out:
    if run_seo:
        if video_topic:
            with st.spinner("⏳ กำลังเจาะระบบ Algorithm ของ YouTube..."):
                try:
                    # สั่ง Llama 3 ให้ทำ SEO แบบมืออาชีพ
                    prompt = f"""
                    ในฐานะผู้เชี่ยวชาญ YouTube SEO ช่วยวิเคราะห์เนื้อหา: '{video_topic}' สำหรับกลุ่มเป้าหมาย {target_group}
                    โดยให้ข้อมูลดังนี้:
                    1. [TITLE]: เสนอชื่อคลิป 3 แบบ (น่าสนใจ/ทางการ/เน้นยอดวิว)
                    2. [DESCRIPTION]: คำอธิบายคลิปสั้นๆ พร้อมใส่ Keyword สำคัญ
                    3. [TAGS]: ชุดแท็ก 15 คำ (แยกด้วยคอมม่า)
                    4. [THUMBNAIL]: ไอเดียภาพหน้าปกที่ดึงดูดสายตา
                    5. [TIPS]: เทคนิคพิเศษเฉพาะคลิปนี้
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    
                    result = completion.choices[0].message.content
                    
                    st.success("วิเคราะห์เสร็จแล้ว! นำไปใช้ได้เลย")
                    
                    # แสดงผลแบบแยกหมวดหมู่
                    if "[TITLE]" in result:
                        st.markdown("### 🏷️ ชื่อคลิปที่แนะนำ:")
                        st.code(result.split("[TITLE]")[1].split("[DESCRIPTION]")[0].strip())
                        
                        st.markdown("### 📝 คำอธิบาย (Description):")
                        st.info(result.split("[DESCRIPTION]")[1].split("[TAGS]")[0].strip())
                        
                        st.markdown("### 🏷️ แท็กที่ควรใส่ (Tags):")
                        tags_raw = result.split("[TAGS]")[1].split("[THUMBNAIL]")[0].strip()
                        st.code(tags_raw) # ให้พี่ก๊อปไปวางในช่อง Tags ของ YouTube
                        
                        st.markdown("### 🖼️ ไอเดียหน้าปก:")
                        st.warning(result.split("[THUMBNAIL]")[1].split("[TIPS]")[0].strip())
                    else:
                        st.write(result)
                        
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("ใส่หัวข้อคลิปก่อนครับพี่ JAAO")

st.write("---")
st.caption("© 2026 JAAO SEO Studio | ดันช่องของคุณให้พุ่งทะลุล้านวิว")

