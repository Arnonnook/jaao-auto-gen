# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON Payroll", page_icon="🔐", layout="wide")

# --- ระบบ Login และดักจับ API Key ---
def check_login():
    if "logged_in" not in st.session_state:
        st.markdown("""
        <style>
            .stApp { background-color: #000000; }
            .login-card { 
                background-color: #1a1a1a; padding: 30px; border-radius: 20px; 
                border: 2px solid #00ffcc; text-align: center;
            }
            label { color: #00ffcc !important; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 style="color:#00ffcc; text-align:center; text-shadow: 2px 2px 10px #00ffcc;">🔐 ARNON LOGIN SYSTEM</h1>', unsafe_allow_html=True)
        
        with st.container():
            col_l, col_r = st.columns([1, 1])
            with col_l:
                u = st.text_input("Username", key="u_input")
                p = st.text_input("Password", type="password", key="p_input")
            with col_r:
                api = st.text_input("Gemini API Key", type="password", key="api_input", help="กรอกคีย์จาก aistudio.google.com")
            
            if st.button("🚀 เข้าสู่ระบบสุดจ๊าบ", use_container_width=True):
                if u == "arnon" and p == "1234" and api: # <-- เช็กว่ากรอกครบและรหัสถูก
                    st.session_state["logged_in"] = True
                    st.session_state["user_api_key"] = api
                    st.rerun()
                elif not api:
                    st.warning("⚠️ พี่ต้องใส่ API Key ด้วยนะครับถึงจะเข้าได้")
                else:
                    st.error("🚫 ชื่อหรือรหัสผิดครับพี่อานนท์!")
        return False
    return True

if check_login():
    # --- CSS สไตล์นีออนจ๊าบๆ ---
    st.markdown("""
    <style>
        header {visibility: hidden;} .stDeployButton {display:none;}
        #MainMenu {visibility: hidden;} footer {visibility: hidden;}
        .stApp { background-color: #000; color: #fff; }
        .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
        .card { background-color: #1a1a1a; padding: 20px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 15px; }
        .total-box { background-color: #000; padding: 25px; border-radius: 25px; border: 4px solid #00ffcc; text-align: center; }
        label { color: #00ffcc !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<h1 class="main-title">🤑 ARNON Payroll v.8.0</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        # --- ข้อมูลรายได้ ---
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🏢 รายได้หลัก")
            daily_rate = st.number_input("ค่าแรงพื้นฐานต่อวัน (฿):", value=350, help="ฐานค่าแรงปกติ")
            c_p, c_l = st.columns(2)
            with c_p: pos_allowance = st.number_input("ค่าตำแหน่ง:", value=0)
            with c_l: liv_allowance = st.number_input("ค่าครองชีพ:", value=0)
            st.markdown('</div>', unsafe_allow_html=True)

        # --- วันทำงานและวันลา ---
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📅 วันทำงาน/ลา")
            total_days = st.number_input("จำนวนวันทำงานในเดือน:", value=26)
            leave_dates = st.multiselect("จิ้มเลือก 'วันที่ลา':", options=[d for d in range(1, 32)])
            actual_work_days = total_days - len(leave_dates)
            st.write(f"✨ ทำงานจริง: {actual_work_days} วัน")
            c_i1, c_i2 = st.columns(2)
            with c_i1: inc1 = st.checkbox("วิกแรก ✅", value=True)
            with c_i2: inc2 = st.checkbox("วิกสอง ✅", value=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # --- โอที ---
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🕒 โอที (OT)")
            ot_mode = st.radio("โหมดโอที:", ["วัน (2.5 ชม.)", "ชั่วโมง"])
            hr_rate = daily_rate / 8
            if ot_mode == "วัน (2.5 ชม.)":
                d1, d2, d3 = st.columns(3)
                with d1: ot_n_d = st.number_input("1.5x (วัน):", value=0)
                with d2: ot_h_d = st.number_input("2x (วัน):", value=0)
                with d3: ot_s_d = st.number_input("3x (วัน):", value=0)
                p_ot_n = ot_n_d * 2.5 * (hr_rate * 1.5)
                p_ot_h = ot_h_d * 8 * (hr_rate * 2.0)
                p_ot_s = ot_s_d * 8 * (hr_rate * 3.0)
            else:
                h1, h2, h3 = st.columns(3)
                with h1: ot_n_h = st.number_input("1.5x (ชม.):", value=0.0)
                with h2: ot_h_h = st.number_input("2x (ชม.):", value=0.0)
                with h3: ot_s_h = st.number_input("3x (ชม.):", value=0.0)
                p_ot_n = ot_n_h * (hr_rate * 1.5)
                p_ot_h = ot_h_h * (hr_rate * 2.0)
                p_ot_s = ot_s_h * (hr_rate * 3.0)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- คำนวณยอดเงิน ---
    total_base = (daily_rate * total_days) + pos_allowance + liv_allowance
    total_inc = (350 if inc1 else 0) + (350 if inc2 else 0)
    total_welfare = (50 + 60) * actual_work_days
    gross = total_base + p_ot_n + p_ot_h + p_ot_s + total_inc + total_welfare
    
    sso_p = st.sidebar.slider("ประกันสังคม (%)", 0.0, 5.0, 4.0, 0.1)
    sso_val = int(gross * (sso_p / 100))
    if sso_val > 750: sso_val = 750
    net = gross - sso_val

    with col2:
        st.subheader("📑 รายละเอียดสลิป")
        res = {"รายการ": ["ค่าแรงพื้นฐาน", "ตำแหน่ง+ครองชีพ", "โอทีรวม", "เบี้ยขยัน", "ข้าว+รถ"],
               "เงิน (฿)": [f"{total_base:,.2f}", f"{(pos_allowance+liv_allowance):,.2f}", f"{(p_ot_n+p_ot_h+p_ot_s):,.2f}", f"{total_inc:,.2f}", f"{total_welfare:,.2f}"]}
        st.table(pd.DataFrame(res))
        st.markdown(f"**หักประกันสังคม ({sso_p}%):** -{sso_val:,.0f} ฿")
        st.markdown(f'<div class="total-box"><h1 style="color:#fff;">฿ {net:,.2f}</h1></div>', unsafe_allow_html=True)
        
        # --- ปุ่ม AI วิเคราะห์ (ใช้คีย์จากหน้า Login) ---
        st.write("---")
        if st.button("✨ ให้ AI วิเคราะห์รายได้"):
            try:
                genai.configure(api_key=st.session_state["user_api_key"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"พนักงานชื่ออานนท์ ได้เงินเดือนสุทธิ {net} บาท ช่วยวิเคราะห์แบบจ๊าบๆ")
                st.success(response.text)
            except:
                st.error("❌ API Key ไม่ถูกต้อง หรือเกิดข้อผิดพลาด")
        
        if st.button("🚪 ออกจากระบบ"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

st.caption("Arnon Payroll App v.8.0 | Login with Integrated API Key")
