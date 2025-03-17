# prompt: tolong buatkan saya code dashboard sederhana streamlit sesuai dengan hasil analisis diatas yang akan menampilkan hasil dari visualisasi di dashboard sesuai dengan analisa di notebook yaitu pada tahap Visualization & Explanatory Analysis dan dashboard nya dilengkapi dengan fitur interaktif buat kedalam bahasa indonesia

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the combined dataset (replace with your actual file path)
df = pd.read_csv('main_data.csv')

# Judul Dashboard
st.title('Dashboard Analisis Peminjaman Sepeda')

# Sidebar untuk filter
st.sidebar.header('Filter Data')

# Filter berdasarkan tipe hari (weekday/weekend)
selected_day_type = st.sidebar.selectbox('Pilih Tipe Hari', ['Weekday', 'Weekend'])
filtered_df = df[df['day_type'] == selected_day_type]

# Visualisasi 1: Pola Peminjaman Pengguna Terdaftar
st.header('Pola Peminjaman Pengguna Terdaftar')
fig, ax = plt.subplots(figsize=(12, 6))
sns.pointplot(x='hr', y='registered', hue='day_type', data=filtered_df, ax=ax)
plt.title('Pola Peminjaman Pengguna Terdaftar pada Hari Kerja dan Akhir Pekan')
plt.xlabel('Jam')
plt.ylabel('Jumlah Peminjaman (Registered)')
st.pyplot(fig)

# Visualisasi 2: Pola Peminjaman Sepeda pada Jam Sibuk
st.header('Pola Peminjaman Sepeda pada Jam Sibuk')
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='rush_hour', y='cnt', hue='day_type', data=filtered_df, ax=ax)
plt.title('Pola Peminjaman Sepeda pada Jam Sibuk (Pagi & Sore)')
plt.xlabel('Jam Sibuk')
plt.ylabel('Jumlah Peminjaman Sepeda')
st.pyplot(fig)


# Menambahkan informasi tambahan atau metrik lain
st.header("Informasi Tambahan")
st.write("Anda dapat menambahkan informasi lain di sini.")

# Contoh metrik: Rata-rata peminjaman
average_rentals = filtered_df['cnt'].mean()
st.metric(label="Rata-rata Peminjaman", value=average_rentals)
