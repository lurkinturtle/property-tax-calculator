import streamlit as st

# Configure page style to look like a modern mobile/desktop app
st.set_page_config(page_title="Bell County Housing Cost Estimator", page_icon="🏠", layout="centered")

st.title("🏠 Central Texas Total Housing Cost Estimator")
st.write("Estimate your complete monthly payment including Principal, Interest, Taxes, and Insurance (PITI).")

# --- DATA LAYERS ---
base_rates = {
    "Belton": 0.010370,
    "Temple": 0.012144,
    "Morgan's Point Resort": 0.009526,
    "Moffat": 0.004128,
    "Salado": 0.007359,
    "Little River-Academy": 0.007028
}

isd_rates = {
    "Belton ISD": 0.011494,
    "Temple ISD": 0.011372,
    "Salado ISD": 0.011669,
    "Academy ISD": 0.011489
}

# --- MOBILE FRIENDLY INPUT FORM ---
with st.form("calculator_form"):
    st.subheader("1. Property Details")
    
    home_price = st.number_input(
        "Property Purchase Price ($)",
        min_value=100000, max_value=1500000, value=300000, step=1000, format="%d"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox("Location / City Limits", list(base_rates.keys()), index=0)
    with col2:
        selected_isd = st.selectbox("School District (ISD)", list(isd_rates.keys()), index=0)
        
    homestead = st.checkbox("Apply Texas Homestead Exemption ($110,000 School Tax Discount)", value=True)
    
    st.markdown("---")
    st.subheader("2. Financing & Insurance")
    
    col3, col4, col5 = st.columns(3)
    with col3:
        down_payment_pct = st.number_input("Down Payment (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
    with col4:
        interest_rate = st.number_input("Interest Rate (%)", min_value=1.0, max_value=15.0, value=6.5, step=0.125)
    with col5:
        loan_term_years = st.selectbox("Loan Term", [30, 15], index=0)
        
    annual_insurance = st.number_input(
        "Estimated Annual Homeowners Insurance ($)",
        min_value=0, max_value=10000, value=2400, step=100
    )
    
    submit_button = st.form_submit_button(label="🚀 Calculate Total Payment")

# --- MATH LOGIC & DISPLAY ---
if submit_button or home_price:
    # 1. Tax Math
    city_base_rate = base_rates[selected_city]
    isd_rate = isd_rates[selected_isd]
    taxable_isd_value = max(0, home_price - 110000) if homestead else home_price
    
    annual_base_tax = home_price * city_base_rate
    annual_isd_tax = taxable_isd_value * isd_rate
    total_annual_tax = annual_base_tax + annual_isd_tax
    monthly_tax = total_annual_tax / 12
    
    # 2. Mortgage Math (Principal & Interest)
    down_payment_amount = home_price * (down_payment_pct / 100)
    loan_amount = home_price - down_payment_amount
    
    # Monthly interest calculation
    monthly_rate = (interest_rate / 100) / 12
    total_payments = loan_term_years * 12
    
    if monthly_rate > 0:
        monthly_p_and_i = loan_amount * (monthly_rate * (1 + monthly_rate) ** total_payments) / ((1 + monthly_rate) ** total_payments - 1)
    else:
        monthly_p_and_i = loan_amount / total_payments
        
    # 3. Insurance Math
    monthly_insurance = annual_insurance / 12
    
    # 4. Grand Total (PITI)
    total_monthly_payment = monthly_p_and_i + monthly_tax + monthly_insurance

    # --- DISPLAY RESULTS ---
    st.markdown("---")
    st.subheader("Estimated Total Monthly Payment (PITI)")
    
    # Massive summary metric for quick scanning on phones
    st.metric(
        label="Total Estimated Monthly Out-of-Pocket", 
        value=f"${total_monthly_payment:,.2f}",
        help="Includes Principal, Interest, Local Taxes, and Homeowners Insurance Escrow."
    )
    
    # Visual columns breaking down the pillars of the payment
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="Principal & Interest", value=f"${monthly_p_and_i:,.2f}")
    with m_col2:
        st.metric(label="Taxes (Escrow)", value=f"${monthly_tax:,.2f}")
    with m_col3:
        st.metric(label="Insurance (Escrow)", value=f"${monthly_insurance:,.2f}")
        
    # Detailed Breakdown expander for the full picture
    with st.expander("View Full Financial Details"):
        st.markdown(f"**Total Loan Amount:** ${loan_amount:,.2f} *(Down Payment: ${down_payment_amount:,.2f})*")
        st.write(f"**Taxable School Value:** ${taxable_isd_value:,}")
        st.write(f"**City/County Base Tax ({city_base_rate*100:.4f}%):** ${annual_base_tax:,.2f}/yr")
        st.write(f"**School District Tax ({isd_rate*100:.4f}%):** ${annual_isd_tax:,.2f}/yr")
        st.write(f"**Total Combined Tax Rate:** {(city_base_rate + isd_rate)*100:.4f}%")
