import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

pwd = os.getcwd()  

# Load data
@st.cache_data
def load_data():
    print(os.getcwd())
    day_data = pd.read_csv('day.csv')
    hour_data = pd.read_csv('hour.csv')
    
    # Data preprocessing
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])
    hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
    
    day_data.rename(columns={
        'dteday': 'dateday',
        'yr': 'year',
        'mnth': 'month',
        'cnt': 'count'
    }, inplace=True)
    
    hour_data.rename(columns={
        'dteday': 'dateday',
        'yr': 'year',
        'mnth': 'month',
        'cnt': 'count',
        'hr': 'hour'
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
    
    return day_data, hour_data

day_data, hour_data = load_data()

st.title('Bike Sharing Data Analysis')

# Sidebar navigation
page = st.sidebar.radio('Select Page', ['Season Usage', 'Weekday Usage', 'Monthly Distribution', 'Weather Impact'])

if page == 'Season Usage':
    st.header('Penggunaan Bike Sharing Setiap Musim')
    
    season_usage = day_data.groupby('season')['count'].sum()
    colors = sns.color_palette('coolwarm', len(season_usage))
    
    fig, ax = plt.subplots(figsize=(10, 10))
    wedges, texts, autotexts = ax.pie(season_usage, labels=season_usage.index, colors=colors, 
                                      autopct='%1.1f%%', startangle=90, 
                                      wedgeprops={'edgecolor': 'black'})
    
    # Create donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    
    plt.title('Penggunaan Bike Sharing Setiap Musim', fontsize=16, color='navy')
    plt.gcf().set_facecolor('#f7f7f7')
    
    st.pyplot(fig)

elif page == 'Weekday Usage':
    st.header('Pengguna Terdaftar dan Tidak Terdaftar Saat Weekday')
    
    weekday_mapping = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    day_data['weekday_name'] = day_data['weekday'].map(weekday_mapping)
    weekday_usage = day_data.groupby('weekday')[['casual', 'registered']].sum()
    weekday_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekday_usage = weekday_usage.reindex(weekday_order)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    weekday_usage.plot(kind='bar', stacked=True, color=['#FF9999', '#66B2FF'], ax=ax)
    
    plt.title('Pengguna Terdaftar dan Tidak Terdaftar Saat Weekday', fontsize=16, color='navy')
    plt.xlabel('Weekday', fontsize=12, color='darkblue')
    plt.ylabel('Jumlah Pengguna', fontsize=12, color='darkblue')
    plt.gcf().set_facecolor('#e6f2ff')
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    st.pyplot(fig)

elif page == 'Monthly Distribution':
    st.header('Distribusi Penggunaan Bike Sharing per Bulan (2011-2012)')
    
    monthly_data = day_data.groupby(['year', 'month'])['count'].sum().unstack(level=0)
    monthly_data.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig, ax = plt.subplots(figsize=(14, 7))
    monthly_data.plot(kind='line', ax=ax, marker='o', linewidth=2, markersize=8)
    
    plt.title('Distribusi Penggunaan Bike Sharing per Bulan (2011-2012)', fontsize=16, fontweight='bold')
    plt.xlabel('Bulan', fontsize=12)
    plt.ylabel('Jumlah Pengguna', fontsize=12)
    plt.legend(['2011', '2012'], fontsize=10)
    
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    plt.imshow(gradient, extent=[ax.get_xlim()[0], ax.get_xlim()[1], ax.get_ylim()[0], ax.get_ylim()[1]],
               aspect='auto', zorder=0, alpha=0.2, cmap='coolwarm')
    
    plt.tight_layout()
    st.pyplot(fig)

elif page == 'Weather Impact':
    st.header('Pengaruh Cuaca terhadap Peminjaman Bike Sharing per Bulan')
    
    weather_monthly = day_data.groupby(['month', 'weathersit'])['count'].mean().unstack()
    weather_monthly.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig, ax = plt.subplots(figsize=(16, 8))
    weather_monthly.plot(kind='bar', ax=ax, width=0.8)
    
    plt.title('Pengaruh Cuaca terhadap Peminjaman Bike Sharing per Bulan', fontsize=16, fontweight='bold')
    plt.xlabel('Bulan', fontsize=12)
    plt.ylabel('Rata-rata Jumlah Pengguna', fontsize=12)
    plt.legend(['Cerah/Berawan Sebagian', 'Berkabut/Berawan', 'Salju/Hujan Ringan', 'Hujan Lebat'], 
               fontsize=10, title='Kondisi Cuaca')
    plt.xticks(rotation=45)
    
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    plt.imshow(gradient, extent=[ax.get_xlim()[0], ax.get_xlim()[1], ax.get_ylim()[0], ax.get_ylim()[1]],
               aspect='auto', zorder=0, alpha=0.2, cmap='rainbow')
    
    plt.tight_layout()
    st.pyplot(fig)