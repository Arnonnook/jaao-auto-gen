import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="JAAO Auto Gen", page_icon="🎵", layout="wide")

# --- UI Custom Style ---
st.markdown("""
<style>
    .stApp { background-color: #fcfcfc; }
    .stButton>button { background: linear-gradient(45deg, #00B4DB, #0083B0); color: white; border-radius: 12px; height: 3.5em; width: 100%; font-weight: bold; border: none; }
    .style-card { background: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #0083B0; margin-bottom: 20px; }
    .lyrics-container { background-color: #ffffff; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Input ---
with st.sidebar:
    st.title("🎵 JAAO Auto Gen")
    api_key = st.text_input("Gemini API Key:", type="password")
    st.divider()
    
    artist_name = st.text_input("Artist Name:", placeholder="e.g. JAAO, WARIN")
    song_topic = st.text_input("Song Topic:", placeholder="e.g. Rain in Bangkok")
    
    st.divider()
    
    st.subheader("Select Music Style")
    music_main_style = st.selectbox("Category:", ["Pop", "Country / Folk", "Indie / Rock", "Hip Hop / R&B"])
    
    sub_styles = {
        "Pop": ["T-Pop Idol", "Modern Ballad", "Synth Pop", "City Pop"],
        "Country / Folk": ["Thai Country Indie", "Modern Luk Thung", "Folk Song", "Puea Chiwit"],
        "Indie / Rock": ["Alternative Indie", "Shoegaze", "Thai Rock", "Modern Rock"],
        "Hip Hop / R&B": ["Trap", "Old School Hip Hop", "R&B / Soul", "Lo-fi Hip Hop"]
    }
    selected_style = st.selectbox("Specific Genre:", sub_styles[music_main_style])

    generate_btn = st.button("Generate & Analyze Style ✨")

# --- Main Display Area ---
st.header(f"🎧 Producer: {artist_name if artist_name else 'JAAO Studio'}")

if generate_btn:
    if not api_key:
        st.error("Please enter API Key")
    elif not song_topic:
        st.error("Please enter Song Topic")
    else:
        with st.spinner('AI is composing and analyzing...'):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # สั่งให้ AI เจนทั้งเนื้อเพลงและบทวิเคราะห์สไตล์
                prompt = f"""
                Write Thai song lyrics for artist '{artist_name}' in style '{selected_style}' about '{song_topic}'.
                
                After the lyrics, provide a brief 'Style Summary' in English including:
                - Estimated Tempo (BPM)
                - Overall Mood
                - Recommended Instruments
                
                Requirements:
                1. Include guitar chords (e.g. [C][Am]) ABOVE the lyrics.
                2. Structure: Verse, Chorus, Bridge, etc.
                3. Use modern Thai language.
                """
                
                response = model.generate_content(prompt)
                full_text = response.text
                
                # แสดงส่วนวิเคราะห์สไตล์ (Style Analysis)
                st.markdown(f"""
                <div class="style-card">
                    <h4>✨ Song Style Analysis</h4>
                    <p><b>Genre:</b> {selected_style} | <b>Artist:</b> {artist_name if artist_name else 'JAAO'}</p>
                    <p><i>The lyrics below include chords and can be copied immediately.</i></p>
                </div>
                """, unsafe_allow_html=True)
                
                # ส่วนแสดงผลเนื้อเพลง (Copyable Code Block)
                st.subheader("📝 Lyrics & Chords")
                st.code(full_text, language="markdown")
                
                st.success("Successfully Generated! Click the 'Copy' icon at the top right of the lyrics box.")
                
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Fill in the details on the left and click the button to start.")

st.divider()
st.caption("JAAO Studio - Your Creative Music Partner")
