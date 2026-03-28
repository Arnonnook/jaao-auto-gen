import streamlit as st
import google.generativeai as genai

# --- RAINBOW CONFIG & STYLE ---
st.set_page_config(page_title="JAAO Suno Helper", page_icon="🌈", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(120deg, #ff9a9e, #fecfef, #a1c4fd, #c2e9fb); }
    .rainbow-title { font-weight: bold; background: linear-gradient(to right, red, orange, #e6b800, green, blue, indigo, violet); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 35px; }
    .stButton>button { background: linear-gradient(45deg, #ff2400, #ffeb00, #00ced1, #9370db); color: white; border-radius: 20px; border: none; font-weight: bold; }
    .copy-label { background-color: #ffffff; padding: 5px 15px; border-radius: 10px; font-weight: bold; color: #333; margin-bottom: 5px; display: inline-block; border: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='rainbow-title'>JAAO Studio</h1>", unsafe_allow_html=True)
    api_key = st.text_input("Gemini API Key:", type="password")
    st.divider()
    
    artist_name = st.text_input("Artist Name:", placeholder="e.g. JAAO, WARIN")
    song_topic = st.text_input("Topic / Story:", placeholder="เช่น แอบรักเพื่อนแต่ไม่กล้าบอก")
    
    st.subheader("🎵 Select Style")
    main_style = st.selectbox("Category:", ["Pop", "Country / Folk", "Indie / Rock", "Hip Hop / R&B"])
    sub_styles = {
        "Pop": ["T-Pop Idol", "Modern Ballad", "Synth Pop", "City Pop"],
        "Country / Folk": ["Thai Country Indie", "Modern Luk Thung", "Folk Song", "Puea Chiwit"],
        "Indie / Rock": ["Alternative Indie", "Shoegaze", "Thai Rock", "Modern Rock"],
        "Hip Hop / R&B": ["Trap", "Old School Hip Hop", "R&B / Soul", "Lo-fi Hip Hop"]
    }
    selected_style = st.selectbox("Specific Genre:", sub_styles[main_style])

    generate_btn = st.button("รังสรรค์เพลงสำหรับ Suno ✨")

# --- MAIN AREA ---
if generate_btn:
    if not api_key:
        st.error("กรุณาใส่ API Key")
    elif not song_topic:
        st.error("กรุณาใส่ Topic")
    else:
        with st.spinner('กำลังปรุงแต่งเพลง...'):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # สั่ง AI แยกส่วนชัดเจน
                prompt = f"""
                Task: Create a song for Suno AI.
                Artist: {artist_name}
                Topic: {song_topic}
                Style: {selected_style}
                
                Output Format:
                1. Suggested Song Title (Thai)
                2. Style Prompt (English only, comma separated tags for Suno)
                3. Lyrics with Guitar Chords (Thai, with [C][Am] tags and structure like [Verse][Chorus])
                """
                
                response = model.generate_content(prompt)
                res_text = response.text
                
                # แยกข้อมูลแบบง่ายๆ (AI มักจะแยกหัวข้อมาให้)
                st.balloons()

                # --- ส่วนที่ 1: ชื่อเพลง ---
                st.markdown("<div class='copy-label'>📌 Step 1: Copy Song Title</div>", unsafe_allow_html=True)
                # ค้นหาบรรทัดที่มีคำว่า Title
                title_line = [l for l in res_text.split('\n') if 'Title' in l]
                st.code(title_line[0].replace('Suggested Song Title:', '').replace('1.', '').strip() if title_line else "Song by " + artist_name)

                # --- ส่วนที่ 2: สไตล์สำหรับ Suno ---
                st.markdown("<div class='copy-label'>🎹 Step 2: Copy Style (Suno Prompt)</div>", unsafe_allow_html=True)
                st.code(f"Thai, {selected_style}, catchy, emotional, male/female vocals", language="markdown")

                # --- ส่วนที่ 3: เนื้อเพลง ---
                st.markdown("<div class='copy-label'>📝 Step 3: Copy Lyrics & Chords</div>", unsafe_allow_html=True)
                st.code(res_text, language="markdown")
                
                st.success("ครบถ้วน! ก๊อปปี้ไปวางใน Suno AI ช่อง Custom Mode ได้เลยครับ")
                
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("กรอกข้อมูลด้านซ้ายเพื่อเริ่มสร้างเพลงครับ")

st.markdown("---")
st.caption("🌈 JAAO Studio x Suno AI | Powered by Gemini")
