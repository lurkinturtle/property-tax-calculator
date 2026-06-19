import streamlit as st

# Configure page style to look like a modern mobile/desktop app
st.set_page_config(page_title="Bell County Tax Calculator", page_icon="🏠", layout="centered")

st.title("🏠 Central Texas Property Tax Calculator")
st.write("Quickly estimate monthly escrow and annual property tax layers.")

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
# Wrapping everything in st.form prevents Streamlit from rerunning until the button is clicked!
with st.form("calculator_form"):
    st.subheader("Calculator Inputs")
    
    # Clean manual numeric input box
    home_price = st.number_input(
        "Property Purchase Price ($)",
        min_value=100000,
        max_value=1500000,
        value=300000,
        step=100,
        format="%d"
    )
    
    # Dropdown selectors inside the form
    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox("Location / City Limits", list(base_rates.keys()), index=0)
    with col2:
        selected_isd = st.selectbox("School District (ISD)", list(isd_rates.keys()), index=0)
        
    homestead = st.checkbox("Apply Texas Homestead Exemption ($110,000 School Tax Discount)", value=True)
    
    # The magical mobile friendly submit button
    submit_button = st.form_submit_button(label="🚀 Calculate")

# --- MATH LOGIC & DISPLAY ---
# This code executes cleanly when the user hits the button
if submit_button or home_price:
    city_base_rate = base_rates[selected_city]
    isd_rate = isd_rates[selected_isd]
    
    # Apply homestead deduction logic safely
    taxable_isd_value = max(0, home_price - 110000) if homestead else home_price
    
    annual_base_tax = home_price * city_base_rate
    annual_isd_tax = taxable_isd_value * isd_rate
    
    total_annual_tax = annual_base_tax + annual_isd_tax
    total_monthly_tax = total_annual_tax / 12
    
    # --- DISPLAY RESULTS ---
    st.markdown("---")
    st.subheader("Estimated Tax Breakdown")
    
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric(label="Estimated Monthly Escrow Impact", value=f"${total_monthly_tax:,.2f}")
    with metric_col2:
        st.metric(label="Total Annual Property Tax", value=f"${total_annual_tax:,.2f}")
        
    # Detailed collapse panel for transparency
    with st.expander("View Layered Details"):
        st.write(f"**Taxable School Value:** ${taxable_isd_value:,}")
        st.write(f"**City/County Base Tax ({city_base_rate*100:.4f}%):** ${annual_base_tax:,.2f}")
        st.write(f"**School District Tax ({isd_rate*100:.4f}%):** ${annual_isd_tax:,.2f}")
        st.write(f"**Combined Total Baseline Rate:** {(city_base_rate + isd_rate)*100:.3f}%")
