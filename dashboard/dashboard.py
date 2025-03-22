import streamlit as st
import pandas as pd
import urllib.request
import matplotlib.pyplot as plt
import seaborn as sns
import os

github_url = "https://raw.githubusercontent.com/DickySaragih/Submission/main/dashboard/main_data.csv"
file_path = "main_data.csv"

if not os.path.exists(file_path):
    urllib.request.urlretrieve(github_url, file_path)
    print("File berhasil diunduh!")
else:
    print("File sudah ada.")

df = pd.read_csv(file_path)

main_data = pd.read_csv("main_data.csv")

st.sidebar.title("Filter Data")
weekday_filter = st.sidebar.checkbox("Hanya Hari Kerja")
weekend_filter = st.sidebar.checkbox("Hanya Akhir Pekan")
weather_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca", main_data['weathersit'].unique())

if weekday_filter:
    main_data = main_data[main_data['weekday'] < 5]
elif weekend_filter:
    main_data = main_data[main_data['weekday'] >= 5]

if weather_filter:
    main_data = main_data[main_data['weathersit'].isin(weather_filter)]

st.title("Dashboard Analisis Peminjaman Sepeda")

st.subheader("Ringkasan Data")
st.write(main_data.describe())

st.subheader("Pola Peminjaman Sepeda Registered Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dteday', y='registered', hue='weathersit', data=main_data, ax=ax)
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Peminjaman Registered')
plt.title('Pola Peminjaman Sepeda Registered Berdasarkan Kondisi Cuaca')
st.pyplot(fig)

st.subheader("Rata-Rata Peminjaman Sepeda pada Jam Sibuk (Pagi & Sore)")
peak_hours_df = main_data[(main_data['hr'].between(7, 9)) | (main_data['hr'].between(17, 19))]
peak_hours_grouped = peak_hours_df.groupby(['weekday', 'hr'])['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='hr', y='cnt', hue='weekday', data=peak_hours_grouped, ax=ax)
plt.xlabel('Jam')
plt.ylabel('Rata-rata Jumlah Peminjaman')
plt.title('Rata-Rata Peminjaman Sepeda pada Jam Sibuk')
st.pyplot(fig)

total_peminjaman = main_data['cnt'].sum()
st.markdown(f"**Jumlah Total Peminjaman:** {total_peminjaman}")
