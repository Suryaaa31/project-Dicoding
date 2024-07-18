import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

bike_day_df = pd.read_csv("https://raw.githubusercontent.com/Suryaaa31/Dicoding-Proyek-Analisis-Data/master/Bike-sharing-dataset/day.csv")
bike_day_df.head()

#Mengubah bulan dari angka menjadi nama bulan
bike_day_df['mnth'] = bike_day_df['mnth'].map({
    1: 'Januari', 2: 'Februari', 3: 'Maret',
    4: 'April', 5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
})

#Mengubah musim/season dengan nama musim
bike_day_df['season'] = bike_day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Autumn', 4: 'Winter'
})

#Mengubah kondisi awan dengan nama yang mudah
bike_day_df['weathersit'] = bike_day_df['weathersit'].map({
    1: 'Sunny', 2: 'Cloudly', 3: 'Rain', 4: 'Snow'
})

#Membuat bike_daily_rent_df
def create_bike_daily_rent_df(df):
    bike_daily_rent_df = df.groupby('dteday').agg({'cnt': 'sum'}).reset_index()
    return bike_daily_rent_df

#Membuat bike_daily_casual_rent_df
def create_bike_daily_casual_rent_df(df):
    bike_daily_casual_rent_df = df.groupby('dteday').agg({'casual': 'sum'}).reset_index()
    return bike_daily_casual_rent_df

#Membuat bike_daily_registered_rent_df
def create_bike_daily_registered_rent_df(df):
    bike_daily_registered_rent_df = df.groupby('dteday').agg({'registered': 'sum'}).reset_index()
    return bike_daily_registered_rent_df

#Membuat bike_seasonal_usage_df
def create_bike_seasonal_usage_df(df):
    bike_seasonal_usage_df = df.groupby('season').agg({'registered': 'sum', 'casual': 'sum'}).reset_index()
    return bike_seasonal_usage_df 

#Membuat bike_weekday_usage_df
def create_bike_weekday_usage_df(df):
    bike_weekday_usage_df = df.groupby('weekday').agg({'cnt': 'sum'}).reset_index()
    return bike_weekday_usage_df
    
#Membuat bike_workingday_usage_df
def create_bike_workingday_usage_df(df):
    bike_workingday_usage_df = df.groupby('workingday').agg({'cnt': 'sum'}).reset_index()
    return bike_workingday_usage_df

def create_bike_holiday_usage_df(df):
    bike_holiday_usage_df = df.groupby('holiday').agg({'cnt': 'sum'}).reset_index() 
    return bike_holiday_usage_df

#Membuat bike_weather_usage_df
def create_bike_weather_usage_df(df):
    bike_weather_usage_df = df.groupby('weathersit').agg({'cnt': 'sum'})
    return bike_weather_usage_df

#Komponen filter
min_date = pd.to_datetime(bike_day_df['dteday']).min()
max_date = pd.to_datetime(bike_day_df['dteday']).max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/Suryaaa31/Dicoding-Proyek-Analisis-Data/master/logo.png")
    #Mengambil start_date dan end_date dari input
    start_date, end_date = st.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
    )

main_df = bike_day_df[(bike_day_df['dteday'] >= str(start_date)) & (bike_day_df['dteday'] <= str(end_date))]

#Data Frame
bike_daily_rent_df = create_bike_daily_rent_df(main_df)
bike_daily_casual_rent_df = create_bike_daily_casual_rent_df(main_df)
bike_daily_registered_rent_df = create_bike_daily_registered_rent_df(main_df)
bike_seasonal_usage_df = create_bike_seasonal_usage_df(main_df)
bike_weekday_usage_df = create_bike_weekday_usage_df(main_df)
bike_workingday_usage_df = create_bike_workingday_usage_df(main_df)
bike_holiday_usage_df = create_bike_holiday_usage_df(main_df)
bike_weather_usage_df = create_bike_weather_usage_df(main_df)


#Proses membuat Dashboard

#Header
st.header("Bike Rental Dashboard")

st.subheader("Daily Bike Rental")
col1, col2, col3 = st.columns(3)

with col1:
    bike_daily_casual_rent = bike_daily_casual_rent_df['casual'].sum()
    st.metric(label="Casual Users", value=bike_daily_casual_rent)

with col2:
    bike_daily_registered_rent = bike_daily_registered_rent_df['registered'].sum()
    st.metric(label="Registered Users", value=bike_daily_registered_rent)

with col3:
    bike_daily_rent = bike_daily_rent_df['cnt'].sum()
    st.metric(label="Total Users", value=bike_daily_rent)


st.subheader('Pengguna sepeda berdasarkan Kondisi Cuaca')
fig, ax = plt.subplots(figsize=(13,10))
color=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(x=bike_weather_usage_df.index,y=bike_weather_usage_df['cnt'], color=color[0], ax=ax)

for index, row in enumerate(bike_weather_usage_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Penguna')
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.subheader('Pengguna Sepeda Pada Weekday, Holiday, and Working Day')
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 12))

colors1=["tab:blue", "tab:orange"]
colors2=["tab:blue", "tab:orange"]
colors3=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]
plt.subplots_adjust(hspace=0.4)

sns.barplot(x='workingday', y='cnt', data=bike_workingday_usage_df, palette=colors1, ax=axes[0])
for index, row in enumerate(bike_workingday_usage_df['cnt']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=10)

axes[0].set_title('Pengguna Sepeda pada Working Day')
axes[0].set_ylabel('Jumlah Pengguna Sepeda')
axes[0].tick_params(axis='x', labelsize=20)
axes[0].tick_params(axis='y', labelsize=15)


sns.barplot(x='holiday', y='cnt', data=bike_holiday_usage_df,palette=colors2, ax=axes[1])
for index, row in enumerate(bike_holiday_usage_df['cnt']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=10)

axes[1].set_title("Pengguna Sepeda pada Holiday")
axes[1].set_ylabel('Jumlah Pengguna Sepeda')
axes[1].tick_params(axis='x', labelsize=20)
axes[1].tick_params(axis='y', labelsize=15)

sns.barplot(x='weekday', y='cnt', data=bike_weekday_usage_df,palette=colors3, ax=axes[2])
for index, row in enumerate(bike_weekday_usage_df['cnt']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=10)

axes[2].set_title("Pengguna Sepeda pada Weekday")
axes[2].set_ylabel('Jumlah Pengguna Sepeda')
axes[2].tick_params(axis='x', labelsize=20)
axes[2].tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.subheader('Pengguna Sepeda Berdasrkan Musim')
fig, ax = plt.subplots(figsize=(13,10))
sns.barplot(x='season', y='registered', data=bike_seasonal_usage_df, label='Registered', color="blue", ax=ax)
sns.barplot(x='season', y='casual', data=bike_seasonal_usage_df, label='Casual', color="orange", ax=ax)


for index, row in bike_seasonal_usage_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=10)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=10)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=45)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.subheader('Casual Registered dan Musim')

fig, axes = plt.subplots(3, 1, figsize=(10, 12))
plt.subplots_adjust(hspace=0.4)
sns.scatterplot(x='temp', y='cnt', data=bike_day_df, ax=axes[0])
axes[ 0].set_title('Temp vs Count')

sns.scatterplot(x='atemp', y='cnt', data=bike_day_df, ax=axes[1])
axes[1].set_title('Atemp vs Count')

sns.scatterplot(x='hum', y='cnt', data=bike_day_df, ax=axes[2])
axes[2].set_title('Hum vs Count')


plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright (c) Suryadi 2024')
