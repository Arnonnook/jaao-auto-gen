import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Arnon คิดเงินเดือนสุดจ๊าบ", page_icon="🤑", layout="wide")

# --- การตกแต่งด้วย CSS สีสันสดใส (Neon & Vibrant) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    .main-title { 
        color: #00ffcc !important; 
        text-align: center; 
        font-size: 45px !important; 
        font-weight: 900 !important;
        text-shadow: 2px 2px 10px #00ffcc;
    }
    .card { 
        background-color: #1a1a1a; 
        padding: 25px; 
        border-radius: 20px; 
        border: 2px solid #ff00ff; /* เส้นขอบสีชมพูนีออน */
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
    }
    .total-box { 
        background-color: #000000; 
        padding: 30px; 
        border-radius: 25px; 
        border: 4px solid #00ffcc; /* เส้นขอบสีเขียวนีออน */
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
    }
    h2, h3 { color: #ff00ff !important; }
    .stNumberInput label, .stSelectbox label, .stCheckbox label {
        color: #00ffcc !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🤑 ARNON คิดเงินเดือนสุดจ๊าบ v.6.0</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏢 รายได้ประจำเดือน")
        daily_rate = st.number_input("ค่าแรงพื้นฐานต่อวัน:", min_value=0, value=350)
        c1, c2 = st.columns(2)
        with c1:
            position_allowance = st.number_input("ค่าตำแหน่ง:", min_value=0, value=0)
        with c2:
            living_allowance = st.number_input("ค่าครองชีพ:", min_value=0, value=0)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📅 เช็กวันทำงานและการลา")
        total_days = st.number_input("จำนวนวันทำงานในเดือนนี้:", min_value=1, value=26)
        c3, c4, c5 = st.columns(3)
        with c3: vacation_days = st.number_input("พักร้อน (วัน):", value=0)
        with c4: sick_leave = st.number_input("ลาป่วย (วัน):", value=0)
        with c5: personal_leave = st.number_input("ลากิจ (วัน):", value=0)
        
        actual_work_days = total_days - (vacation_days + sick_leave + personal_leave)
        st.markdown(f"✨ **มาทำงานจริง: {actual_work_days} วัน** (เพื่อคิดค่าข้าว/เดินทาง)")
        
        st.write("---")
        st.write("🌈 **เบี้ยขยันสุดจ๊าบ (350.- / วิก)**")
        incentive_1 = st.checkbox("วิกแรก (1-15) : ผ่าน! ✅", value=True)
        incentive_2 = st.checkbox("วิกสอง (16-31) : ผ่าน! ✅", value=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("➕ โอทีและสวัสดิการ")
        ot_normal_days = st.number_input("OT ธรรมดา (กี่วัน? วันละ 2.5 ชม.):", value=0)
        ot_holiday_days = st.number_input("OT วันหยุด (กี่วัน? 2 แรง):", value=0)
        st.write("---")
        food_rate = st.number_input("ค่าอาหารฟรี (ต่อวัน):", value=50)
        travel_rate = st.number_input("ค่าเดินทาง (ต่อวัน):", value=60)
        st.markdown('</div>', unsafe_allow_html=True)

# --- คำนวณ (สูตรใหม่ ประกันสังคม 4%) ---
total_base_pay = (daily_rate * total_days) + position_allowance + living_allowance
hourly_rate = daily_rate / 8
ot_normal_pay = ot_normal_days * 2.5 * (hourly_rate * 1.5)
ot_holiday_pay = ot_holiday_days * (daily_rate * 2)
total_incentive = (350 if incentive_1 else 0) + (350 if incentive_2 else 0)
total_welfare = (food_rate + travel_rate) * actual_work_days

gross_income = total_base_pay + ot_normal_pay + ot_holiday_pay + total_incentive + total_welfare

# คำนวณประกันสังคม 4% ตามที่พี่อานนท์คำนวณมา (626 จาก 15,580.50)
sso_rate = 0.04 
sso_deduct = int(total_base_pay * sso_rate)
# ใส่เพดานเผื่อไว้ แต่ถ้าตาม 4% ของ 15,000 จะอยู่ที่ 600 บาท
if sso_deduct > 626 and total_base_pay <= 16000: sso_deduct = 626 

net_pay = gross_income - sso_deduct

with col2:
    st.subheader("📑 สรุปยอดเงินเดือนของพี่อานนท์")
    
    res_table = {
        "รายการ": ["ค่าแรงพื้นฐาน", "ค่าตำแหน่ง+ครองชีพ", "OT ธรรมดา", "OT วันหยุด", "เบี้ยขยันรวม", "อาหาร+เดินทาง"],
        "ยอดเงิน (฿)": [
            f"{(daily_rate * total_days):,.2f}", f"{(position_allowance + living_allowance):,.2f}",
            f"{ot_normal_pay:,.2f}", f"{ot_holiday_pay:,.2f}", f"{total_incentive:,.2f}", f"{total_welfare:,.2f}"
        ]
    }
    st.table(pd.DataFrame(res_table))
    
    st.markdown(f"**📉 หักประกันสังคม (4%):** -{sso_deduct:,.0f} ฿")
    
    st.markdown(f"""
    <div class="total-box">
        <p style="margin:0; font-size:25px; color:#00ffcc;">💰 ยอดเงินโอนเข้ากระเป๋า 💰</p>
        <h1 style="margin:0; font-size:70px; color:#ffffff; text-shadow: 0 0 20px #00ffcc;">฿ {net_pay:,.2f}</h1>
        <p style="margin-top:10px; color:#ff00ff; font-weight:bold;">จ๊าบสุดๆ ไปเลยครับพี่!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✨ ให้ AI อวยพรเงินเดือนใหม่"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["MY_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"พนักงานชื่ออานนท์ ได้เงินเดือน {net_pay} บาท ช่วยอวยพรแบบสุดจ๊าบและกวนๆ หน่อย"
            response = model.generate_content(prompt)
            st.success(response.text)
        except:
            st.write("ยินดีด้วยครับพี่อานนท์ เงินเดือนรอบนี้อย่างโหด!")
