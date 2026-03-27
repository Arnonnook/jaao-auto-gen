# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON Payroll", page_icon="🔐", layout="wide")

# --- ระบบ Login ---
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown('<h1 style="color:#00ffcc; text-align:center;">🔐 ARNON LOGIN</h1>', unsafe_allow_html=True)
        user = st.text_input("Username", key="username")
        pw = st.text_input("Password", type="password", key="password")
        if st.button("เข้าสู่ระบบสุดจ๊าบ"):
            if user == "arnon" and pw == "1234": # <-- พี่เปลี่ยนรหัสตรงนี้ได้
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("รหัสผิดนะพี่!")
        return False
    return True

if check_password():
    # --- CSS สไตล์นีออน ---
    st.markdown("""
    <style>
        header {visibility: hidden;} .stDeployButton {display:none;}
        .stApp { background-color: #000; color: #fff; }
        .main-title { color: #00ffcc; text-align: center; font-weight: 900; text-shadow: 2px 2px 15px #00ffcc; }
        .card { background-color: #1a1a1a; padding: 20px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 15px; }
        .total-box { background-color: #000; padding: 25px; border-radius: 25px; border: 4px solid #00ffcc; text-align: center; }
        label { color: #00ffcc !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar สำหรับจัดการ API Key ของผู้ใช้คนอื่น ---
    st.sidebar.markdown("### 🔑 ตั้งค่า API ส่วนตัว")
    user_api_key = st.sidebar.text_input("กรอก Gemini API Key ของคุณ:", type="password", help="ไปเอาคีย์ได้ที่ aistudio.google.com")
    
    st.markdown('<h1 class="main-title">🤑 ARNON Payroll v.7.9</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🏢 รายได้หลัก")
            daily_rate = st.number_input("ค่าแรงพื้นฐานต่อวัน (฿):", value=350)
            c_p, c_l = st.columns(2)
            with c_p: pos_allowance = st.number_input("ค่าตำแหน่ง:", value=0)
            with c_l: liv_allowance = st.number_input("ค่าครองชีพ:", value=0)
            st.markdown('</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📅 วันทำงาน/ลา")
            total_days = st.number_input("วันทำงานในเดือน:", value=26)
            leave_dates = st.multiselect("จิ้มเลือก 'วันที่ลา':", options=[d for d in range(1, 32)])
            actual_work_days = total_days - len(leave_dates)
            st.write("🌈 เบี้ยขยันวิก 1-2")
            c_inc1, c_inc2 = st.columns(2)
            with c_inc1: inc1 = st.checkbox("วิกแรก ✅", value=True)
            with c_inc2: inc2 = st.checkbox("วิกสอง ✅", value=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🕒 โอที (OT)")
            ot_mode = st.radio("โหมดโอที:", ["วัน (2.5 ชม.)", "ชั่วโมง"])
            hourly_rate = daily_rate / 8
            if ot_mode == "วัน (2.5 ชม.)":
                d1, d2, d3 = st.columns(3)
                with d1: ot_n_days = st.number_input("1.5x (วัน):", value=0)
                with d2: ot_h_days = st.number_input("2x (วัน):", value=0)
                with d3: ot_s_days = st.number_input("3x (วัน):", value=0)
                pay_ot_n = ot_n_days * 2.5 * (hourly_rate * 1.5)
                pay_ot_h = ot_h_days * 8 * (hourly_rate * 2.0)
                pay_ot_s = ot_s_days * 8 * (hourly_rate * 3.0)
            else:
                h1, h2, h3 = st.columns(3)
                with h1: ot_n_hr = st.number_input("1.5x (ชม.):", value=0.0)
                with h2: ot_h_hr = st.number_input("2x (ชม.):", value=0.0)
                with h3: ot_s_hr = st.number_input("3x (ชม.):", value=0.0)
                pay_ot_n = ot_n_hr * (hourly_rate * 1.5)
                pay_ot_h = ot_h_hr * (hourly_rate * 2.0)
                pay_ot_s = ot_s_hr * (hourly_rate * 3.0)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- การคำนวณเงิน ---
    total_base = (daily_rate * total_days) + pos_allowance + liv_allowance
    total_inc = (350 if inc1 else 0) + (350 if inc2 else 0)
    total_welfare = (50 + 60) * actual_work_days
    gross_income = total_base + pay_ot_n + pay_ot_h + pay_ot_s + total_inc + total_welfare
    
    sso_p = st.sidebar.slider("หักประกันสังคม (%)", 0.0, 5.0, 4.0, 0.1)
    sso_deduct = int(gross_income * (sso_p / 100))
    if sso_deduct > 750: sso_deduct = 750
    net_pay = gross_income - sso_deduct

    with col2:
        st.subheader("📑 สรุปสลิปเงินเดือน")
        res_table = {
            "รายการ": ["ค่าแรงพื้นฐาน", "ตำแหน่ง+ครองชีพ", "โอทีรวม", "เบี้ยขยัน", "ข้าว+รถ"],
            "เงิน (฿)": [f"{total_base:,.2f}", f"{(pos_allowance+liv_allowance):,.2f}", f"{(pay_ot_n+pay_ot_h+pay_ot_s):,.2f}", f"{total_inc:,.2f}", f"{total_welfare:,.2f}"]
        }
        st.table(pd.DataFrame(res_table))
        st.markdown(f"**📉 หักประกันสังคม ({sso_p}%):** -{sso_deduct:,.0f} ฿")
        st.markdown(f'<div class="total-box"><h1 style="color:#fff;">฿ {net_pay:,.2f}</h1></div>', unsafe_allow_html=True)
        
        # --- ส่วนของ AI (ใช้คีย์ที่กรอกใน Sidebar) ---
        st.write("---")
        if st.button("✨ ให้ AI วิเคราะห์รายได้"):
            if not user_api_key:
                st.warning("⚠️ พี่ต้องกรอก API Key ในแถบด้านข้างก่อนครับ ถึงจะใช้ AI ได้")
            else:
                try:
                    genai.configure(api_key=user_api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"พนักงานรายได้ {net_pay} บาท ช่วยวิเคราะห์แบบจ๊าบๆ"
                    response = model.generate_content(prompt)
                    st.success(response.text)
                except:
                    st.error("❌ API Key ไม่ถูกต้อง หรือหมดอายุครับ")
