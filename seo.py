import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO SEO Master v.2.7", page_icon="🎥", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; color: #ffffff; }
    .seo-title { color: #ff0000 !important; text-align: center; font-size: 40px !important; font-weight: 900 !important; }
    div.stButton > button:first-child { background-color: #ff0000 !important; color: white !important; height: 60px; font-size: 20px; font-weight: bold; border-radius: 30px; width: 100%; }
    .tag-label { color: #00f2ff; font-weight: bold; font-size: 18px; margin-bottom: 5px; }
    .preview-box { border: 2px solid #333; border-radius: 15px; padding: 10px; background: #1a1a1a; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

try:
    API_KEY = st.secrets["MY_API_KEY"] 
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ ไม่พบ API Key ใน Secrets!")
    st.stop()

st.markdown('<h1 class="seo-title">🎥 JAAO SEO & VIDEO PREVIEW v.2.7</h1>', unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("🔗 ข้อมูลวิดีโอ")
    yt_url = st.text_input("วางลิงก์ YouTube ที่นี่:", placeholder="https://www.youtube.com/watch?v=...")
    
    # --- ช่องโชว์วิดีโอตัวอย่าง ---
    if yt_url:
        try:
            st.markdown('<div class="preview-box">', unsafe_allow_html=True)
            st.video(yt_url) # คำสั่งโชว์ตัวเล่น YouTube
            st.markdown('</div>', unsafe_allow_html=True)
        except:
            st.warning("⚠️ ลิงก์ไม่ถูกต้อง หรือวิดีโอไม่สามารถเล่นได้")

    music_detail = st.text_area("✍️ ใส่เนื้อร้องหรือรายละเอียดเพิ่มเติม (ถ้ามี):", height=150)
    music_style = st.selectbox("🎸 แนวเพลง:", ["ลูกทุ่งอินดี้", "เพื่อชีวิต", "ร็อก/สตริง", "ป็อป", "แร็ป"])
    
    analyze_btn = st.button("🚀 วิเคราะห์ SEO จากวิดีโอนี้")

with col_out:
    if analyze_btn:
        if yt_url or music_detail:
            with st.spinner("⏳ กำลังวิเคราะห์ข้อมูลวิดีโอและวางกลยุทธ์ SEO..."):
                try:
                    # สั่ง AI ให้วิเคราะห์จากตัววิดีโอที่ให้มา
                    prompt = f"""
                    วิเคราะห์วิดีโอจากลิงก์: {yt_url} 
                    ข้อมูลประกอบ: "{music_detail}" 
                    แนวเพลง: {music_style}
                    
                    ภารกิจ: ให้ข้อมูล SEO ที่แม่นยำที่สุดเพื่อให้ยอดวิวสูงขึ้น
                    [TITLE]: ชื่อคลิปใหม่ที่ดึงดูดใจ
                    [DESC]: คำอธิบาย 3 บรรทัดแรก
                    [TAGS]: เฉพาะคำค้นหาคั่นด้วยคอมม่าเท่านั้น
                    [HASHTAGS]: เฉพาะ # คั่นด้วยช่องว่าง
                    """
                    
                    response = model.generate_content(prompt)
                    res = response.text
                    
                    # สกัดข้อมูลมาโชว์
                    parts = {"[TITLE]": "", "[DESC]": "", "[TAGS]": "", "[HASHTAGS]": ""}
                    current_key = None
                    for line in res.split('\n'):
                        for key in parts.keys():
                            if key in line:
                                current_key = key
                                parts[key] = line.replace(key, "").replace(":", "").strip()
                                break
                    
                    st.success("วิเคราะห์เสร็จเรียบร้อยครับ!")
                    st.markdown('<p class="tag-label">🎯 ชื่อที่แนะนำ:</p>', unsafe_allow_html=True)
                    st.info(parts["[TITLE]"])
                    st.markdown('<p class="tag-label">🏷️ Tags (สะอาด ก๊อปไปวางได้เลย):</p>', unsafe_allow_html=True)
                    st.code(parts["[TAGS]"], language="text")
                    st.markdown('<p class="tag-label">#️⃣ Hashtags:</p>', unsafe_allow_html=True)
                    st.code(parts["[HASHTAGS]"], language="text")
                    st.markdown('<p class="tag-label">📝 คำอธิบาย:</p>', unsafe_allow_html=True)
                    st.write(parts["[DESC]"])

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาวางลิงก์ YouTube ก่อนครับ")

st.write("---")
st.caption("© 2026 JAAO SEO Studio | Video Preview & Music SEO")
