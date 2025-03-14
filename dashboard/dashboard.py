# prompt: buatkan saya dashboard untuk rangkaian kode diatas sederhana pada streamlit

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Tahap 1: Mengambil Data dari GitHub ---
URL_DAY = "https://raw.githubusercontent.com/DickySaragih/Submission/refs/heads/main/data/day.csv"
URL_HOUR = "https://raw.githubusercontent.com/DickySaragih/Submission/refs/heads/main/data/hour.csv"
df_day = pd.read_csv(URL_DAY)
df_hour = pd.read_csv(URL_HOUR)

# --- Streamlit Dashboard ---
st.title("Bike Sharing Dataset Analysis")

st.header("Data Overview")
st.write("Berikut adalah 5 baris pertama dari dataset harian:")
st.dataframe(df_day.head())

st.write("Berikut adalah 5 baris pertama dari dataset per jam:")
st.dataframe(df_hour.head())

st.header("Descriptive Statistics")
st.write("Statistik deskriptif dataset harian:")
st.dataframe(df_day.describe())

st.write("Statistik deskriptif dataset per jam:")
st.dataframe(df_hour.describe())

st.header("Visualizations")

# Visualisasi 1: Pengaruh kecepatan angin
st.subheader("Pengaruh Kecepatan Angin terhadap Jumlah Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x=df_day["windspeed"], y=df_day["cnt"], alpha=0.6, ax=ax)
plt.title("Pengaruh Kecepatan Angin terhadap Jumlah Peminjaman Sepeda")
plt.xlabel("Kecepatan Angin")
plt.ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig)

# Visualisasi 2: Perbedaan pola peminjaman
st.subheader("Perbedaan Peminjaman antara Pengguna Kasual dan Terdaftar")
weekend_vs_weekday = df_day.groupby("workingday")[["casual", "registered"]].mean()
fig, ax = plt.subplots(figsize=(8, 5))
weekend_vs_weekday.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
plt.title("Perbedaan Peminjaman antara Pengguna Kasual dan Terdaftar")
plt.xlabel("Hari Kerja (0 = Akhir Pekan, 1 = Hari Kerja)")
plt.ylabel("Rata-rata Jumlah Peminjaman")
plt.xticks(ticks=[0, 1], labels=["Akhir Pekan", "Hari Kerja"], rotation=0)
plt.legend(["Kasual", "Terdaftar"])
st.pyplot(fig)


# Visualisasi 3: Korelasi faktor cuaca
st.subheader("Korelasi antara Faktor Cuaca dan Jumlah Peminjaman Sepeda")
correlation_matrix = df_day[["temp", "hum", "windspeed", "cnt"]].corr()
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
plt.title("Korelasi antara Faktor Cuaca dan Jumlah Peminjaman Sepeda")
st.pyplot(fig)

st.header("Kesimpulan")
st.write("1. Kecepatan angin tidak memiliki dampak signifikan terhadap jumlah peminjaman sepeda.")
st.write("2. Pengguna kasual lebih sering menyewa saat akhir pekan, sedangkan pengguna terdaftar lebih sering pada hari kerja.")
st.write("3. Suhu berpengaruh besar terhadap peminjaman, sedangkan kelembaban tinggi cenderung menurunkan peminjaman.")
