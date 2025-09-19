

import streamlit as st
import time
import base64
import pandas as pd
import random

    
def show_gif_with_text(gif_path, display_time=3):
    """
    Displays a GIF animation along with dynamic text before loading the main content.
    """
    # Read and encode the GIF file
    with open(gif_path, "rb") as file:
        gif_bytes = file.read()
    encoded_gif = base64.b64encode(gif_bytes).decode("utf-8")

    # List of dynamic welcome messages
    messages = [
        "Are you ready to Take OFF? ✈️",
        "Fasten your seatbelts! 🚀",
        "Welcome aboard! Let's explore aviation history! 🛫",
        "Buckle up! You're about to navigate flight data! 🎯",
    ]
    selected_message = random.choice(messages)  # Random message selection

    # Create a placeholder
    placeholder = st.empty()

    # Render the GIF and text
    with placeholder.container():
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/gif;base64,{encoded_gif}" alt="loading gif" width="300">
                <h2 style='text-align: center; color: #ff4b4b;'>{selected_message}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Wait for the specified time before clearing the placeholder
    time.sleep(display_time)
    placeholder.empty()

# Show the animated loading screen
show_gif_with_text("planeTransparent.gif", display_time=3)

# Cache dataset loading
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

# Load dataset
df1 = load_data('Plane Crashes.csv')

# 🎯 Main App Content
st.title("🛫 Buckle up to Navigate!!")
st.write("📊 While you're here, why not take a look at the dataset?")

# Brief Description
st.markdown("""
### ✈️ About This Project
This interactive **Streamlit dashboard** provides insights into **aviation safety, flight delays, and crash statistics**.
Users can navigate through different sections to analyze trends in **delays, crashes, and airline safety**.

🔹 **Features:**
- 📊 **Visualizations** of crash data, delays, and airline performance.
- 🌎 **Interactive world maps** for geographical analysis.
- ⏳ **Time-based trends** to identify improvements in aviation safety.
- 📌 **User-friendly navigation** with a sidebar.

**Navigate using the sidebar to explore different sections!**
""")

# Group Information with LinkedIn Links
st.markdown("### 👨‍💻 Our Team")
st.markdown("""
- [**Mugilan Thiyagarajan**](https://www.linkedin.com/in/mugilan-t-598a2b208/)  
- [**Prakathesh KS**](http://www.linkedin.com/in/prakathesh-k-s-5a43a5183)    
""", unsafe_allow_html=True)

# GitHub Link
st.markdown("""
### 🔗 Project GitHub Repository  
Click [here](https://github.com/prakathesh/Airspace__analytics) to view the code and contribute!
""")
