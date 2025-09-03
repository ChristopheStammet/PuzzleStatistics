import streamlit as st
import pandas as pd
import plotly.express as px

# Load your CSV data
@st.cache_data
def load_data():
    df = pd.read_csv('solving_times.csv')
    # Convert all times to numeric (seconds), fill missing with NaN
    for level in ['level_3', 'level_6', 'level_9', 'level_12', 'level_15']:
        df[level] = pd.to_numeric(df[level], errors='coerce')
    return df

df = load_data()

st.title("Puzzle Solving Times Dashboard")

# Show raw data for transparency
st.write("Raw Data:", df)

# Plot average solving times per level
level_cols = ['level_3', 'level_6', 'level_9', 'level_12', 'level_15']
avg_times = df[level_cols].mean()

fig = px.line(
    x=[3, 6, 9, 12, 15],
    y=avg_times,
    labels={'x': 'Puzzle Pieces', 'y': 'Average Time (seconds)'},
    title='Average Solving Time per Puzzle Level'
)
st.plotly_chart(fig)

# Individual user times
fig2 = px.scatter(
    df.melt(id_vars='name', value_vars=level_cols),
    x='variable', y='value', color='name',
    labels={'variable': 'Level', 'value': 'Time (seconds)', 'name': 'User'},
    title='Individual Solving Times'
)
st.plotly_chart(fig2)

# Optional: Add a boxplot for time distributions
fig3 = px.box(
    df.melt(id_vars='name', value_vars=level_cols),
    x='variable', y='value',
    points="all",
    labels={'variable': 'Level', 'value': 'Time (seconds)'},
    title='Time Distributions by Level'
)
st.plotly_chart(fig3)

# Add leaderboard
leaderboard = df[['name'] + level_cols].set_index('name')
st.subheader("Leaderboard")
st.dataframe(leaderboard)
