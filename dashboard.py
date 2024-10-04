import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


hours_df = pd.read_csv('hour.csv')
days_df = pd.read_csv('day.csv')

hours_df['dteday'] = pd.to_datetime(hours_df['dteday'])
days_df['dteday'] = pd.to_datetime(days_df['dteday'])  

daily_avg_casual = hours_df.groupby('dteday')['casual'].mean()
daily_avg_registered = hours_df.groupby('dteday')['registered'].mean()

weekly_avg_casual = hours_df.resample('W', on='dteday')['casual'].mean()
weekly_avg_registered = hours_df.resample('W', on='dteday')['registered'].mean()


daily_avg_duration = pd.DataFrame({
    'avg_casual': daily_avg_casual,
    'avg_registered': daily_avg_registered
})

weekly_avg_duration = pd.DataFrame({
    'avg_casual': weekly_avg_casual,
    'avg_registered': weekly_avg_registered
})

days_df['month'] = days_df['dteday'].dt.month_name()
days_df['season'] = days_df['season'].replace({
    1: 'Spring', 
    2: 'Summer', 
    3: 'Fall', 
    4: 'Winter'
})

monthly_sharing = days_df.groupby('month')['cnt'].sum().reindex([
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'
])
seasonal_sharing = days_df.groupby('season')['cnt'].sum()

st.sidebar.title("Pengaturan Visualisasi")
view_option = st.sidebar.selectbox("Lihat Rata-rata Durasi Peminjaman:", ["Daily", "Weekly"])
visualization_option = st.sidebar.selectbox("Lihat Total Rental:", ["Month", "Season"])

st.title("Bike Sharing Dashboard")

def plot_duration(data, title):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['avg_casual'], label='Casual', color='blue', marker='o')
    plt.plot(data.index, data['avg_registered'], label='Registered', color='green', marker='o')
    plt.title(title)
    plt.ylabel("Duration (hours)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)

def plot_monthly_sharing(data, title):
    plt.figure(figsize=(10, 6))
    plt.bar(data.index, data.values, color='orange')
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel("Total Sharing")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

def plot_seasonal_sharing(data, title):
    plt.figure(figsize=(10, 6))
    plt.bar(data.index, data.values, color='purple')
    plt.title(title)
    plt.xlabel("Season")
    plt.ylabel("Total Sharing (Million)")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

if view_option == "Daily":
    st.subheader("Rata-rata Durasi Peminjaman per Hari")
    plot_duration(daily_avg_duration, "Daily Average Bike Sharing Duration  (Casual & Registered)")
else:
    st.subheader("Rata-rata Durasi Peminjaman per Minggu")
    plot_duration(weekly_avg_duration, "Weekly Average Bike Sharing Duration  (Casual & Registered)")

if visualization_option == "Month":
    st.subheader("Total Peminjaman Sepeda per Bulan")
    plot_monthly_sharing(monthly_sharing, "Total Bike Sharing per Month")
else:
    st.subheader("Total Peminjaman Sepeda per Musim")
    plot_seasonal_sharing(seasonal_sharing, "Total Bike Sharing per Season")

st.write("""
    **Catatan:**
    - Garis biru mewakili rata-rata durasi peminjaman oleh pengguna Casual.
    - Garis hijau mewakili rata-rata durasi peminjaman oleh pengguna Registered.
""")