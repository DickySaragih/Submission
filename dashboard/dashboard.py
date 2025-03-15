import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the dataset
try:
    main_data = pd.read_csv('main_data.csv')
except FileNotFoundError:
    st.error("File 'main_data.csv' tidak ditemukan. Pastikan file tersebut ada di direktori yang sama dengan skrip ini.")
    st.stop()

# Judul Aplikasi Streamlit
st.title('Dashboard Analisis Data Peminjaman Sepeda')

# Sidebar untuk filter
st.sidebar.header('Filter Data')

# Filter by day_type
day_type_filter = st.sidebar.multiselect(
    "Pilih Tipe Hari",
    options=main_data['day_type'].unique(),
    default=main_data['day_type'].unique()
)

# Filter by weathersit
weathersit_filter = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=main_data['weathersit'].unique(),
    default=main_data['weathersit'].unique()
)

# Filter by hour
hour_filter = st.sidebar.slider(
    "Pilih Rentang Jam",
    min_value=int(main_data['hr'].min()),
    max_value=int(main_data['hr'].max()),
    value=(int(main_data['hr'].min()), int(main_data['hr'].max()))
)

# Filter by windspeed
windspeed_filter = st.sidebar.slider(
    "Pilih Rentang Kecepatan Angin",
    min_value=float(main_data['windspeed'].min()),
    max_value=float(main_data['windspeed'].max()),
    value=(float(main_data['windspeed'].min()), float(main_data['windspeed'].max()))
)

# Apply filters
filtered_data = main_data[
    (main_data['day_type'].isin(day_type_filter)) &
    (main_data['weathersit'].isin(weathersit_filter)) &
    (main_data['hr'].between(hour_filter[0], hour_filter[1])) &
    (main_data['windspeed'].between(windspeed_filter[0], windspeed_filter[1]))
]

# Menampilkan informasi umum tentang data
st.subheader('Informasi Umum Dataset')
st.write(filtered_data.info())

# Menampilkan statistik deskriptif
st.subheader('Statistik Deskriptif')
st.write(filtered_data.describe())

# Visualisasi 1: Pengaruh kecepatan angin terhadap jumlah peminjaman sepeda
st.subheader('Pengaruh Kecepatan Angin terhadap Jumlah Peminjaman Sepeda')
fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(x='windspeed', y='cnt', data=filtered_data, ax=ax)
plt.title('Pengaruh Kecepatan Angin terhadap Jumlah Peminjaman Sepeda')
plt.xlabel('Kecepatan Angin')
plt.ylabel('Jumlah Peminjaman Sepeda')
st.pyplot(fig)

# Visualisasi 2: Perbedaan pola peminjaman antara pengguna casual dan registered
st.subheader('Perbedaan Pola Peminjaman antara Pengguna Casual dan Registered')
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
# Plot 1: Pointplot for casual users
sns.pointplot(x='hr', y='casual', hue='day_type', data=filtered_data, ax=axes[0, 0])
axes[0, 0].set_title('Pola Peminjaman (Casual)')
# Plot 2: Pointplot for registered users
sns.pointplot(x='hr', y='registered', hue='day_type', data=filtered_data, ax=axes[0, 1])
axes[0, 1].set_title('Pola Peminjaman (Registered)')
# Plot 3: Boxplot for casual users
sns.boxplot(x='day_type', y='casual', hue='weathersit', data=filtered_data, ax=axes[1, 0])
axes[1, 0].set_title('Distribusi Peminjaman (Casual)')
# Plot 4: Boxplot for registered users
sns.boxplot(x='day_type', y='registered', hue='weathersit', data=filtered_data, ax=axes[1, 1])
axes[1, 1].set_title('Distribusi Peminjaman (Registered)')
st.pyplot(fig)
