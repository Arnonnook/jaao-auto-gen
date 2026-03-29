import streamlit as st
import google.generativeai as genai
from groq import Groq
import re

# --- 1. SETTINGS & THEME (แต่งหน้าตาให้เหมือนรูป) ---
st.set_page_config(page_title="JAAO Music Studio", page_icon="🎵", layout="wide")

st.markdown("""
<style>
    /* พื้นหลังหลักโทน Deep Blue */
    .stApp {
        background: radial-gradient(circle at top right, #0a192f, #050a14);
        color: #e6f1ff;
    }

    /* ตกแต่ง Sidebar ให้ดูหรู */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 25, 47, 0.8);
        border-right: 1px solid #1e3a5f;
    }

    /* หัวข้อใหญ่แบบในรูป */
    .hero-title {
        font-size: 60px;
        font-weight: 850;
        line-height: 1.1;
        background: linear-gradient(to bottom, #ffffff, #8892b0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    /* การ์ดแบบ Glassmorphism (เนื้อร้อง/ข้อมูล) */
    .music-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(10px);
        margin-top: 20px;
    }

    /* ปุ่มสไตล์ในรูป (Blue Gradient) */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1e3a5f, #3366ff);
        color: white;
        border-radius: 50px;
        border: none;
        padding: 12px;
        font-weight: bold;
        transition: 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(51, 102, 255, 0.6);
        transform: translateY(-2px);
    }

    /* ป้าย Tag เล็กๆ */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
        margin-right: 5px;
        background: #0044cc;
        color: #00f2fe;
        border: 1px solid #00f2fe;
    }

    /* ลิงก์ Suno สไตล์ปุ่มเด่น */
    .suno-link {
        display: block;
        text-align: center;
        padding: 15px;
        background: #3366ff;
        color: white !important;
        text-decoration: none;
        border-radius: 12px;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. LOGIC FUNCTIONS ---
def extract_content(text, tag):
    pattern = f"{tag}:(.*?)(?=(TITLE:|STYLE:|LYRICS:|$))"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# --- 3. SIDEBAR (Input Section) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe;'>⚙️ Studio Config</h2>", unsafe_allow_html=True)
    ai_choice = st.radio("AI Engine", ["Gemini", "Groq"])
    api_key = st.text_input("API Key", type="password")
    
    st.divider()
    artist = st.text_input("Artist Name", value="JAAO Official")
    topic = st.text_area("Song Concept / Story", placeholder="Describe your music...")
    
    style = st.selectbox("Genre", ["EDM", "Pop", "Rock", "LUK THUNG", "HIPHOP"])
    generate_btn = st.button("Generate Masterpiece")

# --- 4. HERO SECTION ---
col_hero, col_img = st.columns([1.2, 1])

with col_hero:
    st.markdown("<h1 class='hero-title'>Dive Into<br>Deep Blue<br>Sound</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8892b0; font-size:18px;'>ระบบรังสรรค์และคำนวณบทเพลงระดับ Exclusive สำหรับ Suno AI โดยเฉพาะ</p>", unsafe_allow_html=True)
    st.markdown("""
        <span class='badge'>Exclusive License</span>
        <span class='badge'>Full Mix MP3</span>
        <span class='badge'>Crystal UI Theme</span>
    """, unsafe_allow_html=True)

with col_img:
    # ใส่รูป Placeholder หรือรูปบรรยากาศคอนเสิร์ต
    st.image("https://images.unsplash.com/photo-1514525253361-bee8718a74a7?q=80&w=1000&auto=format&fit=crop", use_container_width=True)

# --- 5. MAIN LOGIC & DISPLAY ---
if generate_btn:
    if not api_key:
        st.warning("Please enter your API Key")
    else:
        prompt = f"Create a Suno AI song. Artist: {artist}, Topic: {topic}, Genre: {style}. TITLE: [Thai], STYLE: [English Tags], LYRICS: [Thai with Chords]"
        try:
            with st.spinner('Calculating Harmony...'):
                if ai_choice == "Gemini":
                    genai.configure(api_key=api_key)
                    res_text = genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt).text
                else:
                    res_text = Groq(api_key=api_key).chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.1-8b-instant").choices[0].message.content

                title = extract_content(res_text, "TITLE")
                style_tags = extract_content(res_text, "STYLE")
                lyrics = extract_content(res_text, "LYRICS")

                # การแสดงผลแบบ Card
                st.markdown("<h2 style='color:#00f2fe; margin-top:40px;'>🎵 Generated Track</h2>", unsafe_allow_html=True)
                
                # แสดงผล Title และ Style ในกล่องเดียวกัน
                st.markdown(f"""
                <div class='music-card'>
                    <div style='display:flex; align-items:center; gap:20px;'>
                        <div style='background:#1e3a5f; padding:20px; border-radius:50%;'>🎧</div>
                        <div>
                            <h3 style='margin:0; color:#ffffff;'>{title}</h3>
                            <p style='margin:0; color:#8892b0;'>{style} | {artist}</p>
                        </div>
                    </div>
                    <hr style='border-color:rgba(255,255,255,0.1);'>
                    <p><b style='color:#00f2fe;'>STYLE TAGS:</b> {style_tags}</p>
                    <a href='https://suno.com/create' target='_blank' class='suno-link'>COPY & CREATE ON SUNO AI</a>
                </div>
                """, unsafe_allow_html=True)

                # แสดงเนื้อร้อง
                st.markdown("<div class='music-card'>", unsafe_allow_html=True)
                st.markdown("<b style='color:#00f2fe;'>LYRICS & CHORDS:</b>", unsafe_allow_html=True)
                st.code(lyrics if lyrics else res_text, language="markdown")
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
else:
    # หน้าแสดงผลเริ่มต้น (เลียนแบบแถวล่างของรูป)
    st.markdown("<h3 style='margin-top:50px;'>Featured Tracks</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for c in [c1, c2, c3]:
        with c:
            st.markdown("""
            <div class='music-card' style='padding:15px; text-align:center;'>
                <div style='font-size:30px;'>🎧</div>
                <p><b>Ready to Compose</b></p>
                <p style='color:#8892b0; font
