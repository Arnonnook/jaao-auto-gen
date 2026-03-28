import streamlit as st
import google.generativeai as genai

# --- 1. ตั้งค่าหน้าแอป (Config & Style) ---
st.set_page_config(
    page_title="🎶 JAAO Auto Gen - Thai Songwriter AI",
    page_icon="🎵",
    layout="wide"
)

# เพิ่ม CSS เล็กน้อยเพื่อสีสัน (Option: จ๊ะโอ๋ปรับสีตามชอบได้ที่นี่)
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6; /* สีพื้นหลัง */
    }
    .stSelectbox, .stTextInput, .stButton {
        border-radius: 10px; /* ขอบมน */
    }
    .stButton>button {
        background-color: #FF4B4B; /* สีปุ่มหลัก */
        color: white;
    }
    .stCodeBlock {
        background-color: #262730; /* สีพื้นหลังกล่องคอร์ด */
        color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. หน้าตาแอป (UI Structure) ---
col1, col2 = st.columns([1, 2]) # แบ่งเป็น 2 คอลัมน์ (ซ้ายเล็ก, ขวากว้าง)

with col1:
    st.image("https://img.icons8.com/fluent/96/000000/music-conductor.png", width=64) # ใส่ไอคอนน่ารักๆ
    st.title("🎶 JAAO Auto Gen")
    st.write("ช่วยคุณแต่งเพลงไทยพร้อมคอร์ดแบบง่ายๆ!")
    st.markdown("---")
    
    # --- ส่วนที่ 1: ใส่ API Key ---
    st.markdown("### 🔑 ขั้นตอนที่ 1: ใส่ Key")
    # แนะนำให้ใช้ st.secrets เพื่อความปลอดภัย แต่ถ้าทำผ่านหน้าเว็บใช้ช่องกรอกก็ได้ครับ
    # ในหน้า Streamlit Cloud จ๊ะโอ๋ไปที่ Settings -> Secrets -> ใส่ [google] api_key = "..."
    if "google" in st.secrets:
        api_key = st.secrets.google["api_key"]
        st.success("API Key เชื่อมต่อแล้ว (จาก Secrets) ✅")
    else:
        api_key = st.text_input("ใส่ Gemini API Key ของคุณ:", type="password", placeholder="AIzaSy...")
        st.info("หากยังไม่มี Key ไปเอาได้ที่ [Google AI Studio](https://aistudio.google.com/) (ฟรี)")
    
    st.markdown("---")

    # --- ส่วนที่ 2: เลือกสไตล์และแนวเพลง (ตัวเลือกเยอะๆ และแบ่งช่องสไตล์) ---
    st.markdown("### 🎼 ขั้นตอนที่ 2: เลือกสไตล์และแนวเพลง")
    
    # แบ่งช่องสไตล์
    main_style = st.selectbox(
        "สไตล์ดนตรีหลัก:",
        ["🎤 T-Pop / Mainstream", "🌾 ลูกทุ่ง / หมอลำ", "🎸 Indie / Alternative", "🤘 Rock / Metal"]
    )
    
    # แสดงแนวเพลงตามสไตล์ที่เลือก
    thai_genres = []
    if main_style == "🎤 T-Pop / Mainstream":
        thai_genres = ["T-Pop (ไอดอล)", "Ballad (เพลงรักเศร้าๆ)", "Rap/Hip-hop ไทย", "City Pop ไทย (เหงาๆ)"]
    elif main_style == "🌾 ลูกทุ่ง / หมอลำ":
        thai_genres = ["ลูกทุ่งอินดี้ (กินใจ)", "ลูกทุ่งแดนซ์", "ลูกทุ่งหมอลำ (ซิ่ง)", "ลูกทุ่งวิถีชีวิต"]
    elif main_style == "🎸 Indie / Alternative":
        thai_genres = ["Thai Indie (เพลงนอกกระแส)", "Indie Pop (ชิลล์ๆ)", "Alternative Rock (ดื้อๆ)", "Post-Rock (บรรยากาศ)"]
    elif main_style == "🤘 Rock / Metal":
        thai_genres = ["Thai Rock (รักกระแทกใจ)", "Hard Rock", "Heavy Metal", "Metalcore"]

    selected_genre = st.selectbox("เลือกแนวเพลงเฉพาะ:", thai_genres)
    
    st.markdown("---")
    
    # --- ส่วนที่ 3: ใส่หัวข้อ ---
    st.markdown("### 📝 ขั้นตอนที่ 3: ใส่เรื่องราว")
    topic = st.text_input("แต่งเพลงเกี่ยวกับอะไร:", placeholder="เช่น รักครั้งแรก, อกหักตอนฝนตก")
    
    # ปุ่มเริ่มแต่ง
    start_btn = st.button("รังสรรค์เนื้อเพลง ✨", use_container_width=True)

# --- คอลัมน์ด้านขวา (แสดงผลลัพธ์) ---
with col2:
    st.markdown("## 📖 ผลลัพธ์เนื้อเพลง")
    if start_btn:
        if not api_key:
            st.warning("กรุณาใส่ API Key ก่อนนะครับจ๊ะโอ๋!")
        elif not topic:
            st.warning("บอกหน่อยสิว่าอยากแต่งเพลงเรื่องอะไร?")
        else:
            with st.spinner(f'AI กำลังแต่งเพลงแนว {selected_genre} เรื่อง "{topic}" ให้จ๊ะโอ๋...'):
                genai.configure(api_key=api_key)
                
                prompt = f"""
                คุณเป็นนักแต่งเพลงมืออาชีพในไทย ที่เข้าใจกระแสนิยมปัจจุบัน
                ช่วยแต่งเนื้อเพลงแนว {selected_genre} เรื่อง "{topic}" โดยมีเงื่อนไขดังนี้:
                1. ใส่คอร์ดกีตาร์ประกอบ (เช่น [C] [Am] [F] [G]) ไว้เหนือเนื้อร้อง
                2. ใช้ชุดคอร์ดที่คนไทยชอบฟัง ไพเราะ และเข้ากับแนวเพลง
                3. โครงสร้างเพลงต้องมี: Verse 1, Pre-Chorus, Chorus (ต้องโดนใจ), Verse 2, Bridge, และ Outro
                4. ภาษาที่ใช้ต้องสละสลวย เข้ากับกลุ่มเป้าหมายในไทย และมี "ท่อนฮุค" ที่จำง่าย
                """
                
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(prompt)
                    
                    st.success("แต่งเสร็จแล้ว! กดปุ่ม 'ก๊อปปี้' ตรงมุมขวาบนของเนื้อเพลงเพื่อนำไปใช้ได้เลย")
                    
                    # --- ส่วนที่ 4: แสดงผลและก๊อปปี้ (ด้วย st.code) ---
                    # ใช้ st.code เพื่อให้ได้ช่องสไตล์คอร์ด และมีปุ่มก๊อปปี้ให้โดยอัตโนมัติ
                    st.markdown("---")
                    st.code(response.text, language="markdown")
                    
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.markdown(
            """
            <div style="background-color: #fff; padding: 20px; border-radius: 10px; border: 1px solid #ddd; text-align: center;">
                <img src="https://img.icons8.com/fluent/96/000000/waiting-room.png" width="96"/>
                <br><br>
                <h5>กรอกข้อมูลด้านซ้าย แล้วกดปุ่ม 'รังสรรค์เนื้อเพลง ✨' นะครับจ๊ะโอ๋</h5>
                <p style="color: #666;">เนื้อเพลงพร้อมคอร์ดจะปรากฏตรงนี้ครับ</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

# --- ท้ายแอป ---
st.markdown("---")
st.write("Developed by JAAO Studio | Powered by Gemini AI")
