# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON Payroll", page_icon="💰", layout="wide")

# --- CSS สไตล์นีออนสดใส ---
st.markdown("""
<style>
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stApp { background-color: #000000; color: #ffffff; }
    .main-title { color: #00ffcc !important; text-align: center; font-size: 40px !important; font-weight: 900 !important; text-shadow: 2px 2px 15px #00ffcc; }
    .card { background-color: #1a1a1a; padding: 20px; border-radius: 20px; border: 2px solid #ff00ff; margin-bottom: 15px; }
    .total-box { background-color: #000; padding: 25px; border-radius: 25px; border: 4px solid #00ffcc; text-align: center; box-shadow: 0 0 20px rgba(0, 255, 204, 0.4); }
    label { color: #00ffcc !important; font-weight: bold; }
    .block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🤑 ARNON คิดเงินเดือนสุดจ๊าบ v.7.4</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏢 รายได้ประจำเดือน")
        daily_rate = st.number_input("ค่าแรงพื้นฐานต่อวัน (฿):", min_value=0, value=350)
        c1, c2 = st.columns(2)
        with c1: pos_allowance = st.number_input("ค่าตำแหน่ง:", value=0)
        with c2: liv_allowance = st.number_input("ค่าครองชีพ:", value=0)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📅 บันทึกวันทำงานและวันลา")
        total_days = st.number_input("จำนวนวันทำงานทั้งหมดในเดือนนี้:", value=26)
        leave_dates = st.multiselect("จิ้มเลือก 'วันที่ลา':", options=[d for d in range(1, 32)], default=[])
        actual_work_days = total_days - len(leave_dates)
        st.markdown(f"🚫 ลาไป: {len(leave_dates)} วัน | ✨ มาทำจริง: {actual_work_days} วัน")
        st.write("---")
        st.write("🌈 เบี้ยขยัน (350.- / วิก)")
        inc1 = st.checkbox("วิกแรก (1-15) : ผ่าน ✅", value=True)
        inc2 = st.checkbox("วิกสอง (16-31) : ผ่าน ✅", value=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🛡️ ประกันสังคม & สวัสดิการ")
        sso_percent = st.slider("เลือก % ประกันสังคมที่โดนหัก:", 0.0, 5.0, 4.0, 0.1)
        c3, c4 = st.columns(2)
        with c3: food_rate = st.number_input("ค่าข้าวรายวัน:", value=50)
        with c4: travel_rate = st.number_input("ค่ารถรายวัน:", value=60)
        st.markdown('</div>', unsafe_allow_html=True)

# --- ส่วนของการคำนวณ ---
st.sidebar.markdown("### 🕒 ตั้งค่าโอที")
ot_days = st.sidebar.number_input("จำนวนวันทำ OT (2.5 ชม./วัน):", value=0)
ot_holiday = st.sidebar.number_input("จำนวนวันทำ OT วันหยุด (2 แรง):", value=0)

ot_normal_pay = ot_days * 2.5 * ((daily_rate / 8) * 1.5)
ot_holiday_pay = ot_holiday * (daily_rate * 2)
total_inc = (350 if inc1 else 0) + (350 if inc2 else 0)
total_food = food_rate * actual_work_days
total_travel = travel_rate * actual_work_days
total_base_pay = (daily_rate * total_days) + pos_allowance + liv_allowance
gross_income = total_base_pay + ot_normal_pay + ot_holiday_pay + total_inc + total_food + total_travel
sso_deduct = int(total_base_pay * (sso_percent / 100))
if sso_deduct > 750: sso_deduct = 750
net_pay = gross_income - sso_deduct

with col2:
    st.subheader("📑 สรุปสลิปเงินเดือนพี่อานนท์")
    res_table = {
        "รายการ": ["ค่าแรงพื้นฐาน", "ตำแหน่ง+ครองชีพ", "โอทีทั้งหมด", "เบี้ยขยัน", "ค่าข้าว", "ค่ารถ"],
        "ยอดเงิน (฿)": [
            f"{(daily_rate * total_days):,.2f}", f"{(pos_allowance + liv_allowance):,.2f}",
            f"{(ot_normal_pay + ot_holiday_pay):,.2f}", f"{total_inc:,.2f}",
            f"{total_food:,.2f}", f"{total_travel:,.2f}"
        ]
    }
    st.table(pd.DataFrame(res_table))
    st.markdown(f"**📉 หักประกันสังคม ({sso_percent}%):** -{sso_deduct:,.0f} ฿")
    
    # แก้ไขจุดที่ทำให้ Error โดยใช้ตัวหนังสือธรรมดาแทน Emoji ใน HTML
    st.markdown(f"""
    <div class="total-box">
        <p style="margin:0; font-size:25px; color:#00ffcc;">[ MONEY ] ยอดเงินเดือนโอนสุทธิ [ MONEY ]</p>
        <h1 style="margin:0; font-size:65px; color:#ffffff; text-shadow: 0 0 20px #00ffcc;">฿ {net_pay:,.2f}</h1>
        <p style="margin-top:10px; color:#ff00ff; font-weight:bold;">จ๊าบสุดๆ ไปเลยครับพี่!</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("Arnon Payroll App v.7.4 | สุดจ๊าบและแม่นยำ")
