import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
  
# Notes: run streamlit 'streamlit run .\dashboard\dashboard.py'

# Load data
@st.cache_data
def load_data():
    day_data = pd.read_csv('day.csv')
    
    # Data preprocessing
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])
    
    day_data.rename(columns={
        'dteday': 'dateday',
        'yr': 'year',
        'mnth': 'month',
        'cnt': 'count'
    }, inplace=True)
    

    day_data['season'] = day_data['season'].map({
        1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
    })
    day_data['season'] = day_data.season.astype('category')
    
    day_data['weekday'] = day_data['weekday'].map({
        0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
    })
    
    day_data['month'] = day_data['month'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    day_data['month'] = day_data.month.astype('category')
    
    day_data['weathersit'] = day_data['weathersit'].map({
        1: 'Clear/Partly Cloudy',
        2: 'Misty/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Severe Weather'
    })
    day_data['weathersit'] = day_data.weathersit.astype('category')
    
    return day_data

day_data = load_data()


st.title('Bike Sharing Data Analysis')

st.markdown("""
    <style>
    .justified-text {
        text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
page = st.sidebar.radio('Select Page', ['Purpose and Question', 'Season Usage', 'Weekday Usage', 'Monthly Distribution', 'Weather Impact', 'Conclusion'])


if page == 'Purpose and Question':
    st.header('Welcome to the Bike Sharing Data Analysis Dashboard!')
    st.markdown("""
<div style="text-align: justify">
  This dashboard provides a comprehensive visual exploration of bike sharing usage patterns across different seasons, weekdays, months, and weather conditions. 
  By examining the data from 2011 and 2012, you will gain insights into how external factors like seasonality, day of the week, and weather impact the number 
  of casual and registered bike users. Through provided charts, you can discover trends and fluctuations that influence bike-sharing demand, offering valuable 
  information for optimizing bike-sharing services and planning for future urban mobility.
                
<br><br>           
                
  The analysis focuses on answering four key questions:
  1. **How does bike sharing usage vary across seasons?**
  2. **How many registered and casual users utilize bike sharing during weekdays?**
  3. **How was the distribution of bike sharing usage per month in 2011 and 2012?**
  4. **Does weather affect bike sharing usage each month?**            
<br>           
  At the end of the analysis, a conclusion is provided, summarizing the key findings from these visualizations and offering insights that could guide decision-making 
  in the bike-sharing industry.
</div>
""", unsafe_allow_html=True)

# For question 1
if page == 'Season Usage':
    st.header('Bike Sharing Usage by Season')
    st.subheader('How does bike sharing usage vary across seasons?')
    

    # Calculate bike sharing usage by season
    season_usage = day_data.groupby('season')['count'].sum()

    # Colors for pie chart
    colors = sns.color_palette('coolwarm', len(season_usage))

    # Create pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(season_usage, labels=season_usage.index, colors=colors, 
                                      autopct='%1.1f%%', startangle=90, 
                                      wedgeprops={'edgecolor': 'black'})
    
    # Create Donut pie chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='#FF9999')
    fig.gca().add_artist(centre_circle)

    # Add title and background color
    plt.title('Bike Sharing Usage by Season', fontsize=18, fontweight='bold', color='black')
    plt.gcf().set_facecolor('#FF9999')
    
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify">
    <strong>Explanation of bike sharing usage by season:</strong>
<br>
    The donut pie chart above shows the relationship between the number of bike sharing users each season. 
    There are 4 seasons, namely Winter, Summer, Spring, and Fall. It can be seen that the number of bike sharing users is highest in autumn, followed by summer, winter, and spring.
</div>
""", unsafe_allow_html=True)

# For question 2
elif page == 'Weekday Usage':
    st.header('Registered and Casual Users During Weekdays')
    st.subheader('How many registered and casual users utilize bike sharing during weekdays?')
    
    # Calculate casual and registered usage by weekday
    weekday_mapping = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    day_data['weekday_name'] = day_data['weekday'].map(weekday_mapping)

    weekday_usage = day_data.groupby('weekday')[['casual', 'registered']].sum()

    weekday_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekday_usage = weekday_usage.reindex(weekday_order)

    # Create bar chart for casual and registered users
    fig, ax = plt.subplots(figsize=(10, 6))
    weekday_usage.plot(kind='bar', stacked=True, color=['#FF9999', '#66B2FF'], ax=ax)

    # Add title, labels, and background
    plt.title('Registered and Casual Users by Weekdays', fontsize=15, fontweight='bold', color='black')
    plt.xlabel('Weekday', fontsize=12, color='black')
    plt.ylabel('Number of Users', fontsize=12, color='black')
    plt.gcf().set_facecolor('#e6f2ff')

    # Grid and x-axis label rotation
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify">
    <strong>Explanation of registered and casual users by day of the week:</strong>
<br>
    The bar chart above shows the relationship between the number of registered and unregistered (casual) users during weekdays. 
    The following statements were obtained:
    <div>
        <ul>
            <li>The highest number of bike sharing users is on Friday (Fri) and the lowest is on Sunday (Sun).</li>
            <li>The highest number of unregistered users is on Saturday (Sat) and the lowest is on Tuesday (Tue) and Wednesday (Wed).</li>
            <li>The highest number of registered users is on Thursday (Thu).</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# For question 3
elif page == 'Monthly Distribution':
    st.header('Monthly Bike Sharing Usage Distribution (2011-2012)')
    st.subheader('How was the distribution of bike sharing usage per month in 2011 and 2012?')
    
    # Monthly distribution of bike sharing usage for 2011 and 2012 
    monthly_data = day_data.groupby(['year', 'month'])['count'].sum().unstack(level=0)
    monthly_data.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, ax = plt.subplots(figsize=(14, 7))
    monthly_data.plot(kind='line', ax=ax, marker='o', linewidth=2, markersize=8)

    plt.title('Monthly Distribution of Bike Sharing Usage in 2011 and 2012', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Users', fontsize=12)
    plt.legend(['2011', '2012'], fontsize=10)

    # Add colorful background
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    plt.imshow(gradient, extent=[ax.get_xlim()[0], ax.get_xlim()[1], ax.get_ylim()[0], ax.get_ylim()[1]],
               aspect='auto', zorder=0, alpha=0.2, cmap='coolwarm')

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify">
        <strong>Explanation of monthly bike sharing usage:</strong>
<br>
    The line chart above shows the relationship between the number of bike sharing users and months for 2 years, 
    namely 2011 and 2012. The following statements were obtained:
    <div>
        <ul>
            <li>The number of bike sharing users increased from the previous year. However, the increase 
            and decrease in the number of bike sharing users in both years were almost the same.</li>
            <li>The lowest number of users in 2011 and 2012 was in May.</li>
            <li>The highest number of users in 2011 was in July. While in 2012, the peak was in December.</li>
            <li>Bike sharing enthusiasts experienced a decline in certain months, including March, April, May, August, and October.</li>
        </ul>
    <div>
</div>
""", unsafe_allow_html=True)

# For question 4
elif page == 'Weather Impact':
    st.header('Weather Impact on Bike Sharing by Month')
    st.subheader('Does weather affect bike sharing usage each month?')
    
    # Weather impact on bike sharing each month 
    weather_monthly = day_data.groupby(['month', 'weathersit'])['count'].mean().unstack()
    weather_monthly.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, ax = plt.subplots(figsize=(16, 8))
    weather_monthly.plot(kind='bar', ax=ax, width=0.8)

    plt.title('Weather Impact on Bike Sharing Usage by Month', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Average Number of Users', fontsize=12)
    plt.legend(['Clear/Partly Cloudy', 'Misty/Cloudy', 'Light Snow/Rain', 'Severe Weather'], fontsize=10, title='Weather Condition')
    plt.xticks(rotation=45)

    # Add gradient background
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    plt.imshow(gradient, extent=[ax.get_xlim()[0], ax.get_xlim()[1], ax.get_ylim()[0], ax.get_ylim()[1]],
               aspect='auto', zorder=0, alpha=0.2, cmap='Wistia')

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
<div style="text-align: justify">
    <strong>Explanation of the impact of weather on bike usage:</strong>
<br>
    The bar chart above shows the relationship between the average number of users each month based on the weather. 
    Bike users rent more during sunny/partly cloudy weather, followed by snow/light rain, and finally foggy/cloudy 
    weather. However, bike users prefer snow/light rain in June. Meanwhile, in February, July, and September, there are very few (almost no) bike renters during foggy/cloudy weather.
</div>
""", unsafe_allow_html=True)

# For conclusion
if page == 'Conclusion':
    st.header('Conclusion')
    st.subheader('Conclusion to Understanding User Behavior')
    st.markdown("""
<div style="text-align: justify">
    This section introduces the conclusions and provides context for the insights gathered from the analysis. 
    It emphasizes the importance of understanding user patterns.
<br><br>
    <strong>How does bike sharing usage vary across seasons?</strong>
<br>
    Fall has the highest percentage because the air temperature is cooler, not too cold or hot. Then, in summer, 
    many people are on holiday and the weather is conducive to outdoor activities, so the percentage is the 
    second highest after fall. On the contrary, in winter and spring, the air temperature is cold and unstable, 
    less conducive to outdoor activities, thus affecting the interest of bicycle renters. However, the percentage 
    of winter should be the lowest because the cold air and snow make the roads less safe for users. But, 
    the percentage of spring is the smallest, perhaps because foggy/cloudy weather reduces the interest of bike 
    sharing renters and is dangerous due to poor visibility (obstructed by fog).
<br><br>
    <strong>How many registered and casual users utilize bike sharing during weekdays?</strong>
<br>
    On weekdays, registered users rent more on Thursday and peak on Friday for all users. This can be caused by 
    their routine activities such as school, work, and then their interest in cycling towards the weekend. Then, 
    casual users are most on Saturday, indicating that they use their free time for cycling and recreation.
<br><br>
    <strong>How was the distribution of bike sharing usage per month in 2011 and 2012?</strong>
<br>
    Bicycle usage increased from 2011 to 2012 and had almost similar fluctuations. The decrease in usage in 
    several months (March, April, May, August, and October) may be related to weather changes or changing seasons 
    and vice versa. The different peaks in usage were caused by several less favorable conditions.
<br><br>
    <strong>Does weather affect bike sharing usage each month?</strong>   
<br>
    Weather significantly affects the interest of bike renters. Clear or partly cloudy weather is the favorite 
    time for renters to cycle because the safe and comfortable conditions are very supportive of outdoor activities. 
    Then, in June, renters prefer light snow/rain weather. This could be due to the cooler air temperature than usual 
    during summer. Bike renters tend to avoid foggy/cloudy weather because poor visibility and unsafe roads can endanger users.
<br><br>
    In summary, these insights emphasize the importance of considering seasonal and weather-related factors when planning and 
    promoting bike sharing services. Continuous monitoring and adapting strategies based on user behavior can lead to improved 
    service and user satisfaction. 
</div>
""", unsafe_allow_html=True)