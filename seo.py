import streamlit as st
import google.generativeai as genai
import json

# --- 1. ตั้งค่า API Key (ดึงจาก Secrets เพื่อความปลอดภัย) ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("❌ ไม่พบ API Key ใน Secrets กรุณาตั้งค่าก่อนครับ")
except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการโหลด API Key: {e}")

# --- 2. หน้าตาแอป (UI) ---
st.set_page_config(page_title="JAAO SEO Pro", page_icon="🚀")
st.title("🚀 JAAO YouTube SEO Pro")
st.markdown("---")

lyrics_input = st.text_area("✍️ ใส่เนื้อร้องหรือรายละเอียดวิดีโอ:", placeholder="วางเนื้อหาที่นี่...", height=200)
genre = st.selectbox("🎸 แนวคอนเทนต์:", ["ร็อก/สตริง", "ลูกทุ่ง/หมอลำ", "ป๊อป/อินดี้", "Vlog/รีวิว", "ทั่วไป"])

# --- 3. ฟังก์ชันวิเคราะห์ ---
def analyze_seo(text, category):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    คุณคือผู้เชี่ยวชาญ YouTube SEO ไทย
    วิเคราะห์เนื้อหานี้: {text}
    หมวดหมู่: {category}
    ตอบกลับเป็น JSON เท่านั้น:
    {{
      "title": "ชื่อคลิปที่น่าสนใจ",
      "tags": "คำค้นหา 1, คำค้นหา 2",
      "hashtags": "#แท็ก1 #แท็ก2"
    }}
    """
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_text)
    except:
        return None

# --- 4. ปุ่มกด ---
if st.button("🚀 วิเคราะห์ SEO", type="primary", use_container_width=True):
    if not lyrics_input:
        st.warning("ใส่เนื้อหาก่อนครับ")
    else:
        with st.spinner("กำลังประมวลผล..."):
            res = analyze_seo(lyrics_input, genre)
            if res:
                st.success("เรียบร้อย!")
                st.subheader("🎯 ชื่อที่แนะนำ:")
                st.info(res['title'])
                st.subheader("🏷️ Tags:")
                st.code(res['tags'])
                st.subheader("#️⃣ Hashtags:")
                st.code(res['hashtags'])
            else:
                st.error("AI วิเคราะห์พลาด ลองใหม่อีกทีครับ")

st.divider()
st.caption("Developed by JAAO AI")
