import streamlit as st
from groq import Groq
import datetime
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO YouTube SEO Pro v.2.2", page_icon="🎥", layout="wide")

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; color: #ffffff; }
    .seo-title { color: #ff0000 !important; text-align: center; font-size: 40px !important; font-weight: 900 !important; }
    div.stButton > button:first-child {
        background-color: #ff0000 !important; color: white !important;
        height: 60px; font-size: 20px; font-weight: bold; border-radius: 30px; width: 100%;
    }
    .result-section { background-color: #1e1e1e; padding: 25px; border-radius: 15px; border: 1px solid #444; margin-top: 20px; }
    .tag-label { color: #ff4b4b; font-weight: bold; font-size: 18px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อ Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ ตรวจสอบ GROQ_API_KEY ใน Secrets ด้วยครับ")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="seo-title">🎥 JAAO MUSIC SEO ANALYZER v.2.2</h1>', unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.3])

with col_in:
    st.subheader("🎵 ป้อนข้อมูลเพื่อวิเคราะห์เชิงลึก")
    yt_url = st.text_input("🔗 ลิงก์ YouTube (ถ้ามี):", placeholder="https://www.youtube.com/watch?v=...")
    
    # ส่วนนี้สำคัญมากเพื่อให้ AI วิเคราะห์ได้ตรงเนื้อหาที่สุด
    music_detail = st.text_area("✍️ เนื้อร้องหรือรายละเอียดเพลง (ใส่เยอะยิ่งแม่น):", 
                                 placeholder="ใส่เนื้อเพลง หรือเล่าว่าเพลงเกี่ยวกับอะไร...", height=200)
    
    music_style = st.selectbox("🎸 แนวเพลงหลัก:", 
                                ["ลูกทุ่งอินดี้", "ลูกทุ่งคลาสสิก", "เพื่อชีวิต", "ร็อก/สตริง", "ป็อปสบายๆ", "แร็ป/ฮิปฮอป"])
    
    analyze_btn = st.button("🚀 วิเคราะห์ SEO แบบละเอียด")

with col_out:
    if analyze_btn:
        if music_detail or yt_url:
            with st.spinner("⏳ AI กำลังเจาะลึกเนื้อหาและวางกลยุทธ์ SEO..."):
                try:
                    # สั่ง AI ให้วิเคราะห์ละเอียดแบบเจาะจงเนื้อหา
                    prompt = f"""
                    ในฐานะผู้เชี่ยวชาญ YouTube Music Marketing ช่วยวิเคราะห์เพลงแนว {music_style} 
                    จากข้อมูลเนื้อหา/เนื้อร้อง: "{music_detail}" (ลิงก์อ้างอิง: {yt_url})
                    
                    ให้ผลลัพธ์ที่ละเอียดที่สุดตามหมวดหมู่ดังนี้:
                    1. [ANALYSIS]: วิเคราะห์จุดเด่นของเนื้อหาเพลงและอารมณ์เพลง (Mood & Tone)
                    2. [TITLE_MASTER]: เสนอชื่อคลิป 3 แบบที่ดึงดูดกลุ่มเป้าหมาย (ใช้คำที่คนชอบค้นหา)
                    3. [DESCRIPTION]: เขียนคำอธิบายคลิปแบบ SEO-Friendly (ยาวและละเอียด) ใส่ Keyword แฝง
                    4. [TAGS_COLLECTION]: ชุด Tags 25 คำ สำหรับช่อง YouTube Tags (แยกด้วยคอมม่า)
                    5. [HASHTAGS]: ชุด #Hashtag 10 คำ สำหรับใส่ท้ายคำอธิบาย (เริ่มด้วย #)
                    6. [THUMBNAIL]: ไอเดียการจัดวางรูปปก สีที่ควรใช้ และข้อความที่ควรมีบนปก
                    
                    เน้นภาษาไทยที่ทันสมัยและกระตุ้นให้คนอยากคลิกดู
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    
                    res = completion.choices[0].message.content
                    st.success("วิเคราะห์เสร็จเรียบร้อย! ข้อมูลแม่นยำขึ้น 100% 🎉")
                    
                    # แสดงผลแยกหมวดหมู่ให้ก๊อปปี้ง่ายๆ
                    if "[TAGS_COLLECTION]" in res:
                        st.markdown('<p class="tag-label">🏷️ YouTube Tags (สำหรับหลังบ้าน):</p>', unsafe_allow_html=True)
                        tags = res.split("[TAGS_COLLECTION]")[1].split("[HASHTAGS]")[0].strip()
                        st.code(tags)
                        
                        st.markdown('<p class="tag-label">#️⃣ Hashtags (สำหรับใต้โพสต์):</p>', unsafe_allow_html=True)
                        hashtags = res.split("[HASHTAGS]")[1].split("[THUMBNAIL]")[0].strip()
                        st.code(hashtags)
                        
                        st.markdown("### 📝 รายละเอียดการวิเคราะห์:")
                        st.write(res.split("[TAGS_COLLECTION]")[0].replace("[ANALYSIS]","").replace("[TITLE_MASTER]","### 🏷️ ชื่อที่แนะนำ").replace("[DESCRIPTION]","### 📝 คำอธิบาย").strip())
                        
                        st.markdown("### 🖼️ ไอเดียหน้าปก:")
                        st.warning(res.split("[THUMBNAIL]")[1].strip())
                    else:
                        st.write(res)

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาใส่เนื้อร้องหรือรายละเอียดเพลง เพื่อความแม่นยำในการวิเคราะห์ครับ")

st.write("---")
st.caption("© 2026 JAAO SEO Studio v.2.2 | วิเคราะห์ลึกถึงอารมณ์เพลง")
