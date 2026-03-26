import streamlit as st
import pandas as pd
from datetime import date

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Arnon คิดเงินเดือนสุดจ๊าบ v.7.0", page_icon="📅", layout="wide")

# --- CSS สไตล์นีออนสดใส ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    .main-title { 
        color: #00ffcc !important; text-align: center; font-size: 40px !important; 
        font-weight: 900 !important; text-shadow: 2px 2px 15px #00ffcc;
    }
    .card { 
        background-color: #1a1a1a; padding: 20px; border-radius: 20px; 
        border: 2px solid #ff00ff; margin-bottom: 15px;
    }
    .total-box { 
        background-color: #000; padding: 25px; border-radius: 25px; 
        border: 4px solid #00ffcc; text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
    }
    label { color: #00ffcc !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🤑 ARNON คิดเงินเดือนสุดจ๊าบ v.7.0</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    # --- รายได้ประจำเดือน ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏢 รายได้ประจำเดือน")
        daily_rate = st.number_input("ค่าแรงพื้นฐานต่อวัน:", min_value=0, value=350)
        c1, c2 = st.columns(2)
        with c1: position_allowance = st.number_input("ค่าตำแหน่ง:", value=0)
        with c2: living_allowance = st.number_input("ค่าครองชีพ:", value=0)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนใหม่: ปฏิทินเลือกวันลา ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📅 บันทึกวันลาจากปฏิทิน")
        total_days = st.number_input("จำนวนวันทำงานทั้งหมดในเดือนนี้:", value=26)
        
        # ปฏิทินเลือกวันลา
        leave_dates = st.multiselect(
            "จิ้มเลือก 'วันที่พี่ลา' (พักร้อน/กิจ/ป่วย):",
            options=[d for d in range(1, 32)],
            default=[],
            help="เลือกวันที่พี่ไม่ได้มาทำงานจริง ระบบจะนับจำนวนวันให้เองครับ"
        )
        
        total_leave_days = len(leave_dates)
        actual_work_days = total_days - total_leave_days
        
        st.markdown(f"🚫 **รวมวันลาทั้งหมด:** <span style='color:#ff00ff; font-size:20px;'>{total_leave_days}</span> วัน", unsafe_allow_html=True)
        st.markdown(f"✨ **มาทำงานจริง:** <span style='color:#00ffcc; font-size:20px;'>{actual_work_days}</span> วัน", unsafe_allow_html=True)
        
        st.write("---")
        st.write("🌈 **เบี้ยขยัน (350.- / วิก)**")
        incentive_1 = st.checkbox("วิกแรก (1-15) : ไม่ลากิจ/ป่วย ✅", value=True)
        incentive_2 = st.checkbox("วิกสอง (16-31) : ไม่ลากิจ/ป่วย ✅", value=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ปรับเปอร์เซ็นต์ประกันสังคม ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🛡️ ตั้งค่าประกันสังคม")
        # แถบเลื่อนปรับ % เองได้เลย
        sso_percent = st.slider("เลือก % ที่โดนหัก:", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
        st.markdown('</div>', unsafe_allow_html=True)

# --- คำนวณรายได้ ---
total_base_pay = (daily_rate * total_days) + position_allowance + living_allowance
# OT ธรรมดา (สมมติว่าพี่ทำ 2.5 ชม. ทุกวันที่มาทำงานจริง หรือเลือกกรอกเอง)
ot_days = st.sidebar.number_input("จำนวนวันที่ทำ OT ธรรมดา (2.5 ชม.):", value=0)
ot_holiday = st.sidebar.number_input("จำนวนวันที่ทำ OT วันหยุด (2 แรง):", value=0)

ot_normal_pay = ot_days * 2.5 * ((daily_rate / 8) * 1.5)
ot_holiday_pay = ot_holiday * (daily_rate * 2)
total_incentive = (350 if incentive_1 else 0) + (350 if incentive_2 else 0)
total_welfare = (50 + 60) * actual_work_days # ค่าอาหาร 50 + เดินทาง 60

gross_income = total_base_pay + ot_normal_pay + ot_holiday_pay + total_incentive + total_welfare

# คำนวณประกันสังคมตาม % ที่เลือก
sso_deduct = int(total_base_pay * (sso_percent / 100))
if sso_deduct > 750: sso_deduct = 750 # เพดานสูงสุดตามกฎหมายไทย

net_pay = gross_income - sso_deduct

with col2:
    st.subheader("📊 สรุปยอดสุดจ๊าบของพี่อานนท์")
    
    res_table = {
        "รายการ": ["ค่าแรงพื้นฐาน", "ตำแหน่ง+ครองชีพ", "OT รวม", "เบี้ยขยัน", "อาหาร+เดินทาง"],
        "ยอดเงิน (฿)": [
            f"{(daily_rate * total_days):,.2f}", f"{(position_allowance + living_allowance):,.2f}",
            f"{(ot_normal_pay + ot_holiday_pay):,.2f}", f"{total_incentive:,.2f}", f"{total_welfare:,.2f}"
        ]
    }
    st.table(pd.DataFrame(res_table))
    
    st.markdown(f"**📉 หักประกันสังคม ({sso_percent}%):** -{sso_deduct:,.0f} ฿")
    
    st.markdown(f"""
    <div class="total-box">
        <p style="margin:0; font-size:25px; color:#00ffcc;">💰 ยอดเงินเดือนสุทธิ 💰</p>
        <h1 style="margin:0; font-size:65px; color:#ffffff;">฿ {net_pay:,.2f}</h1>
        <p style="margin-top:10px; color:#ff00ff; font-weight:bold;">เงินเข้าเน้นๆ จ๊าบแน่นอน!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 ส่ง AI ไปคำนวณความรวย"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["MY_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"พนักงานชื่ออานนท์ เงินเดือน {net_pay} บาท หักประกันสังคม {sso_percent}% ช่วยอวยพรสั้นๆ"
            response = model.generate_content(prompt)
            st.success(response.text)
        except:
            st.write("เดือนนี้รวยๆ ครับพี่อานนท์!")
