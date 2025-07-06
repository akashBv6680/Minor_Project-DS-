import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np  # For generating sample data
import warnings

# Suppress warnings that might clutter the Streamlit output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

st.set_page_config(
    page_title="My Data Story",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📖 Telling a Story with Data")

st.markdown("""
Welcome to this interactive data story! We'll explore a hypothetical dataset about customer engagement over time.
Our goal is to understand trends and identify key periods.
""")

st.header("Chapter 1: The Initial Trend")

st.markdown("""
Let's start by looking at the overall customer engagement. We've recorded the daily engagement score for a period.
""")

# --- Generate Sample Data ---
# For a real app, you'd load from a file using st.file_uploader
if 'data_story_df' not in st.session_state:
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    engagement = np.random.normal(loc=50, scale=10, size=100).cumsum() + 200
    st.session_state.data_story_df = pd.DataFrame({'Date': dates, 'Engagement': engagement})
    st.session_state.data_story_df['Day_of_Week'] = st.session_state.data_story_df['Date'].dt.day_name()
    st.session_state.data_story_df['Month'] = st.session_state.data_story_df['Date'].dt.month_name()

df = st.session_state.data_story_df

st.write("### Daily Engagement Over Time")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(x='Date', y='Engagement', data=df, ax=ax1)
ax1.set_title("Customer Engagement Trend")
ax1.set_xlabel("Date")
ax1.set_ylabel("Engagement Score")
st.pyplot(fig1)
plt.close(fig1)

st.markdown("""
From this initial view, we can see a general upward trend, but there are some fluctuations.
Let's dive deeper into specific periods or aspects.
""")

st.header("Chapter 2: Uncovering Weekly Patterns")

st.markdown("Is there a pattern based on the day of the week? Let's check the average engagement by day.")

show_weekly_pattern = st.checkbox("Show Average Engagement by Day of Week")

if show_weekly_pattern:
    weekly_avg = df.groupby('Day_of_Week')['Engagement'].mean().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    st.write("### Average Engagement by Day of Week")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(x=weekly_avg.index, y=weekly_avg.values, ax=ax2, palette='viridis')
    ax2.set_title("Average Engagement by Day of Week")
    ax2.set_xlabel("Day of Week")
    ax2.set_ylabel("Average Engagement Score")
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)
    plt.close(fig2)

    st.markdown("""
    **Insight:** It looks like engagement tends to be higher on weekdays and slightly lower on weekends. This could inform our content scheduling!
    """)

st.header("Chapter 3: Focusing on a Key Event")

st.markdown("""
Imagine there was a major marketing campaign or product launch around **February 2024**.
Let's see how engagement changed around that time.
""")

# Use a slider to select a date range
min_date = df['Date'].min().to_pydatetime()
max_date = df['Date'].max().to_pydatetime()

selected_date_range = st.slider(
    "Select Date Range to Zoom In:",
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

start_zoom_date, end_zoom_date = selected_date_range

zoomed_df = df[(df['Date'] >= start_zoom_date) & (df['Date'] <= end_zoom_date)]

if not zoomed_df.empty:
    st.write(f"### Engagement from {start_zoom_date.strftime('%Y-%m-%d')} to {end_zoom_date.strftime('%Y-%m-%d')}")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='Date', y='Engagement', data=zoomed_df, ax=ax3)
    ax3.set_title(f"Customer Engagement ({start_zoom_date.strftime('%b %d')} - {end_zoom_date.strftime('%b %d')})")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Engagement Score")
    st.pyplot(fig3)
    plt.close(fig3)

    st.markdown("""
    **Observation:** By zooming into specific periods, we can observe the immediate impact of events.
    Notice any spikes or dips around your selected range?
    """)
else:
    st.info("No data available for the selected date range. Please adjust the slider.")

st.header("Conclusion: What We've Learned")
st.markdown("""
Through this interactive story, we've:
* Identified the overall trend of customer engagement.
* Discovered a recurring weekly pattern.
* Gained the ability to zoom into specific events to see their immediate impact.

This approach allows stakeholders to explore the data at their own pace and understand the narrative directly.
""")

# Example of an image
st.image("https://images.unsplash.com/photo-1549057446-948f219fcd83", caption="Data Storytelling in Action",
         use_column_width=True)

st.markdown("---")
st.markdown("Thank you for exploring this data story!")