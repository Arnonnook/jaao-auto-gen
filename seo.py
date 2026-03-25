import streamlit as st
from groq import Groq
import datetime
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO YouTube SEO Pro", page_icon="🎥", layout="wide")

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; color: #ffffff; }
    .seo-title { color: #ff0000 !important; text-align: center; font-size: 40px !important; font-weight: 900 !important; }
    div.stButton > button:first-child {
        background-color: #ff0000 !important; color: white !important;
        height: 55px; font-size: 18px; font-weight: bold; border-radius: 30px; width: 100%;
    }
    .result-section { background-color: #1e1e1e; padding: 20px; border-radius: 15px; margin-top: 20px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อ Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ ตรวจสอบ GROQ_API_KEY ใน Secrets ด้วยครับ")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="seo-title">🎥 JAAO MUSIC SEO ANALYZER</h1>', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("🎵 วิเคราะห์เพลง/วิดีโอ")
    yt_url = st.text_input("วางลิงก์ YouTube ที่นี่:", placeholder="https://www.youtube.com/watch?v=...")
    
    # เพิ่มช่องให้พี่ใส่คำอธิบายสั้นๆ เพื่อให้ AI ทำงานแม่นขึ้น
    extra_info = st.text_input("เพลงนี้แนวไหน? (เช่น ลูกทุ่ง, ร็อก, เพื่อชีวิต):", placeholder="ระบุแนวเพลงสั้นๆ จะแม่นขึ้นมากครับ")
    
    analyze_btn = st.button("🚀 เริ่มวิเคราะห์ SEO สายดนตรี")

with col_right:
    if analyze_btn:
        if yt_url:
            with st.spinner("⏳ กำลังแกะรหัส SEO และแนวเพลง..."):
                try:
                    # ปรับ Prompt ให้ฉลาดเรื่องเพลงมากขึ้น
                    prompt = f"""
                    วิเคราะห์วิดีโอจากลิงก์: {yt_url} 
                    ข้อมูลเพิ่มเติมจากผู้ใช้: {extra_info}
                    
                    ในฐานะ YouTube Music Marketing Expert ช่วยแนะนำ SEO ดังนี้:
                    1. [ANALYSIS]: เพลงนี้ควรเน้น Keyword กลุ่มไหนถึงจะเจอคนฟังที่ใช่
                    2. [BEST_TITLES]: เสนอชื่อคลิป 3 แบบ (เน้นอารมณ์เพลง/เน้นค้นหา/เน้นไวรัล)
                    3. [MUSIC_TAGS]: สร้าง Tags 20 คำ (เน้น: แนวเพลง, อารมณ์เพลง, ชื่อศิลปินที่คล้ายกัน, คำค้นหาฮิตๆ) **แยกด้วยคอมม่า**
                    4. [DESCRIPTION_START]: เขียน Hook 2 บรรทัดแรกให้น่าดึงดูด
                    5. [THUMBNAIL_IDEA]: แนวทางการทำรูปหน้าปกให้ดูเป็นมืออาชีพ
                    
                    ตอบเป็นภาษาไทย และเน้น Tag ที่เกี่ยวข้องกับดนตรีและเพลงโดยเฉพาะ
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    
                    result = completion.choices[0].message.content
                    st.success("วิเคราะห์เสร็จแล้วครับพี่ JAAO!")
                    
                    # แสดงผล
                    if "[MUSIC_TAGS]" in result:
                        parts = result.split("[MUSIC_TAGS]")
                        st.markdown("### 📋 Tags สำหรับสายเพลง (ก๊อปปี้ไปวางได้เลย):")
                        tags_part = parts[1].split("[")[0].strip()
                        st.code(tags_part)
                        
                        st.markdown("### 📝 คำแนะนำอื่นๆ:")
                        st.write(result.replace("[MUSIC_TAGS]" + tags_part, ""))
                    else:
                        st.write(result)

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("วางลิงก์ก่อนครับพี่")
