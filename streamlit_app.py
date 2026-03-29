import streamlit as st
import google.generativeai as genai
import re

# --- 1. SETTINGS & THEME (Pro Appearance) ---
st.set_page_config(page_title="JAAO Suno Helper Pro", page_icon="🎸", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #ffffff; }
    [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255,255,255,0.1); }
    .rainbow-title { 
        font-weight: 800; 
        background: linear-gradient(to right, #00f2fe, #4facfe, #9933ff, #ff3366); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-size: 40px; 
        margin-bottom: 10px;
    }
    .stButton>button { 
        width: 100%;
        background: linear-gradient(90deg, #00f2fe, #4facfe); 
        color: #000; border-radius: 12px; border: none; 
        padding: 12px; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4); color: #fff; }
    .copy-section { background: rgba(255, 255, 255, 0.03); padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
    .label-tag { background: #4facfe; color: #000; padding: 2px 10px; border-radius: 5px; font-size: 11px; font-weight: bold; margin-bottom: 8px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def extract_content(text, tag):
    """ฟังก์ชันดึงเนื้อหาตาม Tag แบบ Case-insensitive และรองรับหลายรูปแบบ"""
    pattern = f"{tag}:(.*?)(?=(TITLE:|STYLE:|LYRICS:|$))"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# --- 3. SIDEBAR (Inputs) ---
with st.sidebar:
    st.markdown("<h1 class='rainbow-title'>JAAO Studio</h1>", unsafe_allow_html=True)
    st.caption("AI Songwriting Assistant v2.5")
    api_key = st.text_input("Gemini API Key:", type="password", help="รับ Key ฟรีที่ aistudio.google.com")
    st.divider()
    
    artist_name = st.text_input("Artist Name:", value="JAAO")
    song_topic = st.text_area("Topic / Story:", placeholder="เช่น คิดถึงแฟนเก่าที่เลิกกันไปนานแล้ว...", height=100)
    
    main_style = st.selectbox("Category:", ["Pop", "Country / Folk", "Indie / Rock", "Hip Hop / R&B"])
    sub_styles = {
        "Pop": ["T-Pop Idol", "Modern Ballad", "Synth Pop", "City Pop"],
        "Country / Folk": ["Thai Country Indie", "Modern Luk Thung", "Puea Chiwit"],
        "Indie / Rock": ["Alternative Indie", "Thai Rock", "Post-Rock"],
        "Hip Hop / R&B": ["Trap", "R&B / Soul", "Lo-fi Hip Hop"]
    }
    selected_style = st.selectbox("Specific Genre:", sub_styles[main_style])
    
    with st.expander("⚙️ Advanced Settings"):
        tempo = st.select_slider("Tempo:", options=["Slow", "Moderate", "Fast"], value="Moderate")
        mood = st.multiselect("Mood:", ["Sad", "Happy", "Chill", "Energetic", "Dark"], default=["Happy"])

    generate_btn = st.button("✨ เริ่มรังสรรค์ผลงาน")

# --- 4. MAIN CONTENT (Logic & Display) ---
if generate_btn:
    if not api_key:
        st.warning("⚠️ กรุณากรอก API Key ในแถบด้านซ้าย")
    elif not song_topic:
        st.warning("⚠️ กรุณาบอกเรื่องราวของเพลงที่คุณอยากแต่ง")
    else:
        try:
            # Step A: Setup & Model Discovery
            genai.configure(api_key=api_key)
            
            # ค้นหาโมเดลที่ใช้งานได้อัตโนมัติ (แก้ปัญหา 404)
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # ลำดับความสำคัญ: 1.5 Flash -> 1.5 Pro -> ตัวแรกที่เจอ
            if "models/gemini-1.5-flash" in available_models:
                model_name = "models/gemini-1.5-flash"
            elif "models/gemini-1.5-pro" in available_models:
                model_name = "models/gemini-1.5-pro"
            else:
                model_name = available_models[0] if available_models else ""

            if not model_name:
                st.error("❌ ไม่พบ Model ที่รองรับใน API Key นี้")
                st.stop()

            # Step B: Define Prompt (ต้องอยู่ก่อนเรียกใช้)
            prompt = f"""
            You are a professional Thai songwriter. Create a song for Suno AI.
            Artist: {artist_name}
            Topic: {song_topic}
            Genre: {selected_style}
            Tempo: {tempo}
            Mood: {', '.join(mood)}

            Output format (Strictly):
            TITLE: [Song Name in Thai]
            STYLE: [English Suno Tags: genre, mood, tempo, vocal type, instruments]
            LYRICS:
            [Structure: [Intro], [Verse 1], [Pre-Chorus], [Chorus], [Verse 2], [Bridge], [Chorus], [Outro]]
            (Include Thai lyrics with guitar chords like [C][Am] above the lyrics)
            """

            # Step C: Generate
            with st.spinner(f'🪄 กำลังร่ายมนตร์ด้วย {model_name}...'):
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                res_text = response.text
                
                # Step D: Parsing Data
                title_final = extract_content(res_text, "TITLE")
                style_final = extract_content(res_text, "STYLE")
                lyrics_final = extract_content(res_text, "LYRICS")

            # Step E: UI Display
            st.balloons()
            st.success(f"🎵 รังสรรค์เพลง '{title_final}' สำเร็จ!")

            col_info, col_lyrics = st.columns([1, 1.5])

            with col_info:
                st.markdown("<div class='copy-section'>", unsafe_allow_html=True)
                st.markdown("<span class='label-tag'>1. SONG TITLE</span>", unsafe_allow_html=True)
                st.code(title_final if title_final else "Untitled")
                
                st.markdown("<span class='label-tag'>2. SUNO STYLE PROMPT</span>", unsafe_allow_html=True)
                st.code(f"Thai, {style_final}", language="markdown")
                st.caption("💡 ก๊อปปี้ไปวางในช่อง 'Style of Music' ใน Suno")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # เพิ่ม Bonus: Prompt สำหรับสร้างปกเพลง
                st.markdown("<div class='copy-section'>", unsafe_allow_html=True)
                st.markdown("<span class='label-tag'>🎨 ALBUM ART PROMPT</span>", unsafe_allow_html=True)
                st.code(f"Album cover art, {selected_style} music style, theme about {song_topic}, high quality, artistic", language="markdown")
                st.markdown("</div>", unsafe_allow_html=True)

            with col_lyrics:
                st.markdown("<div class='copy-section'>", unsafe_allow_html=True)
                st.markdown("<span class='label-tag'>3. LYRICS & CHORDS</span>", unsafe_allow_html=True)
                if lyrics_final:
                    st.code(lyrics_final, language="markdown")
                else:
                    st.code(res_text, language="markdown") # Fallback กรณี Regex พลาด
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                st.error("❌ โควตาฟรีหมด (429)! กรุณารอ 1 นาทีแล้วลองใหม่ หรือใช้ API Key แบบเสียเงินครับ")
            elif "404" in error_str:
                st.error("❌ ไม่พบโมเดล (404)! ระบบพยายามสลับโมเดลให้อัตโนมัติแล้ว แต่ยังไม่พบตัวที่ใช้ได้")
            else:
                st.error(f"❌ เกิดข้อผิดพลาด: {error_str}")

else:
    # หน้าแรกตอนเปิดแอป
    st.markdown("""
