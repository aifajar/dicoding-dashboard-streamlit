import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("main_data.csv")

min_date = df["dteday"].min()
max_date = df["dteday"].max()
 
with st.sidebar:

    st.image("bicycle_logo.png")
    
    start_date, end_date = st.date_input(
        label='Date Interval',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date))]

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Bike Sharing Overview')

col1, col2 = st.columns(2)

with col1:
    total_rents = main_df['cnt'].sum()
    st.metric("Total rents", value=total_rents)
    mean_rents_by_casual = round(main_df['casual'].mean(), 2)
    st.metric("Average rents by casual users", value=mean_rents_by_casual)

with col2:
    mean_rents = round(main_df['cnt'].mean(), 2)
    st.metric("Average rents", value=mean_rents)
    mean_rents_by_registered = round(main_df['registered'].mean(), 2)
    st.metric("Average rents by registered users", value=mean_rents_by_registered)

daily_avg = main_df.groupby('dteday')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    daily_avg['dteday'], 
    daily_avg['cnt'], 
    marker='o', 
    linestyle='-', 
    color='blue'
)

ax.set_xlabel('Date')
ax.set_ylabel('Average Daily Count')
ax.set_title('Daily Average Bike Rentals')

st.pyplot(fig)

st.subheader('Average Rents for Casual and Registered Users by Some Factor')

tab1, tab2, tab3, tab4 = st.tabs(["Weathersit", "Season", "Status Day", "Week Day"])

def plot_stacked_avg(group_factor, title):
    avg_counts = main_df.groupby(group_factor)[['casual', 'registered']].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(avg_counts[group_factor], avg_counts['casual'], label='Casual', color='skyblue')
    ax.bar(avg_counts[group_factor], avg_counts['registered'],
           bottom=avg_counts['casual'], label='Registered', color='salmon')

    ax.set_title(title)
    ax.set_xlabel(group_factor.capitalize())
    ax.set_ylabel('Average Count')
    ax.legend(title='User Type')

    st.pyplot(fig)

with tab1:
    plot_stacked_avg(
        group_factor='weathersit',
        title='Average Casual and Registered Counts by Weather Situation'
    )

with tab2:
    plot_stacked_avg(
        group_factor='season',
        title='Average Casual and Registered Counts by Season'
    )

with tab3:
    plot_stacked_avg(
        group_factor='workingday',
        title='Average Casual and Registered Counts by Working Day Status'
    )

with tab4:
    plot_stacked_avg(
        group_factor='weekday',
        title='Average Casual and Registered Counts by Week Day'
    )

st.subheader('Average Rents based on Hour (Holiday and Workingday)')

hourly_avg = main_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(
    data=hourly_avg,
    x='hr', y='cnt', hue='workingday',
    ax=ax,
    palette='Set2'
)

ax.set_title('Average Count by Hour and Working Day Status')
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Average Count')
ax.legend(title='Working Day')

st.pyplot(fig)
with st.expander("See explanation"):
    st.write(
        """There is a different pattern of bicycle rentals during certain hours on working
        days and holidays. On holidays, the average number of bicycle rentals from midnight
        to 4 AM and from 10 AM to 4 PM is higher compared to working days. On working days,
        the average number of bicycle rentals is higher between 5 AM and 9 AM and from 5 PM
        to 11 PM. This makes sense because these times typically coincide with commuting hours,
        so bicycle rentals during these periods are needed to support users’ work activities. 
        Meanwhile, on holidays, bicycles are usually rented for recreational purposes, which can
        be done during the daytime or in the evening.
        """
    )

st.caption('Copyright (C) Ahmad I. Fajar. 2025')