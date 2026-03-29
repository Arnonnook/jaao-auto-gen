import streamlit as st
import google.generativeai as genai
import re

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="JAAO Suno Helper Pro", page_icon="🎸", layout="wide")

# ปรับ CSS ให้ดูสะอาดและเป็นมืออาชีพมากขึ้น (Glassmorphism Style)
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e1e2f, #2a2a40); color: #ffffff; }
    [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.05); }
    .rainbow-title { 
        font-weight: 800; 
        background: linear-gradient(to right, #ff3366, #ff9933, #33ccff, #9933ff); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-size: 42px; 
        margin-bottom: 20px;
    }
    .stButton>button { 
        width: 100%;
        background: linear-gradient(90deg, #ff3366, #9933ff); 
        color: white; border-radius: 12px; border: none; 
        padding: 15px; font-size: 18px; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(255, 51, 102, 0.4); }
    .copy-section { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
    .label-tag { background: #33ccff; color: #000; padding: 2px 10px; border-radius: 5px; font-size: 12px; font-weight: bold; margin-bottom: 10px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

# --- 2. LOGIC FUNCTIONS ---
def clean_text(text, tag):
    """ช่วยดึงข้อมูลตาม Tag ที่กำหนดอย่างแม่นยำ"""
    pattern = f"{tag}:(.*?)(?=(TITLE:|STYLE:|LYRICS:|$))"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='rainbow-title'>JAAO Studio</h1>", unsafe_allow_html=True)
    api_key = st.text_input("Gemini API Key:", type="password", help="รับได้ที่ Google AI Studio")
    st.divider()
    
    artist_name = st.text_input("Artist Name:", value="JAAO", placeholder="ชื่อศิลปิน")
    song_topic = st.text_area("Topic / Story:", placeholder="เล่าเรื่องราวที่อยากให้เป็นเพลง...", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        main_style = st.selectbox("Category:", ["Pop", "Country / Folk", "Indie / Rock", "Hip Hop / R&B"])
    with col2:
        sub_styles = {
            "Pop": ["T-Pop", "Modern Ballad", "Synth Pop", "City Pop"],
            "Country / Folk": ["Thai Country Indie", "Modern Luk Thung", "Folk Song"],
            "Indie / Rock": ["Alternative", "Shoegaze", "Thai Rock", "Post-Rock"],
            "Hip Hop / R&B": ["Trap", "Old School", "R&B / Soul", "Lo-fi"]
        }
        selected_style = st.selectbox("Genre:", sub_styles[main_style])

    tempo = st.select_slider("Tempo:", options=["Slow", "Moderate", "Fast"], value="Moderate")
    mood = st.multiselect("Mood:", ["Sad", "Happy", "Energetic", "Dark", "Romantic"], default=["Happy"])

    generate_btn = st.button("🚀 รังสรรค์เพลง Pro")

# --- 4. MAIN CONTENT ---
if generate_btn:
    if not api_key:
        st.warning("⚠️ กรุณาใส่ API Key ก่อนเริ่มงาน")
    elif not song_topic:
        st.warning("⚠️ อย่าลืมใส่เนื้อหาเพลงนะครับ")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash') # อัปเดตเป็น Model ที่เสถียรที่สุด
            
            prompt = f"""
            You are a professional Thai songwriter for Suno AI.
            Artist: {artist_name}
            Topic: {song_topic}
            Genre: {selected_style}
            Tempo: {tempo}
            Mood: {', '.join(mood)}

            Output Format:
            TITLE: [Song Name]
            STYLE: [English Suno Tags: genre, mood, tempo, vocal type, 5-8 descriptive tags]
            LYRICS:
            [Structure: [Intro], [Verse 1], [Pre-Chorus], [Chorus], [Verse 2], [Bridge], [Outro]]
            [Note: Add guitar chords [C][G] above lyrics line]
            """
            
            with st.spinner('🪄 กำลังร่ายมนตร์สร้างบทเพลง...'):
                response = model.generate_content(prompt)
                res_text = response.text
                
                # ดึงข้อมูลมาแสดงผล
                title = clean_text(res_text, "TITLE")
                style_tags = clean_text(res_text, "STYLE")
                lyrics = clean_text(res_text, "LYRICS")

            st.balloons()
            
            # --- Displaying Results ---
            st.success(f"🎵 ผลงานเพลงสำหรับคุณ {artist_name} พร้อมแล้ว!")
            
            row1_col1, row1_col2 = st.columns([1, 2])
            
            with row1_col1:
                st.markdown("<div class='copy-section'>", unsafe_allow_html=True)
                st.markdown("<span class='label-tag'>SONG TITLE</span>", unsafe_allow_html=True)
                st.code(title if title else "Untitled Song")
                
                st.markdown("<span class='label-tag'>SUNO STYLE PROMPT</span>", unsafe_allow_html=True)
                st.code(f"Thai, {style_tags}", language="markdown")
                st.info("💡 นำไปวางในช่อง 'Style of Music' ใน Suno Custom Mode")
                st.markdown("</div>", unsafe_allow_html=True)

            with row1_col2:
                st.markdown("<div class='copy-section'>", unsafe_allow_html=True)
                st.markdown("<span class='label-tag'>LYRICS & CHORDS</span>", unsafe_allow_html=True)
                st.code(lyrics, language="markdown")
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดทางเทคนิค: {str(e)}")

else:
    # หน้า Welcome ตอนยังไม่ได้กดปุ่ม
    st.markdown("""
    <div style='text-align: center; padding: 100px;'>
        <h2 style='opacity: 0.5;'>🎨 เริ่มต้นสร้างสรรค์ผลงานของคุณจากแถบด้านซ้าย</h2>
        <p style='opacity: 0.3;'>ระบบจะช่วยคิดชื่อเพลง, สไตล์ที่ Suno เข้าใจง่าย และเนื้อเพลงพร้อมคอร์ด</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Developed by JAAO Studio | 🚀 Version 2.0 (Pro Mode)")
