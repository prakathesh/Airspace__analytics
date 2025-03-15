import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ✅ Set Streamlit Page Config (FIRST command in the script)
st.set_page_config(page_title="Airline Delay Dashboard", layout="wide")

# ✅ Load dataset
@st.cache_data
def load_data():
    file_path = "Airline_Delay_Cause.csv"  # Update path if needed
    df = pd.read_csv(file_path)
    return df

df = load_data()

# ✅ Replace infinite values and drop NaN
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# ✅ Convert 'year' column to integer
df["year"] = df["year"].astype(int)

# ✅ Dashboard Title
st.title("✈️ Airline Delay Analysis Dashboard")
st.markdown(
    '<p style="font-size:14px; background-color:#d2a679; padding:4px; display:inline-block; border-radius:5px;">'
    'Period: Aug 2013 - Aug 2023</p>',
    unsafe_allow_html=True
)

# ✅ Filters within Layout
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    years = sorted(df["year"].unique(), reverse=True)
    selected_year = st.selectbox("Select Year", ["All Years"] + years)

with filter_col2:
    selected_carrier = st.selectbox("Select Carrier", ["All"] + list(df["carrier_name"].unique()))

with filter_col3:
    selected_airport = st.selectbox("Select Airport", ["All"] + list(df["airport_name"].unique()))

# ✅ Apply Filters to Data
df_filtered = df.copy()
if selected_year != "All Years":
    df_filtered = df_filtered[df_filtered["year"] == selected_year]
if selected_carrier != "All":
    df_filtered = df_filtered[df_filtered["carrier_name"] == selected_carrier]
if selected_airport != "All":
    df_filtered = df_filtered[df_filtered["airport_name"] == selected_airport]

# ✅ KPI Metrics
st.markdown("### Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
with kpi_col1:
    total_delays = df_filtered["arr_delay"].sum()
    st.metric("Total Delayed Flights", f"{total_delays:,}")
with kpi_col2:
    total_cancelled_flights = df_filtered["arr_cancelled"].sum()
    st.metric("Total Flights Cancelled", f"{total_cancelled_flights:,}")  
with kpi_col3:
    num_airlines = df_filtered["carrier_name"].nunique()
    st.metric("Number of Airlines", num_airlines)

# ✅ Add a Divider
st.markdown("---")

# ✅ Improved Layout for Charts
chart_col1, chart_col2 = st.columns(2)

# ✅ Monthly Flight Delays

with chart_col1:
    st.subheader("📈 Monthly Flight Delays")
    with st.expander("🔍 Insights from the Line Chart"):
        st.markdown("""
        - 📌 *Trends Over Time: This chart helps you track monthly variations in flight delays. Spikes in certain months may indicate **seasonal travel surges* or *weather-related disruptions*.
        - ✈️ *Peak Delay Periods: Notice if delays **increase during holiday seasons* (e.g., Thanksgiving, Christmas, or summer vacations) when airline traffic is high.
        - 🌦️ *Impact of Weather: If specific months (e.g., winter or hurricane seasons) show high delays, **weather may be a key factor*.
        - 🏆 *Best vs. Worst Performing Months: Some months may consistently have fewer delays—analyzing these can help airlines **optimize operations*.
        """)
    if selected_year == "All Years":
        monthly_delays = df_filtered.groupby(["year", "month"])["arr_del15"].sum().reset_index()
        monthly_delays["date"] = pd.to_datetime(monthly_delays[["year", "month"]].assign(day=1))
        fig1 = px.line(
            monthly_delays, x="date", y="arr_del15",
            title="Monthly Flight Delays (All Years)",
            labels={"arr_del15": "Delayed Flights"},
            markers=True, height=500
        )
    else:
        monthly_delays = df_filtered.groupby("month")["arr_del15"].sum().reset_index().sort_values(by="month")
        fig1 = px.line(
            monthly_delays, x="month", y="arr_del15",
            title=f"Monthly Flight Delays - {selected_year}",
            labels={"arr_del15": "Delayed Flights", "month": "Month"},
            markers=True, height=500
        )
        fig1.update_xaxes(type="category", tickmode="linear")
    st.plotly_chart(fig1, use_container_width=True)

# ✅ Delay Breakdown by Reason (Interactive Pie Chart)
with chart_col2:
    st.subheader("⚪ Proportion of Delay")
    with st.expander("🔍 Insights from the Visualization"):
        st.markdown("""
    - Frequent Delays: The pie chart shows which delay causes (e.g., carrier, weather, or late aircraft delays) dominate across months. You may notice that "Late Aircraft Delay" or "Carrier Delay" often take up a large portion, indicating recurring issues in airline operations.
    
    - Peak Delay Months: By animating across months, you can observe which months consistently show higher delays. For example, winter months may have more weather-related delays, or holiday seasons may see an increase in carrier delays due to high traffic.
    
    - Operational Focus: If specific delay types dominate certain months, it can guide airlines to improve efficiency in those areas, whether it's better scheduling, handling weather disruptions, or reducing late aircraft incidents.
    """)

    # ✅ Delay cause columns
    delay_causes = ["carrier_delay", "weather_delay", "nas_delay", "security_delay", "late_aircraft_delay"]

    # ✅ Define labels for each delay cause
    delay_labels = {
        "carrier_delay": "Carrier Delay",
        "weather_delay": "Weather Delay",
        "nas_delay": "National Aviation System Delay",
        "security_delay": "Security Delay",
        "late_aircraft_delay": "Late Aircraft Delay"
    }

    # ✅ Aggregate Data for Pie Chart
    delay_sum = df_filtered[delay_causes].sum()

    # ✅ Handle case when no data is available
    if delay_sum.sum() == 0:
        st.warning(f"No delay data available for the selected filters.")
    else:
        fig_pie = px.pie(
            names=[delay_labels[col] for col in delay_sum.index],
            values=delay_sum.values,
            title="Proportion of Delay Causes",
            hole=0.3,  
            color_discrete_sequence=px.colors.sequential.Reds
        )

        st.plotly_chart(fig_pie, use_container_width=True)

# ✅ Download Button
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

csv = convert_df(df_filtered)
st.download_button("📥 Download Data", csv, "filtered_data.csv", "text/csv")

# ✅ Expander for Data Insights
with st.expander("🔍 See Data Insights"):
    st.write(df_filtered.describe())