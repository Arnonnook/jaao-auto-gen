import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Daily Tracker", page_icon="📝", layout="wide")

# --- การตกแต่งด้วย CSS สไตล์สมุดบัญชีส่วนตัว ---
st.markdown("""
<style>
    .stApp { background-color: #1e1e1e; color: #ffffff; }
    .main-title { color: #00ff88 !important; text-align: center; font-size: 35px !important; font-weight: 900 !important; }
    .card { background-color: #2d2d2d; padding: 20px; border-radius: 15px; border-top: 5px solid #00ff88; margin-bottom: 20px; }
    .result-box { background-color: #004d33; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #00ff88; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📝 JAAO รายรับ-รายจ่าย รายวัน</h1>', unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💰 คำนวณรายได้")
    
    daily_rate = st.number_input("ค่าแรงรายวัน (บาท):", min_value=0, value=350, step=10)
    work_days = st.number_input("จำนวนวันที่ทำงานในเดือนนี้:", min_value=0, max_value=31, value=26)
    
    st.write("---")
    st.write("🕒 **ค่าล่วงเวลา (OT)**")
    ot_hours = st.number_input("จำนวนชั่วโมง OT รวมทั้งเดือน:", min_value=0, value=0)
    ot_multiplier = st.number_input("ตัวคูณ OT (เช่น 1.5 หรือ 2):", min_value=1.0, value=1.5, step=0.1)
    
    # คำนวณค่าแรงต่อชั่วโมง (คิดจาก 8 ชม. ต่อวัน)
    hourly_rate = daily_rate / 8
    total_ot_money = ot_hours * (hourly_rate * ot_multiplier)
    
    total_income = (daily_rate * work_days) + total_ot_money
    
    st.markdown(f"**รายได้รวม: {total_income:,.2f} บาท**")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🚫 รายจ่าย/เงินหัก")
    food_per_day = st.number_input("ค่ากิน+เดินทาง (ต่อวัน):", min_value=0, value=150)
    monthly_fixed = st.number_input("ค่าห้อง/ค่าน้ำ-ไฟ/หนี้สิน (ต่อเดือน):", min_value=0, value=0)
    other_expense = st.number_input("ค่าใช้จ่ายอื่นๆ:", min_value=0, value=0)
    
    total_daily_expense = food_per_day * work_days
    total_expense = total_daily_expense + monthly_fixed + other_expense
    st.markdown('</div>', unsafe_allow_html=True)

# 4. ส่วนสรุปผล
net_profit = total_income - total_expense

with col2:
    st.subheader("📊 สรุปเงินเหลือรายเดือน")
    
    summary_data = {
        "รายการ": ["ค่าแรงพื้นฐาน", "เงิน OT ทั้งเดือน", "ค่ากิน+เดินทาง (รวม)", "ค่าคงที่ (ที่พัก/หนี้)", "ค่าใช้จ่ายอื่น"],
        "จำนวนเงิน": [
            f"{daily_rate * work_days:,.2f}",
            f"{total_ot_money:,.2f}",
            f"-{total_daily_expense:,.2f}",
            f"-{monthly_fixed:,.2f}",
            f"-{other_expense:,.2f}"
        ]
    }
    st.table(pd.DataFrame(summary_data))
    
    st.markdown(f"""
    <div class="result-box">
        <p style="margin:0; font-size:20px; color:#00ff88;">💰 เดือนนี้เหลือเงินสุทธิ 💰</p>
        <h1 style="margin:0; color:#ffffff;">฿ {net_profit:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

    # ฟีเจอร์ AI แนะนำการออม
    if st.button("💡 ให้ AI ช่วยวางแผนการเงิน"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["MY_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"ฉันมีเงินเหลือหลังหักค่าใช้จ่ายเดือนนี้ {net_profit} บาท จากรายได้ {total_income} บาท ช่วยแนะนำการเก็บออมหรือการใช้เงินให้คุ้มค่าหน่อย"
            response = model.generate_content(prompt)
            st.info(response.text)
        except:
            st.write("ลองแบ่งเก็บออม 10% ของเงินที่เหลือนดูนะครับพี่ JAAO!")

st.write("---")
st.caption("JAAO Daily Tracker | คิดเอง ใช้เอง เหลือเงินเก็บเอง")
