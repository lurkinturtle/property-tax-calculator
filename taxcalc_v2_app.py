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

# --- USER INPUTS ---
st.subheader("Calculator Inputs")

# 1. Initialize session state if it doesn't exist yet
if "price" not in st.session_state:
    st.session_state.price = 300000

# 2. Define callback functions to sync the widgets
def update_from_slider():
    st.session_state.price = st.session_state.slider_price

def update_from_input():
    # Keep typed input within the logical boundaries of the slider
    clamped_val = min(max(st.session_state.input_price, 150000), 750000)
    st.session_state.price = clamped_val

# 3. Render the widgets side-by-side or stacked
# We pull the shared data from st.session_state.price
home_price_input = st.number_input(
    "Type Exact Property Price ($)",
    min_value=150000,
    max_value=750000,
    value=st.session_state.price,
    step=100,
    key="input_price",
    on_change=update_from_input
)

home_price_slider = st.slider(
    "Or Drag to Adjust Price", 
    min_value=150000, 
    max_value=750000, 
    value=st.session_state.price, 
    step=100,
    format="$%d",
    key="slider_price",
    on_change=update_from_slider
)

# 4. Use the consolidated state value for all tax math below
home_price = st.session_state.price

# Hyper-precise slider down to $100 increments
home_price = st.slider(
    "Property Purchase Price ($)", 
    min_value=150000, 
    max_value=750000, 
    value=300000, 
    step=100,
    format="$%d"
)

# Side-by-side dropdown selectors
col1, col2 = st.columns(2)
with col1:
    selected_city = st.selectbox("Location / City Limits", list(base_rates.keys()), index=0)
with col2:
    # Intentionally separate to handle Temple's multi-ISD addresses smoothly
    selected_isd = st.selectbox("School District (ISD)", list(isd_rates.keys()), index=0)

homestead = st.toggle("Apply Texas Homestead Exemption ($110,000 School Tax Discount)", value=True)

# --- MATH LOGIC ---
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