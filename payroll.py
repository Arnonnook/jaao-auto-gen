# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ARNON Payroll", page_icon="💰", layout="wide")

# --- CSS สไตล์นีออนจ๊าบๆ ---
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
    /* ปรับแต่งสี Tooltip */
    .stTooltipIcon { color: #ff00ff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🤑 ARNON Payroll สุดจ๊าบ v.7.7</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏢 รายได้หลัก")
        daily_rate = st.number_input("ค่าแรงพื้นฐานต่อวัน (฿):", min_value=0, value=350, help="เงินเดือนปกติที่พี่ได้รับต่อวัน (คิดฐาน 8 ชม.)")
        c_p, c_l = st.columns(2)
        with c_p: pos_allowance = st.number_input("ค่าตำแหน่ง:", value=0, help="เงินพิเศษตามตำแหน่งงานรายเดือน")
        with c_l: liv_allowance = st.number_input("ค่าครองชีพ:", value=0, help="เงินช่วยเหลือค่าครองชีพรายเดือน")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📅 วันทำงาน/ลา")
        total_days = st.number_input("จำนวนวันทำงานทั้งหมดในเดือน:", value=26, help="จำนวนวันทำงานปกติในเดือนนั้นๆ")
        leave_dates = st.multiselect("จิ้มเลือก 'วันที่ลา':", options=[d for d in range(1, 32)], default=[], help="วันที่พี่ลาพักร้อน/กิจ/ป่วย ระบบจะนำไปหักค่าข้าวและค่ารถ")
        actual_work_days = total_days - len(leave_dates)
        
        st.write("🌈 **เบี้ยขยันวิก 1-2**")
        c_inc1, c_inc2 = st.columns(2)
        with c_inc1: inc1 = st.checkbox("วิกแรก ✅", value=True, help="ถ้าไม่ลาเลยในช่วงวันที่ 1-15 จะได้รับ 350 บาท")
        with c_inc2: inc2 = st.checkbox("วิกสอง ✅", value=True, help="ถ้าไม่ลาเลยในช่วงวันที่ 16-31 จะได้รับ 350 บาท")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🕒 ตั้งค่าโอที (OT)")
        ot_mode = st.radio("เลือกรูปแบบการลงโอที:", ["ลงเป็นจำนวนวัน (วันละ 2.5 ชม.)", "ลงเป็นจำนวนชั่วโมง (ระบุเอง)"], help="เลือกวิธีที่พี่ถนัดในการนับโอที")
        
        hourly_rate = daily_rate / 8
        
        if ot_mode == "ลงเป็นจำนวนวัน (วันละ 2.5 ชม.)":
            d1, d2, d3 = st.columns(3)
            with d1: ot_n_days = st.number_input("วันธรรมดา (1.5x):", value=0, help="คูณ 1.5 เท่าของค่าแรงรายชั่วโมง ทำวันละ 2.5 ชม.")
            with d2: ot_h_days = st.number_input("วันหยุด (2x):", value=0, help="คูณ 2 เท่าของค่าแรงปกติ คิดฐาน 8 ชม. ต่อวัน")
            with d3: ot_s_days = st.number_input("หยุดพิเศษ (3x):", value=0, help="วันหยุดนักขัตฤกษ์ คูณ 3 เท่าของค่าแรงปกติ คิดฐาน 8 ชม. ต่อวัน")
            pay_ot_n = ot_n_days * 2.5 * (hourly_rate * 1.5)
            pay_ot_h = ot_h_days * 8 * (hourly_rate * 2.0)
            pay_ot_s = ot_s_days * 8 * (hourly_rate * 3.0)
        else:
            h1, h2, h3 = st.columns(3)
            with h1: ot_n_hr = st.number_input("ชม. ธรรมดา (1.5x):", value=0.0, help="ระบุชั่วโมงรวมทั้งเดือน คูณ 1.5")
            with h2: ot_h_hr = st.number_input("ชม. วันหยุด (2x):", value=0.0, help="ระบุชั่วโมงรวมทั้งเดือน คูณ 2")
            with h3: ot_s_hr = st.number_input("ชม. หยุดพิเศษ (3x):", value=0.0, help="ระบุชั่วโมงรวมทั้งเดือน คูณ 3")
            pay_ot_n = ot_n_hr * (hourly_rate * 1.5)
            pay_ot_h = ot_h_hr * (hourly_rate * 2.0)
            pay_ot_s = ot_s_hr * (hourly_rate * 3.0)
        st.markdown('</div>', unsafe_allow_html=True)

# --- ส่วนการคำนวณเงิน ---
total_base = (daily_rate * total_days) + pos_allowance + liv_allowance
total_inc = (350 if inc1 else 0) + (350 if inc2 else 0)
total_welfare = (50 + 60) * actual_work_days

gross_income = total_base + pay_ot_n + pay_ot_h + pay_ot_s + total_inc + total_welfare

# หักประกันสังคมจากยอดรวม
st.sidebar.markdown("### 🛡️ ตั้งค่าการหัก")
sso_p = st.sidebar.slider("ประกันสังคม (%)", 0.0, 5.0, 4.0, 0.1, help="เปอร์เซ็นต์ที่หักจากยอดรายได้รวมทั้งหมด")
sso_deduct = int(gross_income * (sso_p / 100))
if sso_deduct > 750: sso_deduct = 750

net_pay = gross_income - sso_deduct

with col2:
    st.subheader("📑 สรุปสลิปเงินเดือน")
    res_table = {
        "รายการรายรับ": ["ค่าแรงพื้นฐาน", "ตำแหน่ง+ครองชีพ", "โอทีรวม", "เบี้ยขยัน", "ข้าว+รถ"],
        "เงิน (฿)": [
            f"{(daily_rate * total_days):,.2f}", f"{(pos_allowance + liv_allowance):,.2f}",
            f"{(pay_ot_n + pay_ot_h + pay_ot_s):,.2f}", f"{total_inc:,.2f}", f"{total_welfare:,.2f}"
        ]
    }
    st.table(pd.DataFrame(res_table))
    
    st.markdown(f"**📉 หักประกันสังคม ({sso_p}%):** -{sso_deduct:,.0f} ฿")
    
    st.markdown(f"""
    <div class="total-box">
        <p style="margin:0; font-size:22px; color:#00ffcc;">💰 ยอดเงินเดือนสุทธิ 💰</p>
        <h1 style="margin:0; font-size:60px; color:#ffffff; text-shadow: 0 0 20px #00ffcc;">฿ {net_pay:,.2f}</h1>
        <p style="margin-top:10px; color:#ff00ff; font-weight:bold;">เอาเมาส์ชี้ที่หัวข้อเพื่อดูวิธีคิดเงินได้เลยครับ!</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("Arnon Payroll v.7.7 | ระบบอธิบายแหล่งที่มาของเงิน (Tooltips Enabled)")
