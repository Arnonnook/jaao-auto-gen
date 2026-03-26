import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Advanced Payroll", page_icon="💰", layout="wide")

# --- การตกแต่งด้วย CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-title { color: #f0ad4e !important; text-align: center; font-size: 32px !important; font-weight: 900 !important; }
    .card { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    .total-box { background-color: #1c2128; padding: 20px; border-radius: 15px; border: 2px solid #f0ad4e; text-align: center; }
    .incentive-active { color: #5cb85c; font-weight: bold; }
    .incentive-inactive { color: #d9534f; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💰 JAAO ระบบคิดค่าแรงรายวิก v.3.0</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    # --- ส่วนที่ 1: รายได้คงที่ต่อเดือน ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏢 รายได้คงที่ (ต่อเดือน)")
        c1, c2 = st.columns(2)
        with c1:
            position_allowance = st.number_input("ค่าตำแหน่ง (บาท):", min_value=0, value=0)
        with c2:
            living_allowance = st.number_input("ค่าครองชีพ (บาท):", min_value=0, value=0)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนที่ 2: ข้อมูลรายวันและการลา ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📅 ข้อมูลการทำงาน (ต่อวิก)")
        daily_rate = st.number_input("ค่าแรงพื้นฐานต่อวัน:", min_value=0, value=350)
        
        c3, c4 = st.columns(2)
        with c3:
            work_days = st.number_input("วันที่มาทำจริง (วัน):", min_value=0, max_value=16, value=13)
        with c4:
            vacation_days = st.number_input("ลาพักร้อน (วัน):", min_value=0, max_value=16, value=0)
        
        is_absent = st.checkbox("มีการลากิจ / ลาป่วย ในวิกนี้ (ถ้าติ๊กจะไม่ได้เบี้ยขยัน)", value=False)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนที่ 3: โอทีและสวัสดิการรายวัน ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("➕ โอทีและสวัสดิการ")
        ot_normal_days = st.number_input("จำนวนวันที่ทำ OT ธรรมดา (วันละ 2.5 ชม.):", min_value=0, value=0)
        ot_holiday_days = st.number_input("จำนวนวันที่ทำ OT วันหยุด (คูณ 2 แรง):", min_value=0, value=0)
        
        st.write("---")
        food_rate = st.number_input("ค่าอาหารรายวัน (บาท):", min_value=0, value=50)
        travel_rate = st.number_input("ค่าเดินทางรายวัน (บาท):", min_value=0, value=60)
        st.markdown('</div>', unsafe_allow_html=True)

# --- โลจิกคำนวณ ---
# 1. รายได้พื้นฐาน (ค่าแรง + ค่าตำแหน่ง/ครองชีพ หาร 2 ตามวิก)
fixed_income_half = (position_allowance + living_allowance) / 2
base_pay = daily_rate * (work_days + vacation_days)

# 2. โอทีธรรมดา (2.5 ชม. x 1.5)
hourly_rate = daily_rate / 8
ot_normal_total_hours = ot_normal_days * 2.5
ot_normal_pay = ot_normal_total_hours * (hourly_rate * 1.5)

# 3. โอทีวันหยุด (คูณ 2 แรงของวันธรรมดา)
ot_holiday_pay = ot_holiday_days * (daily_rate * 2)

# 4. เบี้ยขยัน (ถ้าไม่ลาเลยได้ 350 ต่อวิก)
incentive_pay = 350 if not is_absent and work_days > 0 else 0

# 5. สวัสดิการรายวัน (เฉพาะวันที่มาทำจริง)
total_food = food_rate * work_days
total_travel = travel_rate * work_days

# 6. รายได้รวมก่อนหัก
gross_income = base_pay + fixed_income_half + ot_normal_pay + ot_holiday_pay + incentive_pay + total_food + total_travel

# 7. ประกันสังคม (หัก 5% ของค่าแรงพื้นฐาน+ค่าตำแหน่ง/ครองชีพ ไม่เกิน 750 ต่อเดือน ดังนั้นวิกนึงไม่ควรเกิน 375)
sso_base = min((base_pay + fixed_income_half), 15000/2)
sso_deduct = int(sso_base * 0.05)
if sso_deduct > 375: sso_deduct = 375

net_pay = gross_income - sso_deduct

with col2:
    st.subheader("📑 สรุปยอดรายได้ประจำวิก")
    
    status_text = "✅ ได้รับ (350.-)" if incentive_pay > 0 else "❌ ไม่ได้รับ (มีการลา)"
    status_color = "incentive-active" if incentive_pay > 0 else "incentive-inactive"

    res_table = {
        "รายการรายรับ": [
            "ค่าแรงพื้นฐาน", "ค่าตำแหน่ง+ครองชีพ (รายวิก)", "OT ธรรมดา (1.5x)", 
            "OT วันหยุด (2x แรง)", "เบี้ยขยันประจำวิก", "ค่าอาหารรวม", "ค่าเดินทางรวม"
        ],
        "จำนวนเงิน (บาท)": [
            f"{base_pay:,.2f}", f"{fixed_income_half:,.2f}", f"{ot_normal_pay:,.2f}",
            f"{ot_holiday_pay:,.2f}", f"{incentive_pay:,.2f}", f"{total_food:,.2f}", f"{total_travel:,.2f}"
        ],
        "รายละเอียด": [
            f"{work_days+vacation_days} วัน", "หารครึ่งจากยอดเดือน", f"{ot_normal_total_hours} ชม.",
            f"{ot_holiday_days} วัน", status_text, f"{work_days} วัน", "ไม่รวมวันลา"
        ]
    }
    st.table(pd.DataFrame(res_table))
    
    st.metric("หักประกันสังคม (วิก)", f"-{sso_deduct:,.0f} ฿")
    
    st.markdown(f"""
    <div class="total-box">
        <p style="margin:0; font-size:20px; color:#f0ad4e;">💰 ยอดเงินโอนสุทธิวิกนี้ 💰</p>
        <h1 style="margin:0; font-size:55px; color:#ffffff;">฿ {net_pay:,.2f}</h1>
        <p style="margin-top:10px; color:#888;">รายได้รวมก่อนหัก: {gross_income:,.2f} ฿</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💡 ให้ AI ช่วยวิเคราะห์ยอดเงิน"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["MY_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"พนักงานได้เงินวิกนี้ {net_pay} บาท ทำโอทีไป {ot_normal_days} วัน และได้เบี้ยขยัน {incentive_pay} บาท ช่วยชมเชยและแนะนำการออมเงินสั้นๆ"
            response = model.generate_content(prompt)
            st.info(response.text)
        except:
            st.success("ยอดวิกนี้สวยมากครับพี่ JAAO! ลุยต่อวิกหน้าครับ!")

st.caption("JAAO Payroll v.3.0 | ระบบคำนวณรายวิกแม่นยำ 100%")
