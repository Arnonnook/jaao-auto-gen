import streamlit as st
import google.generativeai as genai
from groq import Groq
import re

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="JAAO Hybrid Suno", page_icon="🌈", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #ffffff; }
    [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.05); }
    .rainbow-title { font-weight: 800; background: linear-gradient(to right, #00f2fe, #4facfe, #9933ff, #ff3366); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 38px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00f2fe, #4facfe); color: #000; border-radius: 12px; font-weight: bold; border: none; padding: 10px; }
    .copy-section { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; }
    .label-tag { background: #ff3366; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; margin-bottom: 5px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def extract_content(text, tag):
    pattern = f"{tag}:(.*?)(?=(TITLE:|STYLE:|LYRICS:|$))"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='rainbow-title'>JAAO Studio</h1>", unsafe_allow_html=True)
    
    # เลือกว่าจะใช้ AI ค่ายไหน
    ai_choice = st.radio("เลือก AI Engine:", ["Gemini (Google)", "Groq (Llama 3.1)"])
    
    if ai_choice == "Gemini (Google)":
        api_key = st.text_input("Gemini API Key:", type="password")
        model_option = "models/gemini-1.5-flash"
    else:
        api_key = st.text_input("Groq API Key:", type="password")
        model_option = "llama-3.1-8b-instant"

    st.divider()
    artist_name = st.text_input("Artist Name:", value="JAAO")
    song_topic = st.text_area("หัวข้อ/เรื่องราวเพลง:", placeholder="เช่น รักข้างเดียว...")
    
    main_style = st.selectbox("แนวเพลงหลัก:", ["Pop", "Country", "Rock", "Hip Hop"])
    selected_style = st.selectbox("แนวเพลงย่อย:", ["T-Pop", "Indie", "Rap", "Folk"])
    
    generate_btn = st.button("🚀 รังสรรค์เพลง")

# --- 4. LOGIC ENGINE ---
if generate_btn:
    if not api_key:
        st.warning(f"⚠️ กรุณาใส่ {ai_choice} API Key")
    elif not song_topic:
        st.error("⚠️ กรุณาใส่หัวข้อเพลง")
    else:
        prompt = f"""
        Task: Create a song for Suno AI.
        Artist: {artist_name}
        Topic: {song_topic}
        Style: {selected_style}
        Output format:
        TITLE: [Thai Title]
        STYLE: [English Suno tags]
        LYRICS: [Verse/Chorus with chords]
        """

        try:
            with st.spinner(f'กำลังใช้ {ai_choice} ปรุงแต่งเพลง...'):
                if ai_choice == "Gemini (Google)":
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_option)
                    response = model.generate_content(prompt)
                    res_text = response.text
                else:
                    # เรียกใช้ Groq
                    client = Groq(api_key=api_key)
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model_option,
                    )
                    res_text = chat_completion.choices[0].message.content

                # --- 5. DISPLAY ---
                st.balloons()
                title = extract_content(res_text
