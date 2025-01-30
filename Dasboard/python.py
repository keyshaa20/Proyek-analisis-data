import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_byweatherr_df(df):
    byweatherr_df = df.groupby(by="weathersit_x").registered_x.nunique().reset_index()
    byweatherr_df.rename(columns={
        "registered_x": "registered_count"
    }, inplace=True)
    
    return byweatherr_df

def create_byweatherc_df(df):
    byweatherc_df = df.groupby(by="weathersit_x").casual_x.nunique().reset_index()
    byweatherc_df.rename(columns={
        "casual_x": "casual_count"
    }, inplace=True)
    
    return byweatherc_df

def create_byworkingday_df(df):
    byworkingday_df = df.groupby(by="workingday_y").cnt_y.nunique().reset_index()
    byworkingday_df.rename(columns={
        "cnt_y": "customer_count"
    }, inplace=True)
    
    return byworkingday_df

def create_byweekday_df(df):
    byweekday_df = df.groupby(by="weekday_y").cnt_y.nunique().reset_index()
    byweekday_df.rename(columns={
        "cnt_y": "customer_count"
    }, inplace=True)

    return byweekday_df

all_df = pd.read_csv('all_data (2).csv')

print(all_df)

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image('https://png.pngtree.com/png-clipart/20200727/original/pngtree-bike-logo-png-image_5087473.jpg')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]
    
byweatherr_df = create_byweatherr_df(main_df)
byweatherc_df = create_byweatherc_df(main_df)
byworkingday_df = create_byworkingday_df(main_df)
byweekday_df = create_byweekday_df(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader("Statistik Penyewaan pada hari kerja dan libur (Per jam)")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(x="workingday_y", y="customer_count", data=byworkingday_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Penyewa pada hari kerja, akhir pekan dan liburan (perjam)", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="weekday_y", y="customer_count", data=byweekday_df.sort_values(by="weekday_y", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Visualisasi Data Hari Penyewaan (perjam)", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)
st.pyplot(fig)

st.subheader("Statistik Pengguna Registered dan Casual berdasarkan cuaca (Per hari)")

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="registered_count", 
    y="weathersit_x",
    data=byweatherr_df.sort_values(by="registered_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Registered User by weather (day)", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="casual_count", 
    y="weathersit_x",
    data=byweatherc_df.sort_values(by="casual_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Casual User by weather (day)", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

