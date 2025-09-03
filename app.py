import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

level_cols = ['level_3', 'level_6', 'level_9', 'level_12', 'level_15']

# Prepare melted dataframe for individual data points
melted = df.melt(id_vars='name', value_vars=level_cols,
                  var_name='level', value_name='time')
level_map = {'level_3': 3, 'level_6': 6, 'level_9': 9, 'level_12': 12, 'level_15': 15}
melted['pieces'] = melted['level'].map(level_map)

# Calculate average times
avg_times = melted.groupby('pieces')['time'].mean().reset_index()

# Create combined figure
fig = go.Figure()

# Add scatter plot for individual times - no legend
fig.add_trace(go.Scatter(
    x=melted['pieces'],
    y=melted['time'],
    mode='markers',
    marker=dict(color='rgba(0, 100, 200, 0.5)', size=8),
    name='Individual Times',
    showlegend=False
))

# Add line plot for average times
fig.add_trace(go.Scatter(
    x=avg_times['pieces'],
    y=avg_times['time'],
    mode='lines+markers',
    line=dict(color='red', width=3),
    marker=dict(size=10),
    name='Average Time'
))

fig.update_layout(
    title='Puzzle Solving Times per Level',
    xaxis_title='Number of Pieces',
    yaxis_title='Time (seconds)',
    xaxis=dict(tickmode='array', tickvals=list(level_map.values())),
    template='plotly_white'
)

st.plotly_chart(fig)

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
