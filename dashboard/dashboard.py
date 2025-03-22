import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = "main_data.csv"  # Menggunakan file day.csv dari dataset

df = pd.read_csv(file_path)
df['dteday'] = pd.to_datetime(df['dteday'])

# Dictionary kondisi cuaca
weather_conditions = {
    1: 'Cerah',
    2: 'Mendung',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}

# --- Streamlit App ---
st.set_page_config(layout="wide")  # Menggunakan layout lebar

st.title("Bike Sharing Dashboard")

# Sidebar untuk interaktif
with st.sidebar:
    st.header("Filter Data")
    selected_year = st.selectbox("Pilih Tahun", df['dteday'].dt.year.unique())
    df_filtered_year = df[df['dteday'].dt.year == selected_year]
    
    selected_month = st.selectbox("Pilih Bulan", df_filtered_year['dteday'].dt.month.unique())
    df_filtered_month = df_filtered_year[df_filtered_year['dteday'].dt.month == selected_month]

    # --- Tabel Data Terfilter ---
st.subheader("Data Terfilter")
st.dataframe(df_filtered_month)


# Layout dengan kolom
col1, col2 = st.columns(2)

# --- Visualisasi 1: Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda ---
with col1:
    st.subheader("Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman Sepeda")
    df_2011 = df[(df["dteday"].dt.year == 2011)]
    fig, ax = plt.subplots(figsize=(10,5))
    for condition in df_2011["weathersit"].unique():
        subset = df_2011[df_2011["weathersit"] == condition]
        casual_mean = subset["casual"].mean()
        registered_mean = subset["registered"].mean()
        ax.bar(f"Cuaca {weather_conditions[condition]}", casual_mean, label="Peminjaman Kasual", color="skyblue")
        ax.bar(f"Cuaca {weather_conditions[condition]}", registered_mean, bottom=casual_mean, label="Peminjaman Terdaftar", color="orange")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Peminjaman")
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    st.pyplot(fig)

# --- Visualisasi 2: Perbedaan Tren Penggunaan Sepeda berdasarkan Musim ---
with col2:
    st.subheader("Perbedaan Tren Penggunaan Sepeda antara Musim Panas dan Musim Dingin")
    df_2011_registered = df[(df['dteday'].dt.year == 2011) & (df['season'].isin([1, 3]))]
    season_trend = df_2011_registered.groupby(['season'])['registered'].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    season_trend.plot(kind='bar', color=['blue', 'orange'], ax=ax)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xticklabels(['Musim Dingin', 'Musim Panas'], rotation=0)
    st.pyplot(fig)

# --- Visualisasi Interaktif ---
st.subheader("Rata-rata Pengguna Terdaftar per Hari dalam Seminggu")
fig, ax = plt.subplots(figsize=(10, 5))
weekly_data = df_filtered_month.groupby(df_filtered_month['dteday'].dt.dayofweek)['registered'].mean().reset_index()
weekly_data = weekly_data.sort_values(by='dteday')
sns.barplot(data=weekly_data, x='dteday', y='registered', color='blue', ax=ax)
ax.set_xlabel('Hari dalam Seminggu (0=Senin, 6=Minggu)')
ax.set_ylabel('Rata-rata Jumlah Pengguna Terdaftar')
ax.set_xticklabels(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
st.pyplot(fig)

st.markdown("\n\n")
