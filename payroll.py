import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JAAO Payroll Master", page_icon="💰", layout="wide")

# --- การตกแต่งด้วย CSS (สไตล์แอปธนาคาร/บัญชี) ---
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; color: #1e1e1e; }
    .payroll-title {
        color: #2e7d32 !important; /* สีเขียวเงินตรา */
        text-align: center;
        font-size: 35px !important;
        font-weight: 900 !important;
    }
    .salary-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 5px solid #2e7d32;
    }
    .total-box {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 2px dashed #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# 2. ส่วนหน้าจอหลัก
st.markdown('<h1 class="payroll-title">💰 JAAO PAYROLL MASTER</h1>', unsafe_allow_html=True)
st.write("---")

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📋 บันทึกข้อมูลรายได้")
    
    with st.container():
        st.markdown('<div class="salary-card">', unsafe_allow_html=True)
        emp_name = st.text_input("ชื่อพนักงาน / ชื่อตัวเอง:", value="พนักงาน A")
        base_salary = st.number_input("เงินเดือนพื้นฐาน (บาท):", min_value=0, value=15000, step=500)
        
        col1, col2 = st.columns(2)
        with col1:
            ot_hours = st.number_input("ชั่วโมง OT:", min_value=0, value=0)
            ot_rate = st.number_input("อัตรา OT ต่อชม.:", min_value=0, value=150)
        with col2:
            bonus = st.number_input("ค่าคอมมิชชัน/โบนัส:", min_value=0, value=0)
            allowance = st.number_input("ค่าเบี้ยเลี้ยง/อื่นๆ:", min_value=0, value=0)
            
        st.write("---")
        st.write("🚫 **รายการหัก**")
        social_security = st.checkbox("หักประกันสังคม (5% สูงสุด 750.-)", value=True)
        tax_deduct = st.number_input("หักภาษี ณ ที่จ่าย (%):", min_value=0, max_value=100, value=0)
        other_deduct = st.number_input("รายการหักอื่นๆ:", min_value=0, value=0)
        st.markdown('</div>', unsafe_allow_html=True)

# 3. ส่วนการคำนวณ
# คำนวณรายรับ
total_ot = ot_hours * ot_rate
gross_income = base_salary + total_ot + bonus + allowance

# คำนวณรายหัก
sso_amount = min(base_salary * 0.05, 750) if social_security else 0
tax_amount = gross_income * (tax_deduct / 100)
total_deduction = sso_amount + tax_amount + other_deduct

# รายได้สุทธิ
net_salary = gross_income - total_deduction

with col_right:
    st.subheader("📊 สรุปรายการรับ-จ่าย")
    
    # ตารางสรุปแบบสวยงาม
    data = {
        "รายการ": ["เงินเดือนพื้นฐาน", "ค่า OT", "โบนัส/ค่าคอม", "ค่าเบี้ยเลี้ยง", "หักประกันสังคม", "หักภาษี", "หักอื่นๆ"],
        "จำนวนเงิน (บาท)": [
            f"{base_salary:,.2f}", 
            f"{total_ot:,.2f}", 
            f"{bonus:,.2f}", 
            f"{allowance:,.2f}", 
            f"-{sso_amount:,.2f}", 
            f"-{tax_amount:,.2f}", 
            f"-{other_deduct:,.2f}"
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)
    
    st.markdown(f"""
    <div class="total-box">
        <p style="margin:0; font-size:18px;">รายรับสุทธิที่ต้องจ่าย (Net Salary)</p>
        <h2 style="margin:0; color:#2e7d32;">฿ {net_salary:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # ฟีเจอร์ AI ช่วยเขียนคำนิยมหรือบันทึกท้ายสลิป
    if st.button("📝 ให้ AI ช่วยเขียนคำขอบคุณท้ายสลิป"):
        import google.generativeai as genai
        try:
            genai.configure(api_key=st.secrets["MY_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"เขียนข้อความสั้นๆ ขอบคุณและให้กำลังใจพนักงานชื่อ {emp_name} ที่ทำงานหนักในเดือนนี้ ให้รู้สึกประทับใจ"
            response = model.generate_content(prompt)
            st.info(response.text)
        except:
            st.write(f"ขอบคุณคุณ {emp_name} สำหรับความตั้งใจทำงานในเดือนนี้ครับ!")

st.write("---")
st.caption(f"© 2026 JAAO Payroll Studio | อัปเดตล่าสุด: {pd.Timestamp.now().strftime('%d/%m/%Y')}")
