import pandas as pd
import plotly.express as px

def generate_crash_map(df, selected_period):
    # Extract start and end years from selected period
    start_year, end_year = map(int, selected_period.split('-'))

    # Filter data based on the selected period
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

    # Aggregate fatalities per country & year
    fatalities_by_country = filtered_df.groupby(['Year', 'Country'])['Total fatalities'].sum().reset_index()

    # Generate an animated choropleth map
    fig = px.choropleth(
        fatalities_by_country,
        locations="Country",
        locationmode="country names",
        color="Total fatalities",
        hover_name="Country",
        title=f"✈️ Animated Plane Crash Fatalities by Country ({selected_period})",
        animation_frame="Year",  # Enables animation
        color_continuous_scale="Reds"
    )

    # Increase plot size and optimize layout
    fig.update_layout(
        autosize=True,
        width=1000,
        height=600,
        margin=dict(l=20, r=20, t=50, b=20),
        transition={'duration': 500},  # Smooth transition
    )

    return fig  

def generate_flight_phase_sunburst(df):
    # Aggregate total fatalities by flight phase
    phase_data = df.groupby("Flight phase")["Total fatalities"].sum().reset_index()

    # Create Sunburst Chart
    fig = px.sunburst(
        phase_data,
        path=["Flight phase"],
        values="Total fatalities",
        title="🌞 Fatalities by Flight Phase",
        color="Total fatalities",
        color_continuous_scale="Reds"
    )
    # Adjust layout for better visualization
    return fig

def generate_airline_treemap(df):
    # Count crashes per airline and get top 10
    airline_crashes = df["Operator"].value_counts().reset_index()
    airline_crashes.columns = ["Airline", "Crashes"]
    airline_crashes = airline_crashes.head(10)  # Top 10 airlines

    # Create Treemap
    fig = px.treemap(
        airline_crashes,
        path=["Airline"],
        values="Crashes",
        title="✈️ Top 10 Airlines with Most Crashes",
        color="Crashes",
        color_continuous_scale="Reds"
    )

    return fig