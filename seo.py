import streamlit as st
import google.generativeai as genai
import datetime
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO SEO Pro v.2.5", page_icon="🎥", layout="wide")

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
</style>
""", unsafe_allow_html=True)

# 2. เชื่อมต่อ Gemini API
try:
    # ใช้คีย์เดียวกับแอปแรกได้เลยครับ
    API_KEY = st.secrets["MY_API_KEY"] 
    genai.configure(api_key=API_KEY)
    # ใช้รุ่น 1.5-flash เพื่อโควตาที่เยอะและเสถียร
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ ไม่พบ MY_API_KEY ใน Secrets ครับ!")
    st.stop()

# 3. หน้าจอหลัก
st.markdown('<h1 class="seo-title">🎥 JAAO SEO MASTER (GEMINI)</h1>', unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.3])

with col_in:
    st.subheader("🔗 วิเคราะห์ข้อมูลคลิป")
    yt_url = st.text_input("วางลิงก์ YouTube:", placeholder="https://www.youtube.com/watch?v=...")
    music_detail = st.text_area("✍️ ใส่เนื้อร้องหรือรายละเอียดเพลง:", height=200)
    music_style = st.selectbox("🎸 แนวเพลง:", ["ลูกทุ่งอินดี้", "เพื่อชีวิต", "ร็อก/สตริง", "ป็อป", "แร็ป"])
    
    analyze_btn = st.button("🚀 วิเคราะห์ SEO (Gemini)")

with col_out:
    if analyze_btn:
        if yt_url or music_detail:
            with st.spinner("⏳ ผมกำลังวิเคราะห์ SEO ให้พี่อย่างละเอียด..."):
                try:
                    prompt = f"""
                    วิเคราะห์วิดีโอจาก ลิงก์: {yt_url} และเนื้อหา: "{music_detail}" แนว {music_style}
                    ในฐานะผู้เชี่ยวชาญ YouTube SEO ช่วยจัดลำดับความสำคัญให้คนหาเจอง่ายๆ
                    
                    รูปแบบการตอบ (สำคัญมาก):
                    [TITLE]: ชื่อคลิป 1 ชื่อที่ต้องกดดู
                    [DESC]: คำอธิบายคลิป 3 บรรทัดแรก
                    [TAGS]: เฉพาะคำค้นหาคั่นด้วยคอมม่าเท่านั้น ห้ามมีเลข ห้ามมีคำอธิบาย
                    [HASHTAGS]: เฉพาะคำที่เริ่มด้วย # คั่นด้วยช่องว่าง
                    """
                    
                    response = model.generate_content(prompt)
                    res = response.text
                    st.success("เรียบร้อยครับพี่ JAAO!")

                    # แยกข้อมูลมาโชว์
                    try:
                        title_val = res.split("[TITLE]")[1].split("[DESC]")[0].strip()
                        desc_val = res.split("[DESC]")[1].split("[TAGS]")[0].strip()
                        tags_val = res.split("[TAGS]")[1].split("[HASHTAGS]")[0].strip()
                        hash_val = res.split("[HASHTAGS]")[1].strip()
                        
                        st.markdown('<p class="tag-label">🎯 ชื่อคลิปแนะนำ:</p>', unsafe_allow_html=True)
                        st.info(title_val)

                        st.markdown('<p class="tag-label">🏷️ Tags (สะอาด ก๊อปไปวางได้เลย):</p>', unsafe_allow_html=True)
                        st.code(tags_val, language="text") 
                        
                        st.markdown('<p class="tag-label">#️⃣ Hashtags:</p>', unsafe_allow_html=True)
                        st.code(hash_val, language="text")
                        
                        st.markdown('<p class="tag-label">📝 คำอธิบาย:</p>', unsafe_allow_html=True)
                        st.write(desc_val)
                    except:
                        st.write(res)

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("ใส่ข้อมูลก่อนครับพี่")

st.write("---")
st.caption("Powered by Gemini AI | วิเคราะห์ลึก แม่นยำ เพื่อพี่ JAAO โดยเฉพาะ")
