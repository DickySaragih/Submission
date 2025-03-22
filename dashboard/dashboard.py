import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
main_data = pd.read_csv("main_data.csv")

# Sidebar filters
st.sidebar.title("Filter Data")
weekday_filter = st.sidebar.checkbox("Hanya Hari Kerja")
weekend_filter = st.sidebar.checkbox("Hanya Akhir Pekan")
weather_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca", main_data['weathersit'].unique())

# Apply filters
if weekday_filter:
    main_data = main_data[main_data['weekday'] < 5]
elif weekend_filter:
    main_data = main_data[main_data['weekday'] >= 5]

if weather_filter:
    main_data = main_data[main_data['weathersit'].isin(weather_filter)]

# Title
st.title("Dashboard Analisis Peminjaman Sepeda")

# Data Overview
st.subheader("Ringkasan Data")
st.write(main_data.describe())

# Interactive Line Chart
st.subheader("Pola Peminjaman Sepeda Registered Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dteday', y='registered', hue='weathersit', data=main_data, ax=ax)
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Peminjaman Registered')
plt.title('Pola Peminjaman Sepeda Registered Berdasarkan Kondisi Cuaca')
st.pyplot(fig)

# Interactive Bar Chart
st.subheader("Rata-Rata Peminjaman Sepeda pada Jam Sibuk (Pagi & Sore)")
peak_hours_df = main_data[(main_data['hr'].between(7, 9)) | (main_data['hr'].between(17, 19))]
peak_hours_grouped = peak_hours_df.groupby(['weekday', 'hr'])['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='hr', y='cnt', hue='weekday', data=peak_hours_grouped, ax=ax)
plt.xlabel('Jam')
plt.ylabel('Rata-rata Jumlah Peminjaman')
plt.title('Rata-Rata Peminjaman Sepeda pada Jam Sibuk')
st.pyplot(fig)

# Show total rentals
total_peminjaman = main_data['cnt'].sum()
st.markdown(f"**Jumlah Total Peminjaman:** {total_peminjaman}")
