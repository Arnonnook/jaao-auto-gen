import streamlit as st
import google.generativeai as genai

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Auto Gen", page_icon="🎵")
st.title("🎵 JAAO Auto Gen - แต่งเพลงไทยด้วย AI")

# ใส่ API Key (แนะนำให้ใส่ใน Secrets ของ Streamlit ภายหลัง)
api_key = st.text_input("ใส่ Gemini API Key ของคุณ:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    genre = st.selectbox("เลือกแนวเพลงไทยตามกระแส:", 
                        ["T-Pop (สดใส)", "ลูกทุ่งอินดี้ (กินใจ)", "Thai Indie Pop (ละมุน)"])
    
    topic = st.text_input("อยากแต่งเพลงเกี่ยวกับอะไร:", placeholder="เช่น คิดถึงแฟนเก่าตอนฝนตก")

    if st.button("รังสรรค์เนื้อเพลง ✨"):
        with st.spinner('AI กำลังแต่งเพลงให้จ๊ะโอ๋...'):
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"แต่งเนื้อเพลงไทยแนว {genre} เรื่อง {topic} พร้อมใส่คอร์ดกีตาร์กำกับเหนือเนื้อร้อง แบ่งท่อนให้ชัดเจน"
            
            response = model.generate_content(prompt)
            st.markdown("### 📝 เนื้อเพลงของคุณ")
            st.code(response.text, language="markdown")
else:
    st.info("กรุณาใส่ API Key เพื่อเริ่มใช้งานครับ")

