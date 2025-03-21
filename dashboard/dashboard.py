import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

main_data = pd.read_csv("main_data.csv")

st.sidebar.title("Filter Data")
weekday_filter = st.sidebar.checkbox("Hanya Hari Kerja")
weekend_filter = st.sidebar.checkbox("Hanya Akhir Pekan")

if weekday_filter:
    main_data = main_data[main_data['weekday'] < 5]
elif weekend_filter:
    main_data = main_data[main_data['weekday'] >= 5]

st.title("Dashboard Analisis Peminjaman Sepeda")

st.subheader("Pola Peminjaman Sepeda Registered pada Hari Kerja Berdasarkan Kondisi Cuaca")
weekday_data = main_data[main_data['weekday'] < 5]
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dteday', y='registered', hue='weathersit', data=weekday_data, ax=ax)
plt.title('Pola Peminjaman Sepeda Registered pada Hari Kerja Berdasarkan Kondisi Cuaca')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Peminjaman Registered')
plt.legend(title='Kondisi Cuaca', loc='upper left')
st.pyplot(fig)

st.subheader("Rata-Rata Peminjaman Sepeda pada Jam Sibuk (Pagi & Sore)")
peak_hours_df = main_data[(main_data['hr'].between(7, 9)) | (main_data['hr'].between(17, 19))]
peak_hours_grouped = peak_hours_df.groupby(['weekday', 'hr'])['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='hr', y='cnt', hue='weekday', data=peak_hours_grouped, ax=ax)
plt.title('Rata-Rata Peminjaman Sepeda pada Jam Sibuk (Pagi & Sore)')
plt.xlabel('Jam')
plt.ylabel('Rata-rata Jumlah Peminjaman')
plt.xticks(rotation=0)
plt.legend(title='Hari', labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
st.pyplot(fig)

total_peminjaman = main_data['cnt'].sum()
st.markdown(f"**Jumlah Total Peminjaman:** {total_peminjaman}")

