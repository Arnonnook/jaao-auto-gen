import streamlit as st
from groq import Groq
import datetime
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO SEO Pro v.2.4", page_icon="🎥", layout="wide")

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
st.markdown('<h1 class="seo-title">🎥 JAAO SEO & LINK ANALYZER v.2.4</h1>', unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.3])

with col_in:
    st.subheader("🔗 ข้อมูลวิดีโอ/เพลง")
    # เอากลับมาแล้วครับ ช่องใส่ลิงก์
    yt_url = st.text_input("วางลิงก์ YouTube (ถ้ามี):", placeholder="https://www.youtube.com/watch?v=...")
    
    music_detail = st.text_area("✍️ ใส่เนื้อร้องหรือรายละเอียดเพลง (แนะนำ):", 
                                 placeholder="วางเนื้อเพลงที่นี่ เพื่อความแม่นยำสูงสุด...", height=200)
    
    music_style = st.selectbox("🎸 แนวเพลง:", ["ลูกทุ่งอินดี้", "เพื่อชีวิต", "ร็อก/สตริง", "ป็อป", "แร็ป"])
    
    analyze_btn = st.button("🚀 วิเคราะห์และสร้าง Tags")

with col_out:
    if analyze_btn:
        if yt_url or music_detail:
            with st.spinner("⏳ AI กำลังแกะรหัส SEO และเตรียมข้อมูลแบบสะอาด..."):
                try:
                    # สั่ง AI แบบ Strict เรื่องความสะอาดของผลลัพธ์
                    prompt = f"""
                    ในฐานะ YouTube SEO Expert ช่วยวิเคราะห์วิดีโอจาก ลิงก์: {yt_url} และเนื้อหา: "{music_detail}" แนว {music_style}
                    
                    กฎเหล็กในการตอบ:
                    1. [TAGS]: ให้ตอบ "เฉพาะคำค้นหาที่คั่นด้วยคอมม่าเท่านั้น" ห้ามมีคำอธิบาย ห้ามมีเลขลำดับ ห้ามมีคำนำหน้า
                    2. [HASHTAGS]: ให้ตอบ "เฉพาะคำที่เริ่มด้วย # เท่านั้น" คั่นด้วยช่องว่าง
                    3. [TITLE]: เสนอชื่อคลิปที่ดึงดูด 1 ชื่อ
                    4. [DESC]: เขียนคำอธิบายสั้นๆ 3 บรรทัด
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    
                    res = completion.choices[0].message.content
                    st.success("สร้างข้อมูลเสร็จแล้วครับ!")

                    # แยกข้อมูลมาโชว์แบบก๊อปปี้ง่าย
                    try:
                        title_val = res.split("[TITLE]")[1].split("[DESC]")[0].strip()
                        desc_val = res.split("[DESC]")[1].split("[TAGS]")[0].strip()
                        tags_val = res.split("[TAGS]")[1].split("[HASHTAGS]")[0].strip()
                        hash_val = res.split("[HASHTAGS]")[1].strip()
                        
                        st.markdown('<p class="tag-label">🎯 ชื่อคลิปที่แนะนำ:</p>', unsafe_allow_html=True)
                        st.info(title_val)

                        st.markdown('<p class="tag-label">📝 คำอธิบาย (Description):</p>', unsafe_allow_html=True)
                        st.write(desc_val)

                        st.markdown('<p class="tag-label">🏷️ YouTube Tags (สะอาด 100% ก๊อปไปวางได้เลย):</p>', unsafe_allow_html=True)
                        st.code(tags_val, language="text") 
                        
                        st.markdown('<p class="tag-label">#️⃣ Hashtags (สำหรับใต้โพสต์):</p>', unsafe_allow_html=True)
                        st.code(hash_val, language="text")
                        
                    except:
                        st.write(res) # กรณี AI รูปแบบเพี้ยน

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาใส่ลิงก์ หรือเนื้อเพลงก่อนครับพี่ JAAO")

st.write("---")
st.caption("© 2026 JAAO SEO Studio | ข้อมูลสะอาด ใช้ง่าย มีช่องใส่ลิงก์")
