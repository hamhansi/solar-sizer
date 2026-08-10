import streamlit as st
import math
st.set_page_config(
    page_title="Solar System Sizer",
    page_icon = "☀️",
    layout="centered",
)

st.title("☀️ Solar System Sizing calculator")
st.markdown("Calculate how many solar panels, battery capacity, and inverter size")

#Sidebar for inputs
st.sidebar.header("Your Inputs")
daily_kwh = st.sidebar.number_input(
    "Daily KWH",
    min_value = 0.5,
    value = 30.0,
    step = 0.5,
    help = "Check your electricity bill (monthly kwh /30)"
)

peak_sun_hours = st.sidebar.number_input(
    "Peak sun hours",
    min_value = 1.0,
    value = 4.5,
    step = 0.1,
    help = "Typical range: 3.5 - 6.5 depending on your location"
)

panel_wattage = st.sidebar.number_input(
    "Panel wattage (W)",
    min_value = 100,
    value = 400,
    step = 10
)

performance_ratio = st.sidebar.number_input(
    "Performance ratio",
    min_value = 0.60,
    max_value = 0.95,
    value = 0.80,
    step = 0.01,
    help = "Usually 0.75 - 0.85 (accounts for real - world losses)"
)

offset_percent = st.sidebar.number_input(
    "Desired energy coverage (%)",
    min_value = 10,
    max_value = 150,
    value = 100,
    step = 5
)

st.sidebar.markdown("---")
st.sidebar.subheader("Battery (optional)")

days_autonomy = st.sidebar.number_input(
    "Days of autonomy/ backup",
    min_value = 0.0,
    value = 0.0,
    step = 0.5,
    help = "set to 0 if you don't want a battery"
)

battery_dod = 0.80
battery_efficiency = 0.90

if days_autonomy > 0:
    battery_dod = st.sidebar.slider("Depth of Discharge (dod)", 0.40, 0.95, 0.80, 0.05)
    battery_efficiency = st.sidebar.slider("Battery efficiency", 0.70, 0.98, 0.90, 0.01)

inverter_margin = st.sidebar.slider("Inverter margin", 1.0, 1.5, 1.2, 0.05)


# Calculation
target_daily = daily_kwh * (offset_percent / 100)
array_kw = target_daily / (peak_sun_hours * performance_ratio)
num_panels = math.ceil((array_kw * 1000)/ panel_wattage)
actual_array_kw = (num_panels * panel_wattage) / 1000
estimated_production = actual_array_kw * peak_sun_hours * performance_ratio

battery_kwh = None
if days_autonomy > 0:
    battery_kwh = (daily_kwh * days_autonomy) / (battery_efficiency + battery_dod)

inverter_kw = actual_array_kw * inverter_margin

#Results
st.header("Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Recommended Array", f"{array_kw: .2f} kW")
    st.metric("Number of Panels", f"{num_panels} panels")

with col2:
    st.metric("Actual Array Size", f"{actual_array_kw: .2f} kW")
    st.metric("Estimated Daily production", f"{estimated_production: .2f} kWh")

with col3:
    st.metric("Inverter Size approx", f"{inverter_kw: .2f} KVA")
    if battery_kwh:
        st.metric("Battery capacity", f"{battery_kwh: .2f} kWh")
    else:
        st.metric("Battery", "None")

st.markdown("---")
st.info("""
**Notes**
- This is a first-order planning estimate.
- Always verify Peak Sun Hours with NREL PVWatts or local data.
- Check roof space, shading, local codes, and utility interconnection rules.
- For off-grid systems, size using the worst month of the year.
""")