import streamlit as st
import google.generativeai as genai

# --- 1. ตั้งค่าการเชื่อมต่อ API ---
# พยายามดึง Key จาก Secrets ของ Streamlit
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("⚠️ ไม่พบ GEMINI_API_KEY ใน Secrets กรุณาตั้งค่าก่อนครับ")
except Exception as e:
    st.error(f"❌ Error Loading Secrets: {e}")

# --- 2. ฟังก์ชันวิเคราะห์ SEO (ปรับใหม่ให้เร็วขึ้น) ---
def analyze_seo(text, category):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    คุณคือผู้เชี่ยวชาญ YouTube SEO ไทย
    วิเคราะห์เนื้อหา: {text}
    หมวดหมู่: {category}
    
    ตอบตามรูปแบบนี้เท่านั้น (ห้ามมีข้อความอื่นปน):
    TITLE: [ชื่อคลิปที่น่าสนใจ]
    TAGS: [แท็ก1, แท็ก2, แท็ก3]
    HASH: [#แท็ก1 #แท็ก2 #แท็ก3]
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # แยกข้อมูลออกมาแสดงผล
        res_data = {"title": "", "tags": "", "hashtags": ""}
        for line in content.split('\n'):
            if line.startswith('TITLE:'): res_data['title'] = line.replace('TITLE:', '').strip()
            if line.startswith('TAGS:'): res_data['tags'] = line.replace('TAGS:', '').strip()
            if line.startswith('HASH:'): res_data['hashtags'] = line.replace('HASH:', '').strip()
        return res_data
    except:
        return None

# --- 3. หน้าตาแอป (UI) ---
st.set_page_config(page_title="JAAO SEO Pro", page_icon="🚀")
st.title("🚀 JAAO YouTube SEO Pro")
st.caption("เวอร์ชันใหม่: เร็วขึ้น แม่นยำขึ้น")

lyrics_input = st.text_area("✍️ ใส่เนื้อร้องหรือรายละเอียดวิดีโอ:", placeholder="วางเนื้อเพลงที่นี่...", height=200)
genre = st.selectbox("🎸 แนวคอนเทนต์:", ["ร็อก/สตริง", "ลูกทุ่ง/หมอลำ", "ป๊อป/อินดี้", "Vlog/รีวิว", "ทั่วไป"])

if st.button("🚀 วิเคราะห์ SEO ทันที", type="primary", use_container_width=True):
    if not lyrics_input:
        st.warning("กรุณาใส่เนื้อหาคอนเทนต์ก่อนครับ")
    else:
        with st.spinner("AI กำลังวิเคราะห์..."):
            res = analyze_seo(lyrics_input, genre)
            if res and res['title']:
                st.success("✅ วิเคราะห์เสร็จแล้ว!")
                
                st.subheader("🎯 ชื่อที่แนะนำ")
                st.info(res['title'])
                
                st.subheader("🏷️ Tags (ก๊อปไปวางได้เลย)")
                st.code(res['tags'])
                
                st.subheader("#️⃣ Hashtags")
                st.code(res['hashtags'])
            else:
                st.error("❌ ระบบขัดข้อง หรือ AI ปฏิเสธการวิเคราะห์เนื้อหานี้")

st.divider()
st.caption("Developed by JAAO AI Assistant")
