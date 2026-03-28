import streamlit as st
import google.generativeai as genai

st.title("🎵 JAAO Auto Gen")

# สร้างช่องกรอก Key บนหน้าเว็บ
api_key = st.text_input("กรุณาใส่ Gemini API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        topic = st.text_input("อยากแต่งเพลงเรื่องอะไร:")
        if st.button("เริ่มแต่งเพลง"):
            response = model.generate_content(f"แต่งเพลงไทยพร้อมคอร์ดเรื่อง {topic}")
            st.write(response.text)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.warning("ใส่ API Key ก่อนนะครับจ๊ะโอ๋")

