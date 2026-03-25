import streamlit as st
from groq import Groq
import datetime
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO SEO Pro v.2.3", page_icon="🎥", layout="wide")

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; color: #ffffff; }
    .seo-title { color: #ff0000 !important; text-align: center; font-size: 40px !important; font-weight: 900 !important; }
    div.stButton > button:first-child {
        background-color: #ff0000 !important; color: white !important;
        height: 60px; font-size: 20px; font-weight: bold; border-radius: 30px; width: 100%;
    }
    .tag-label { color: #00f2ff; font-weight: bold; font-size: 18px; margin-bottom: 5px; }
    .instruction { color: #888; font-size: 12px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อ Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ ตรวจสอบ GROQ_API_KEY ใน Secrets ด้วยครับ")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="seo-title">🎥 JAAO SEO CLEAN COPY v.2.3</h1>', unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.3])

with col_in:
    st.subheader("🎵 ข้อมูลเพลง")
    music_detail = st.text_area("✍️ ใส่เนื้อร้องหรือรายละเอียดเพลง:", 
                                 placeholder="วางเนื้อเพลงตรงนี้ เพื่อให้ AI วิเคราะห์คำค้นหาที่แม่นยำที่สุด...", height=250)
    
    music_style = st.selectbox("🎸 แนวเพลง:", ["ลูกทุ่งอินดี้", "เพื่อชีวิต", "ร็อก/สตริง", "ป็อป", "แร็ป"])
    
    analyze_btn = st.button("🚀 วิเคราะห์และสร้าง Tags")

with col_out:
    if analyze_btn:
        if music_detail:
            with st.spinner("⏳ กำลังเตรียม Tags แบบสะอาด..."):
                try:
                    # สั่ง AI แบบเข้มงวดเรื่องรูปแบบข้อมูล (Strict Format)
                    prompt = f"""
                    ในฐานะ YouTube SEO Expert ช่วยสร้าง Tags และ Hashtags จากเนื้อหา: "{music_detail}" แนว {music_style}
                    
                    กฎเหล็ก:
                    1. ในส่วน [TAGS] ให้ตอบ "เฉพาะคำค้นหาที่คั่นด้วยคอมม่าเท่านั้น" ห้ามมีคำนำหน้า ห้ามมีเลขลำดับ ห้ามมีคำอธิบายเพิ่ม
                    2. ในส่วน [HASHTAGS] ให้ตอบ "เฉพาะคำที่เริ่มด้วย # เท่านั้น" คั่นด้วยช่องว่าง
                    3. ในส่วน [TITLE] ให้เสนอชื่อคลิปสั้นๆ 1 ชื่อ
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    
                    res = completion.choices[0].message.content
                    st.success("สร้างข้อมูลเสร็จแล้ว! ก๊อปปี้ไปใช้งานได้เลย")

                    # ดึงข้อมูลออกมาแสดงผลแบบสะอาดที่สุด
                    try:
                        title_part = res.split("[TITLE]")[1].split("[TAGS]")[0].strip()
                        tags_part = res.split("[TAGS]")[1].split("[HASHTAGS]")[0].strip()
                        hash_part = res.split("[HASHTAGS]")[1].strip()
                        
                        st.markdown('<p class="tag-label">🎯 ชื่อคลิปที่แนะนำ:</p>', unsafe_allow_html=True)
                        st.info(title_part)

                        st.markdown('<p class="tag-label">🏷️ YouTube Tags (ก๊อปไปวางช่องแท็กได้เลย):</p>', unsafe_allow_html=True)
                        st.markdown('<p class="instruction">*วางแล้วระบบจะแยกคำให้เองอัตโนมัติ</p>', unsafe_allow_html=True)
                        st.code(tags_part, language="text") # ช่องนี้จะสะอาดมาก มีแค่คำคั่นด้วยคอมม่า
                        
                        st.markdown('<p class="tag-label">#️⃣ Hashtags (สำหรับใต้โพสต์):</p>', unsafe_allow_html=True)
                        st.code(hash_part, language="text")
                        
                    except:
                        st.write(res) # กรณี AI ผิดพลาด ให้โชว์ผลลัพธ์ทั้งหมด

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาใส่เนื้อเพลงก่อนครับพี่")

st.write("---")
st.caption("© 2026 JAAO SEO Studio | ข้อมูลสะอาด ใช้ง่าย วิเคราะห์ตรงจุด")
