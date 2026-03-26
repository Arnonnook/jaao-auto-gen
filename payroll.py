import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Monthly Payroll", page_icon="💰", layout="wide")

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-title { color: #00ff88 !important; text-align: center; font-size: 32px !important; font-weight: 900 !important; }
    .card { background-color: #1c2128; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    .total-box { background-color: #0d1117; padding: 25px; border-radius: 15px; border: 2px solid #00ff88; text-align: center; }
    .incentive-check { color: #00ff88; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💰 JAAO ระบบคิดเงินเดือนรายเดือน v.4.0</h1>', unsafe_allow_html=True)

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
        st.subheader("📅 ข้อมูลวันทำงานและการลา")
        c3, c4 = st.columns(2)
        with c3:
            work_days = st.number_input("วันที่มาทำจริง (วัน):", min_value=0, max_value=31, value=26)
        with c4:
            vacation_days = st.number_input("ลาพักร้อน (วัน):", min_value=0, max_value=31, value=0)
        
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
        food_rate = st.number_input("ค่าอาหารรายวัน (บาท):", min_value=0, value=50)
        travel_rate = st.number_input("ค่าเดินทางรายวัน (บาท):", min_value=0, value=60)
        st.markdown('</div>', unsafe_allow_html=True)

# --- คำนวณรายได้ทั้งหมด ---
# 1. ค่าแรง + ค่าตำแหน่ง + ค่าครองชีพ
total_base_pay = (daily_rate * (work_days + vacation_days)) + position_allowance + living_allowance

# 2. โอทีธรรมดา (2.5 ชม. x 1.5)
hourly_rate = daily_rate / 8
ot_normal_pay = ot_normal_days * 2.5 * (hourly_rate * 1.5)

# 3. โอทีวันหยุด (ค่าแรง x 2 ต่อวัน)
ot_holiday_pay = ot_holiday_days * (daily_rate * 2)

# 4. เบี้ยขยัน (ช่วงละ 350)
total_incentive = (350 if incentive_1 else 0) + (350 if incentive_2 else 0)

# 5. สวัสดิการ (เฉพาะวันที่มาทำจริง)
total_daily_welfare = (food_rate + travel_rate) * work_days

# 6. รายได้รวม
gross_income = total_base_pay + ot_normal_pay + ot_holiday_pay + total_incentive + total_daily_welfare

# 7. ประกันสังคม (5% ของค่าแรง+ตำแหน่ง+ครองชีพ สูงสุด 750)
sso_base = min((daily_rate * (work_days + vacation_days)) + position_allowance + living_allowance, 15000)
sso_deduct = int(sso_base * 0.05)
if sso_deduct > 750: sso_deduct = 750

net_pay = gross_income - sso_deduct

with col2:
    st.subheader("📑 สรุปยอดเงินเดือนสุทธิ")
    
    res_table = {
        "รายการรายรับ": [
            "ค่าแรงพื้นฐาน (รวมลาพักร้อน)", "ค่าตำแหน่ง + ค่าครองชีพ", 
            "OT วันธรรมดา (1.5x)", "OT วันหยุด (2x แรง)", 
            "เบี้ยขยัน (วิก 1 + วิก 2)", "สวัสดิการอาหาร+เดินทาง"
        ],
        "จำนวนเงิน (บาท)": [
            f"{(daily_rate * (work_days + vacation_days)):,.2f}",
            f"{(position_allowance + living_allowance):,.2f}",
            f"{ot_normal_pay:,.2f}",
            f"{ot_holiday_pay:,.2f}",
            f"{total_incentive:,.2f}",
            f"{total_daily_welfare:,.2f}"
        ],
        "รายละเอียด": [
            f"{work_days+vacation_days} วัน", "ยอดคงที่รายเดือน",
            f"{ot_normal_days * 2.5} ชม.", f"{ot_holiday_days} วัน",
            f"{total_incentive} บาท", f"{work_days} วันที่มาจริง"
        ]
    }
    st.table(pd.DataFrame(res_table))
    
    st.metric("หักประกันสังคม 5%", f"-{sso_deduct:,.0f} ฿")
    
    st.markdown(f"""
    <div class="total-box">
        <p style="margin:0; font-size:22px; color:#00ff88;">💰 ยอดเงินเดือนสุทธิที่ได้รับ 💰</p>
        <h1 style="margin:0; font-size:60px; color:#ffffff;">฿ {net_pay:,.2f}</h1>
        <p style="margin-top:10px; color:#888;">รายได้รวมทั้งหมด: {gross_income:,.2f} ฿</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💡 วิเคราะห์การเงินเดือนนี้"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["MY_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"พนักงานรายได้สุทธิ {net_pay} บาท ทำโอที {ot_normal_days} วัน และได้เบี้ยขยัน {total_incentive} บาท ช่วยชมเชยสั้นๆ"
            response = model.generate_content(prompt)
            st.info(response.text)
        except:
            st.success("เดือนนี้พี่ JAAO ทำงานเก่งมากครับ!")

st.write("---")
st.caption("JAAO Payroll v.4.0 |Monthly System | คิดเงินเดือนครั้งเดียว เบี้ยขยันตัดรายวิก")
