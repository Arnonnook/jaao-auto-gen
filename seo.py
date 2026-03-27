import streamlit as st
import google.generativeai as genai
import json

# --- 1. การตั้งค่าหน้าจอ ---
st.set_page_config(page_title="JAAO YouTube SEO Pro v3.0", page_icon="🚀")

# ใส่ API Key ของคุณตรงนี้
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY" 
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. ส่วนหัวแอป ---
st.title("🚀 JAAO YouTube SEO Pro v3.0")
st.subheader("วิเคราะห์ SEO วิดีโอเพลง/คอนเทนต์ แบบแม่นยำ")

# --- 3. ส่วนรับข้อมูล (Input) ---
with st.container():
    lyrics_input = st.text_area("✍️ ใส่เนื้อร้องหรือรายละเอียดเพิ่มเติม (ถ้ามี):", 
                                placeholder="วางเนื้อเพลงที่นี่...", height=200)
    
    genre_selection = st.selectbox("🎸 แนวเพลง/ประเภทคอนเทนต์:", 
                                   ["ร็อก/สตริง", "ลูกทุ่ง/หมอลำ", "ป๊อป/อินดี้", "ฮิปฮอป/แร็ป", "Vlog/รีวิว", "สอนใช้งาน/Education"])

# --- 4. ฟังก์ชันวิเคราะห์ SEO ---
def analyze_seo(text, genre):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prompt ที่รัดกุมเพื่อป้องกัน AI ตอบนอกเรื่องหรือส่งค่าว่าง
    prompt = f"""
    คุณคือผู้เชี่ยวชาญด้าน YouTube SEO สำหรับตลาดเมืองไทย
    ข้อมูลที่ให้มา: {text}
    หมวดหมู่: {genre}

    ภารกิจ: วิเคราะห์และสร้างข้อมูล SEO โดยตอบกลับเป็นรูปแบบ JSON เท่านั้น ห้ามมีข้อความอื่นปน
    โครงสร้าง JSON:
    {{
      "title": "ชื่อคลิปที่ดึงดูดและมี Keyword สำคัญ 1-2 ชื่อ",
      "description": "คำอธิบายคลิปสั้นๆ แต่น่าสนใจ พร้อมใส่ Keyword",
      "tags": "ลิสต์คำค้นหา 15 คำ แยกด้วยเครื่องหมายจุลภาค , ",
      "hashtags": "#แท็ก1 #แท็ก2 #แท็ก3"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # ล้าง Tag ```json ออกถ้า AI ใส่มา
        clean_response = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_response)
    except Exception as e:
        return None

# --- 5. ปุ่มกดและส่วนแสดงผล ---
if st.button("🚀 วิเคราะห์ SEO จากวิดีโอนี้", type="primary", use_container_width=True):
    if lyrics_input.strip() == "":
        st.warning("⚠️ กรุณาใส่เนื้อหาหรือรายละเอียดก่อนครับ")
    else:
        with st.spinner('กำลังวิเคราะห์ด้วย Gemini AI...'):
            result = analyze_seo(lyrics_input, genre_selection)
            
            if result:
                st.success("✅ วิเคราะห์เสร็จเรียบร้อยครับ!")
                
                # แสดงผลแบ่งเป็นสัดส่วน
                st.markdown("### 🎯 ชื่อที่แนะนำ:")
                st.info(result.get("title", "ไม่พบข้อมูล"))
                
                st.markdown("### 📝 คำอธิบาย (Description):")
                st.write(result.get("description", "ไม่พบข้อมูล"))
                
                st.markdown("### 🏷️ Tags (สะอาด ก๊อปไปวางได้เลย):")
                st.code(result.get("tags", "ไม่พบข้อมูล"))
                
                st.markdown("### #️⃣ Hashtags:")
                st.code(result.get("hashtags", "ไม่พบข้อมูล"))
            else:
                st.error("❌ เกิดข้อผิดพลาดในการวิเคราะห์ โปรดลองใหม่อีกครั้ง")

# --- 6. ส่วนท้ายหน้า ---
st.divider()
st.caption("พัฒนาโดย JAAO AI Assistant | ขุมพลังจาก Gemini 1.5 Flash")
