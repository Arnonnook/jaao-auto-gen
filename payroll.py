import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Personal Payroll", page_icon="💰", layout="wide")

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-title { color: #00d4ff !important; text-align: center; font-size: 35px !important; font-weight: 900 !important; }
    .card { background-color: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; }
    .highlight { color: #00d4ff; font-weight: bold; }
    .total-box { background-color: #0d1117; padding: 25px; border-radius: 15px; border: 2px solid #00d4ff; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💰 JAAO ระบบคิดค่าแรงละเอียด v.2.0</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📅 ข้อมูลการทำงาน")
        daily_rate = st.number_input("ค่าแรงพื้นฐานต่อวัน (บาท):", min_value=0, value=350)
        work_days = st.number_input("วันที่มาทำงานจริง (วัน):", min_value=0, max_value=31, value=22)
        vacation_days = st.number_input("วันที่ลาพักร้อน (ได้ค่าแรงแต่ไม่ได้ค่าเดินทาง):", min_value=0, max_value=31, value=0)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("➕ รายได้เสริม / โอที")
        # โอทีวันธรรมดา (1.5 เท่า)
        ot_normal = st.number_input("OT วันธรรมดา (ชั่วโมง):", min_value=0.0, value=0.0)
        # โอทีวันหยุด (2 เท่า)
        ot_holiday = st.number_input("OT วันหยุด (ชั่วโมง - คูณ 2 แรง):", min_value=0.0, value=0.0)
        
        st.write("---")
        st.subheader("🍱 สวัสดิการพิเศษ (ต่อวันที่มาทำจริง)")
        food_allowance = st.number_input("ค่าอาหารฟรีต่อวัน (บาท):", min_value=0, value=50)
        travel_allowance = st.number_input("ค่าเดินทางต่อวัน (บาท):", min_value=0, value=60)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚫 รายการหัก")
        social_security = st.checkbox("หักประกันสังคม 5% (ตามกฎหมายไทยสูงสุด 750.-)", value=True)
        other_deduct = st.number_input("รายการหักอื่นๆ (ถ้ามี):", min_value=0, value=0)
        st.markdown('</div>', unsafe_allow_html=True)

# --- ส่วนการคำนวณโลจิก ---
# 1. รายได้พื้นฐาน (รวมวันทำงานจริงและวันพักร้อน)
base_income = daily_rate * (work_days + vacation_days)

# 2. คำนวณ OT
hourly_rate = daily_rate / 8
ot_normal_pay = ot_normal * (hourly_rate * 1.5)
ot_holiday_pay = ot_holiday * (hourly_rate * 2.0) # คูณ 2 แรงตามโจทย์

# 3. คำนวณสวัสดิการ (เฉพาะวันที่มาทำงานจริง ไม่รวมวันลาพักร้อน)
total_food = food_allowance * work_days
total_travel = travel_allowance * work_days

# 4. รายได้รวมก่อนหัก
gross_income = base_income + ot_normal_pay + ot_holiday_pay + total_food + total_travel

# 5. คำนวณประกันสังคม (คิดจากฐานเงินเดือน ไม่เกิน 15,000 บาท)
sso_base = min(base_income, 15000)
sso_deduct = int(sso_base * 0.05) if social_security else 0
if sso_deduct > 750: sso_deduct = 750

# 6. สรุปเงินสุทธิ
total_deductions = sso_deduct + other_deduct
net_pay = gross_income - total_deductions

with col2:
    st.subheader("📑 สรุปรายละเอียดสลิปเงินเดือน")
    
    res_data = {
        "รายการรายรับ": ["ค่าแรงพื้นฐาน (รวมวันลา)", "OT วันธรรมดา (1.5x)", "OT วันหยุด (2x)", "ค่าอาหารรวม", "ค่าเดินทางรวม"],
        "จำนวนเงิน (บาท)": [
            f"{base_income:,.2f}",
            f"{ot_normal_pay:,.2f}",
            f"{ot_holiday_pay:,.2f}",
            f"{total_food:,.2f}",
            f"{total_travel:,.2f}"
        ],
        "หมายเหตุ": [f"({work_days}+{vacation_days} วัน)", f"{ot_normal} ชม.", f"{ot_holiday} ชม.", f"{work_days} วัน", "ไม่รวมวันลา"]
    }
    st.table(pd.DataFrame(res_data))
    
    st.write("---")
    st.subheader("📉 รายการหัก")
    col_a, col_b = st.columns(2)
    col_a.metric("ประกันสังคม (5%)", f"-{sso_deduct:,.0f} ฿")
    col_b.metric("หักอื่นๆ", f"-{other_deduct:,.0f} ฿")
    
    st.write("---")
    st.markdown(f"""
    <div class="total-box">
        <p style="margin:0; font-size:22px; color:#00d4ff;">💰 รายรับสุทธิเดือนนี้ 💰</p>
        <h1 style="margin:0; font-size:50px; color:#ffffff;">฿ {net_pay:,.2f}</h1>
        <p style="margin-top:10px; color:#888;">ยอดรวมรายได้ทั้งหมด: {gross_income:,.2f} ฿</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💡 ขอคำแนะนำการออมเงินเดือนนี้"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["MY_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"พนักงานมีรายได้สุทธิ {net_pay} บาท โดยมีค่าใช้จ่ายคงที่คือประกันสังคม {sso_deduct} บาท ช่วยวางแผนการเงินสั้นๆ ให้หน่อย"
            response = model.generate_content(prompt)
            st.info(response.text)
        except:
            st.write("ยินดีด้วยครับพี่ JAAO เดือนนี้ทำผลงานได้เยี่ยมมาก!")

st.write("---")
st.caption("JAAO Pro Payroll v.2.0 | คำนวณตามกฎหมายแรงงานไทยและเงื่อนไขส่วนบุคคล")
