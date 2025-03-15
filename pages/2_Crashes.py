import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import maps




def load_and_process_data(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)

    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Extract year from date
    df['Year'] = df['Date'].dt.year

    # Drop rows with missing years
    df = df.dropna(subset=['Year'])

    # Define 20-year intervals
    bins = list(range(int(df['Year'].min()), int(df['Year'].max()) + 20, 20))
    labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]

    # Create a new column for 20-year intervals
    df['Year_Group'] = pd.cut(df['Year'], bins=bins, labels=labels, right=False)

    return df, labels  # Return processed DataFrame and available year groups

def plot_fatalities_for_2_years(df, selected_period):
    # Get the numeric start and end years from selected period
    start_year, end_year = map(int, selected_period.split('-'))

    # Filter data within the selected period
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

    # Define 2-year intervals
    bins = list(range(start_year, end_year + 2, 2))
    labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]

    # Create a new column for 2-year intervals
    filtered_df['Year_2_Group'] = pd.cut(filtered_df['Year'], bins=bins, labels=labels, right=False)

    # Aggregate total fatalities per 2-year period
    fatalities_per_2_year = filtered_df.groupby('Year_2_Group')['Total fatalities'].sum().reset_index()

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create the bar plot
    sns.barplot(data=fatalities_per_2_year, x='Year_2_Group', y='Total fatalities', palette="Reds", ax=ax)

    # Add labels on top of bars
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height()):,}', 
                    (p.get_x() + p.get_width() / 2, p.get_height()), 
                    ha='center', va='bottom', fontsize=12, fontweight="bold")

    # Customize plot
    ax.set_title(f"Total Fatalities Every 2 Years ({selected_period})", fontsize=14, fontweight="bold")
    ax.set_xlabel("2-Year Interval", fontsize=12)
    ax.set_ylabel("Total Fatalities", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    return fig  # Return the figure object




st.title("Lets Dive deep into Plane Crashes")
st.write("Scroll down for more Visualizations")

@st.cache_data
def load_data():
    # Replace with the path to your dataset
    data = pd.read_csv('/Users/prakathesh/Downloads/AirSafe-Analytics-Delays-Crashes/Plane Crashes.csv')
    return data

df = load_data()

with st.expander("📜 View Dataset (Click to Expand)", expanded=False):
    st.dataframe(df)



df, available_year_groups = load_and_process_data('/Users/prakathesh/Downloads/AirSafe-Analytics-Delays-Crashes/Plane Crashes.csv')

# User selection of 20-year period

st.subheader("1. Fatalities over years")
with st.expander("📊 Insights on Aviation Fatalities Across All Periods", expanded=False):
    st.markdown("""
    - **Early Aviation (1918-1937):** Fatalities were low in the early years but surged in the 1930s due to increased commercial and military aviation.
    - **World War & Post-War Era (1938-1957):** Wartime aviation (WWII) caused a sharp rise in crashes, followed by technological improvements in the 1950s.
    - **Jet Age Expansion (1958-1977):** The introduction of jet aircraft led to more air travel, but safety regulations were still evolving, leading to significant accidents.
    - **Modernization & Safety Improvements (1978-1997):** Fatalities started to decline as strict aviation laws, better training, and improved aircraft technology were introduced.
    - **Present-Day Aviation (1998-Present):** The safest period in aviation history, with very few major crashes due to high safety standards, advanced technology, and better air traffic control systems.
    """)
selected_period = st.selectbox("Select a 20-Year Period:", available_year_groups)
# Generate and display the 2-year interval plot
fig = plot_fatalities_for_2_years(df, selected_period)
st.pyplot(fig)

#---- World Map Visualization ----
st.subheader("2.Crashes on different Countries")
with st.expander("🔍 Insights from the Visualization", expanded=False):
    st.markdown("""
    - **United States** had the highest number of crash fatalities, reflecting its early dominance in aviation and military operations.
    - **European countries** (**United Kingdom, France, Germany**) also saw notable fatalities due to military and commercial aviation growth.
    - **Russia and parts of Asia** experienced some crashes, likely linked to experimental aviation.
    - **Minimal fatalities in Africa, South America, and Australia** suggest limited aviation infrastructure during this period.
    """)
map_fig = maps.generate_crash_map(df, selected_period)
st.plotly_chart(map_fig,use_container_width=True)


st.subheader("3. Flight Risk & Airline Safety Visualizations")

# Create columns
col1, col2,col3 = st.columns([2.0,0.5, 2.25])

# Add spacing
st.markdown("<br>", unsafe_allow_html=True)
# Generate and display Fatalities by Flight Phase (Sunburst Chart)
with col1:
    st.markdown("3.1 Fatalities by Flight Phase")
    with st.expander("📊 Insights: Fatalities by Flight Phase", expanded=False):
        st.markdown("""
        - **Flight phase matters** – Most fatalities occur during the **cruise** phase, followed by **takeoff and landing**.
        - **Takeoff & Landing are high-risk** – Rapid speed changes, weather, and mechanical failures increase crash risks.
        - **Cruise phase crashes are deadliest** – Though rare, mid-air failures or controlled flight into terrain (CFIT) often have no survivors.
        """)
    fig1 = maps.generate_flight_phase_sunburst(df)
    st.plotly_chart(fig1, use_container_width=True)

# Add space between charts using the middle empty column
with col2:
    st.markdown("") 
# Generate and display Top 10 Airlines with Most Crashes (Treemap)
with col3:
    st.markdown("3.2 Top 10 Airlines with Most Crashes")
    with st.expander("✈️ Insights: Airlines with Most Crashes", expanded=False):
        st.markdown("""
        - **Military aviation has high crash numbers** – The **Royal Air Force & USAF** have the most recorded incidents.
        - **Older airlines have more crashes** – Longer operational history leads to more recorded crashes.
        - **High-traffic airlines tend to show up** – More flights mean more exposure to potential risks.
        """)
    fig2 = maps.generate_airline_treemap(df)
    st.plotly_chart(fig2, use_container_width=True)