import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load Data ---
@st.cache_data
def load_data():
    URL_DAY = "https://raw.githubusercontent.com/DickySaragih/Submission/refs/heads/main/data/day.csv"
    df = pd.read_csv(URL_DAY)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

df = load_data()

# --- Sidebar untuk Filter ---
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", df['dteday'].dt.year.unique())
df_filtered = df[df['dteday'].dt.year == selected_year]

selected_season = st.sidebar.selectbox("Pilih Musim", ["Semua", "Musim Panas", "Musim Dingin"])
if selected_season == "Musim Panas":
    df_filtered = df_filtered[df_filtered['season'].isin([2, 3])]
elif selected_season == "Musim Dingin":
    df_filtered = df_filtered[df_filtered['season'].isin([1, 4])]

selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", df_filtered['weathersit'].unique(), df_filtered['weathersit'].unique())
df_filtered = df_filtered[df_filtered['weathersit'].isin(selected_weather)]

# --- Visualisasi 1: Pengaruh Cuaca terhadap Peminjaman ---
st.subheader("Pengaruh Cuaca terhadap Peminjaman Sepeda")
weather_data = df_filtered.groupby('weathersit').agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
weather_mapping = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan'}
weather_data['weathersit'] = weather_data['weathersit'].map(weather_mapping)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(weather_data['weathersit'], weather_data['casual'], label='Casual', alpha=0.7)
ax.bar(weather_data['weathersit'], weather_data['registered'], bottom=weather_data['casual'], label='Registered', alpha=0.7)
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Peminjaman Sepeda')
ax.set_title('Pengaruh Cuaca terhadap Peminjaman Sepeda')
ax.legend()
st.pyplot(fig)

# --- Visualisasi 2: Tren Penggunaan Sepeda antara Musim Panas dan Dingin ---
st.subheader("Perbandingan Tren Penggunaan Sepeda di Musim Panas dan Dingin")
df_summer = df_filtered[df_filtered['season'].isin([2, 3])]
df_winter = df_filtered[df_filtered['season'].isin([1, 4])]

summer_trend = df_summer.groupby(df_summer['dteday'].dt.month)['registered'].sum()
winter_trend = df_winter.groupby(df_winter['dteday'].dt.month)['registered'].sum()

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(summer_trend.index, summer_trend.values, color='yellow', label='Musim Panas', alpha=0.7)
ax.bar(winter_trend.index, winter_trend.values, color='blue', label='Musim Dingin', alpha=0.7)
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Peminjaman Sepeda (Registered)')
ax.set_title('Perbandingan Tren Penggunaan Sepeda antara Musim Panas dan Dingin')
ax.legend()
st.pyplot(fig)

# --- Informasi Data ---
st.subheader("Statistik Rata-rata Pengguna Terdaftar per Bulan")
monthly_registered_users = df_filtered.groupby(df_filtered['dteday'].dt.month)['registered'].mean()
st.dataframe(monthly_registered_users)
