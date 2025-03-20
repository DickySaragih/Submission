import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_day = pd.read_csv("https://raw.githubusercontent.com/DickySaragih/Submission/refs/heads/main/data/day.csv")
df_hour = pd.read_csv("https://raw.githubusercontent.com/DickySaragih/Submission/refs/heads/main/data/hour.csv")

st.title("Dashboard Analisis Peminjaman Sepeda")

st.sidebar.header("Filter Data")
selected_day_type = st.sidebar.radio("Pilih Tipe Hari", ["weekday", "weekend"])

if selected_day_type == "Hari Kerja":
    df_day_filtered = df_day[df_day["weekday"] < 5]
    df_hour_filtered = df_hour[df_hour["weekday"] < 5]
elif selected_day_type == "Akhir Pekan":
    df_day_filtered = df_day[df_day["weekday"] >= 5]
    df_hour_filtered = df_hour[df_hour["weekday"] >= 5]
else:
    df_day_filtered = df_day
    df_hour_filtered = df_hour



st.header("Visualisasi Data")

st.subheader("Pola Peminjaman Sepeda Registered pada Hari Kerja Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="dteday", y="registered", hue="weathersit", data=df_day_filtered, ax=ax)
plt.title("Pola Peminjaman Sepeda Registered pada Hari Kerja Berdasarkan Kondisi Cuaca")
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Peminjaman Registered")
plt.legend(title="Kondisi Cuaca", loc="upper left")
st.pyplot(fig)


st.subheader("Pola Peminjaman Sepeda pada Jam Sibuk (Hari Kerja vs. Akhir Pekan)")
busy_hours_df = df_hour_filtered[(df_hour_filtered["hr"] >= 7) & (df_hour_filtered["hr"] <= 9) | (df_hour_filtered["hr"] >= 17) & (df_hour_filtered["hr"] <= 19)]
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x="weekday", y="cnt", data=busy_hours_df, ax=ax)
plt.title("Pola Peminjaman Sepeda pada Jam Sibuk (Hari Kerja vs. Akhir Pekan)")
plt.xlabel("Hari (0: Minggu, 1: Senin, dst)")
plt.ylabel("Jumlah Peminjaman")
st.pyplot(fig)

st.header("Informasi Tambahan")
st.markdown(
    """
    - **Rata-rata Peminjaman Sepeda Harian:** {}
    - **Rata-rata Peminjaman Sepeda pada Jam Sibuk:** {}
    """.format(
        round(df_day_filtered["cnt"].mean(), 2), 
        round(busy_hours_df["cnt"].mean(), 2)
    )
)

