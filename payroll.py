import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Monthly Payroll", page_icon="💰", layout="wide")

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-title { color: #ffcc00 !important; text-align: center; font-size: 32px !important; font-weight: 900 !important; }
    .card { background-color: #1c2128; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    .total-box { background-color: #0d1117; padding: 25px; border-radius: 15px; border: 2px solid #ffcc00; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💰 JAAO ระบบคิดเงินเดือนรายเดือน v.5.0</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    # --- รายได้คงที่ต่อเดือน ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏢 รายได้ประจำเดือน")
        daily_rate = st.number_input("ค่าแรงพื้นฐานต่อวัน:", min_value=0, value=350)
        c1, c2 = st.columns(2)
        with c1:
            position_allowance = st.number_input("ค่าตำแหน่ง (ต่อเดือน):", min_value=0, value=0)
        with c2:
            living_allowance = st.number_input("ค่าครองชีพ (ต่อเดือน):", min_value=0, value=0)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ข้อมูลการทำงานและการลา ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📅 เช็กวันทำงานและการลา")
        total_days_in_month = st.number_input("จำนวนวันทำงานทั้งหมดในเดือนนี้ (เช่น 26 หรือ 30):", min_value=1, value=26)
        
        c3, c4, c5 = st.columns(3)
        with c3:
            vacation_days = st.number_input("ลาพักร้อน (วัน):", min_value=0, value=0)
        with c4:
            sick_leave = st.number_input("ลาป่วย (วัน):", min_value=0, value=0)
        with c5:
            personal_leave = st.number_input("ลากิจ (วัน):", min_value=0, value=0)
        
        # คำนวณวันมาทำจริง
        actual_work_days = total_days_in_month - (vacation_days + sick_leave + personal_leave)
        st.info(f"✨ วันที่มาทำงานจริง (เพื่อคิดค่าข้าว/เดินทาง): {actual_work_days} วัน")
        
        st.write("---")
        st.write("✅ **เช็กเบี้ยขยัน (ตัดรอบทุก 15 วัน)**")
        incentive_1 = st.checkbox("วิกแรก (1-15) : ไม่ลากิจ/ลาป่วย", value=True)
        incentive_2 = st.checkbox("วิกสอง (16-31) : ไม่ลากิจ/ลาป่วย", value=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- โอทีและสวัสดิการ ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("➕ โอทีและสวัสดิการรายวัน")
        ot_normal_days = st.number_input("จำนวนวันที่ทำ OT ธรรมดา (วันละ 2.5 ชม.):", min_value=0, value=0)
        ot_holiday_days = st.number_input("จำนวนวันที่ทำ OT วันหยุด (คูณ 2 แรง):", min_value=0, value=0)
        
        st.write("---")
        food_rate = st.number_input("ค่าอาหารฟรีต่อวัน (บาท):", min_value=0, value=50)
        travel_rate = st.number_input("ค่าเดินทางต่อวัน (บาท):", min_value=0, value=60)
        st.markdown('</div>', unsafe_allow_html=True)

# --- คำนวณรายได้ทั้งหมด ---
# 1. ค่าแรงพื้นฐาน (จ่ายเต็มตามจำนวนวันในเดือน) + ค่าตำแหน่ง/ครองชีพ
total_base_pay = (daily_rate * total_days_in_month) + position_allowance + living_allowance

# 2. โอทีธรรมดา (2.5 ชม. x 1.5)
hourly_rate = daily_rate / 8
ot_normal_pay = ot_normal_days * 2.5 * (hourly_rate * 1.5)

# 3. โอทีวันหยุด (ค่าแรง x 2 ต่อวัน)
ot_holiday_pay = ot_holiday_days * (daily_rate * 2)

# 4. เบี้ยขยัน (ช่วงละ 350)
total_incentive = (350 if incentive_1 else 0) + (350 if incentive_2 else 0)

# 5. สวัสดิการ (หักลบวันลาออก คิดเฉพาะวันที่มาทำจริง)
total_daily_welfare = (food_rate + travel_rate) * actual_work_days

# 6. รายได้รวม
gross_income = total_base_pay + ot_normal_pay + ot_holiday_pay + total_incentive + total_daily_welfare

# 7. ประกันสังคม (หัก 5% จากฐานรายได้ ไม่เกิน 750)
sso_base = min(total_base_pay, 15000)
sso_deduct = int(sso_base * 0.05)
if sso_deduct > 750: sso_deduct = 750

net_pay = gross_income - sso_deduct

with col2:
    st.subheader("📑 สรุปยอดเงินเดือนสุทธิ")
    
    res_table = {
        "รายการรายรับ": [
            "ค่าแรงพื้นฐานรายเดือน", "ค่าตำแหน่ง + ค่าครองชีพ", 
            "OT วันธรรมดา (1.5x)", "OT วันหยุด (2x แรง)", 
            "เบี้ยขยัน", "สวัสดิการอาหาร+เดินทาง"
        ],
        "จำนวนเงิน (บาท)": [
            f"{(daily_rate * total_days_in_month):,.2f}",
            f"{(position_allowance + living_allowance):,.2f}",
            f"{ot_normal_pay:,.2f}",
            f"{ot_holiday_pay:,.2f}",
            f"{total_incentive:,.2f}",
            f"{total_daily_welfare:,.2f}"
        ],
        "หมายเหตุ": [
            f"คิดจาก {total_days_in_month} วัน", "ยอดคงที่รายเดือน",
            f"{ot_normal_days * 2.5} ชม.", f"{ot_holiday_days} วัน",
            f"วิก 1+2", f"จ่ายเฉพาะที่มาทำ {actual_work_days} วัน"
        ]
    }
    st.table(pd.DataFrame(res_table))
    
    st.error(f"⚠️ มีการลาทั้งหมด: {vacation_days + sick_leave + personal_leave} วัน (หักสวัสดิการออกแล้ว)")
    st.metric("หักประกันสังคม 5%", f"-{sso_deduct:,.0f} ฿")
    
    st.markdown(f"""
    <div class="total-box">
        <p style="margin:0; font-size:22px; color:#ffcc00;">💰 ยอดเงินเดือนสุทธิที่ได้รับ 💰</p>
        <h1 style="margin:0; font-size:60px; color:#ffffff;">฿ {net_pay:,.2f}</h1>
        <p style="margin-top:10px; color:#888;">รายได้รวมทั้งหมดก่อนหัก: {gross_income:,.2f} ฿</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("JAAO Payroll v.5.0 | ระบบหักสวัสดิการตามวันลาจริง")
