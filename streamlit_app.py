import streamlit as st
import google.generativeai as genai

# --- 1. SET PAGE & RAINBOW STYLE ---
st.set_page_config(page_title="JAAO Rainbow Song", page_icon="🌈", layout="wide")

st.markdown("""
<style>
    /* พื้นหลังไล่เฉดสีรุ้งอ่อนๆ */
    .stApp {
        background: linear-gradient(120deg, #ff9a9e 0%, #fecfef 20%, #feada6 40%, #fbc2eb 60%, #a1c4fd 80%, #c2e9fb 100%);
    }
    /* หัวข้อสีรุ้ง */
    .rainbow-text {
        font-weight: bold;
        background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px;
    }
    /* ปุ่มกดสีรุ้ง */
    .stButton>button {
        background: linear-gradient(45deg, #ff2400, #ff8c00, #ffeb00, #32cd32, #00ced1, #1e90ff, #9370db);
        color: white;
        border: none;
        border-radius: 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    /* กล่อง Style Analysis */
    .analysis-card {
        background: rgba(255, 255, 255, 0.8);
        padding: 15px;
        border-radius: 15px;
        border-left: 10px solid violet;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (INPUT) ---
with st.sidebar:
    st.markdown("<h1 class='rainbow-text'>JAAO Studio</h1>", unsafe_allow_html=True)
    api_key = st.text_input("ใส่ Gemini API Key:", type="password")
    st.divider()
    
    artist_name = st.text_input("ชื่อศิลปิน (Artist Name):", placeholder="เช่น จ๊ะโอ๋, WARIN")
    song_topic = st.text_input("หัวข้อเพลง (Topic):", placeholder="เช่น รักครั้งแรกที่สยาม")
    
    st.divider()
    
    # Music Style Selection (English Only)
    st.subheader("🎵 Select Music Style")
    main_style = st.selectbox("Category:", ["Pop", "Country / Folk", "Indie / Rock", "Hip Hop / R&B"])
    
    sub_styles = {
        "Pop": ["T-Pop Idol", "Modern Ballad", "Synth Pop", "City Pop"],
        "Country / Folk": ["Thai Country Indie", "Modern Luk Thung", "Folk Song", "Puea Chiwit"],
        "Indie / Rock": ["Alternative Indie", "Shoegaze", "Thai Rock", "Modern Rock"],
        "Hip Hop / R&B": ["Trap", "Old School Hip Hop", "R&B / Soul", "Lo-fi Hip Hop"]
    }
    selected_style = st.selectbox("Specific Genre:", sub_styles[main_style])

    generate_btn = st.button("รังสรรค์เพลงสีรุ้ง ✨")

# --- 3. MAIN DISPLAY ---
st.markdown(f"<h2 style='color: white; text-shadow: 2px 2px 4px #000;'>🎧 Producer: {artist_name if artist_name else 'JAAO Studio'}</h2>", unsafe_allow_html=True)

if generate_btn:
    if not api_key:
        st.error("กรุณาใส่ API Key ก่อนนะครับ")
    elif not song_topic:
        st.error("กรุณาใส่หัวข้อเพลงด้วยครับ")
    else:
        with st.spinner('กำลังปรุงแต่งบทเพลงสีรุ้งให้จ๊ะโอ๋...'):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # สั่งให้ AI เจนเนื้อเพลงและสรุปสไตล์
                prompt = f"""
                แต่งเนื้อเพลงไทยให้ศิลปินชื่อ '{artist_name}' ในสไตล์ '{selected_style}' เรื่อง '{song_topic}'
                โดยให้สรุป Style Summary เป็นภาษาอังกฤษไว้ที่ส่วนท้ายของเนื้อเพลงด้วย
                
                เงื่อนไข:
                1. ใส่คอร์ดกีตาร์ไว้เหนือเนื้อร้อง [C][Am][F][G]
                2. โครงสร้าง: Verse, Chorus, Bridge, Outro
                3. ภาษาไทยทันสมัย สไตล์ {selected_style}
                """
                
                response = model.generate_content(prompt)
                
                # ส่วนแสดงผล Style Analysis
                st.markdown(f"""
                <div class="analysis-card">
                    <h3 style="margin:0;">✨ Style Analysis</h3>
                    <p><b>Genre:</b> {selected_style} | <b>Artist:</b> {artist_name if artist_name else 'JAAO'}</p>
                    <p style="color: #666;">ก๊อปปี้เนื้อเพลงและคอร์ดได้ที่ช่องด้านล่างนี้เลยครับ 👇</p>
                </div>
                """, unsafe_allow_html=True)
                
                # ช่องเนื้อเพลงที่ก๊อปปี้ได้ทันที
                st.code(response.text, language="markdown")
                
                st.balloons() # เอฟเฟกต์ลูกโป่งฉลองแต่งเพลงเสร็จ
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.info("ใส่รายละเอียดทางซ้าย แล้วกดปุ่มสีรุ้งเพื่อเริ่มเลย!")

st.markdown("---")
st.caption("🌈 JAAO Rainbow Auto Gen | Powered by Gemini AI")
