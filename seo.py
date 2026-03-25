import streamlit as st
from groq import Groq
import datetime
import time
import re

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO YouTube SEO Pro", page_icon="🎥", layout="wide")

# --- การตกแต่งด้วย CSS (Dark Mode & YouTube Red) ---
st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; color: #ffffff; }
    .seo-title { color: #ff0000 !important; text-align: center; font-size: 40px !important; font-weight: 900 !important; }
    div.stButton > button:first-child {
        background-color: #ff0000 !important; color: white !important;
        height: 55px; font-size: 18px; font-weight: bold; border-radius: 30px; width: 100%;
    }
    .analysis-card {
        background-color: #1e1e1e; padding: 20px; border-radius: 15px; border-left: 5px solid #ff0000; margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อ Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ อย่าลืมใส่ GROQ_API_KEY ใน Secrets นะครับ!")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="seo-title">🎥 JAAO YOUTUBE LINK ANALYZER</h1>', unsafe_allow_html=True)
st.write("---")

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("🔗 วิเคราะห์จากลิงก์วิดีโอ")
    # ช่องใส่ลิงก์ YouTube
    yt_url = st.text_input("วางลิงก์วิดีโอ YouTube ที่นี่:", placeholder="https://www.youtube.com/watch?v=...")
    
    st.write("หรือ")
    
    video_topic = st.text_area("ระบุหัวข้อ/เนื้อหาคลิป (กรณีไม่มีลิงก์):", height=100)
    
    st.write("---")
    focus_on = st.multiselect("เน้นวิเคราะห์ส่วนไหน:", 
                              ["ชื่อคลิป (Title)", "คำอธิบาย (Description)", "แท็ก (Tags)", "ไอเดียหน้าปก (Thumbnail)"],
                              default=["ชื่อคลิป (Title)", "แท็ก (Tags)"])

    analyze_btn = st.button("🚀 เริ่มวิเคราะห์ SEO ทันที")

with col_right:
    if analyze_btn:
        if yt_url or video_topic:
            with st.spinner("⏳ AI กำลังแกะรหัส SEO ของวิดีโอนี้..."):
                try:
                    # เตรียมข้อมูลส่งให้ AI
                    source_info = yt_url if yt_url else video_topic
                    prompt = f"""
                    วิเคราะห์วิดีโอจากข้อมูลนี้: '{source_info}' 
                    ในฐานะผู้เชี่ยวชาญ YouTube SEO ช่วยวิเคราะห์และเสนอแนะเพื่อเพิ่มยอดวิว (CTR & Ranking):
                    
                    1. [CURRENT_ANALYSIS]: วิเคราะห์ข้อดี/ข้อเสียของ SEO ปัจจุบัน (ถ้าเป็นลิงก์ให้ประเมินจากหัวข้อ)
                    2. [OPTIMIZED_TITLE]: เสนอชื่อคลิปใหม่ 3 แบบที่ดึงดูดใจ (Clickbait แบบมีคุณภาพ)
                    3. [SEO_KEYWORDS]: ชุดแท็ก (Tags) ที่ควรใช้เพื่อดัก Search (แยกด้วยคอมม่า)
                    4. [HOOK_STRATEGY]: แนะนำคำขึ้นต้น Description 2 บรรทัดแรกให้คนอยากกด 'ดูเพิ่มเติม'
                    5. [THUMBNAIL_UPGRADE]: แนะนำการปรับรูปหน้าปกให้เด่นกว่าคู่แข่ง
                    
                    ตอบเป็นภาษาไทยที่เข้าใจง่ายและใช้งานได้จริง
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    
                    result = completion.choices[0].message.content
                    
                    st.success("วิเคราะห์เสร็จสมบูรณ์! 🎉")
                    
                    # แสดงผลแบบแยกส่วน
                    st.markdown("### 📊 ผลการวิเคราะห์กลยุทธ์:")
                    st.write(result)
                    
                    # ทำปุ่มก๊อปปี้แท็กให้พี่ JAAO โดยเฉพาะ
                    if "[SEO_KEYWORDS]" in result:
                        st.write("---")
                        st.subheader("📋 ก๊อปปี้ Tags ไปใช้ได้เลย:")
                        tags = result.split("[SEO_KEYWORDS]")[1].split("[HOOK_STRATEGY]")[0].strip()
                        st.code(tags)

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาใส่ลิงก์ หรือระบุหัวข้อวิดีโอก่อนนะครับพี่")

st.write("---")
st.caption("© 2026 JAAO SEO Studio v.2.0 | วิเคราะห์แม่นยำ ดันยอดวิวให้พุ่ง")
