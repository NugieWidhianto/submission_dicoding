import streamlit as st
import pandas as pd
import datetime
import io
import seaborn as sns
import matplotlib.pyplot as plt #import pyplot dari matplotlib


day_df = pd.read_csv('dashboard/clean_day.csv')
hour_df = pd.read_csv('dashboard/clean_hour.csv')

st.title('Data Analytics Project : Bike Sharing')

# Sidebar
# Inisialisasi variabel
selected_database = True
selected_database_hour = False
selected_cleaning = False
selected_vis = False
selected_EDA = False

st.sidebar.title("Data Assessing")

# Tombol untuk memilih Dataset "Day"
if st.sidebar.button("Dataset Day"):
    selected_database = True
    selected_database_hour = False
    selected_cleaning = False
    selected_vis = False
    selected_EDA = False

# Tombol untuk memilih Dataset "Hour"
if st.sidebar.button("Dataset Hour"):
    selected_database = False
    selected_database_hour = True
    selected_cleaning = False
    selected_vis = False
    selected_EDA = False

# Sidebar 2
st.sidebar.title("Data Cleaning & Fixing")
if st.sidebar.button("Data Cleaning"):
    selected_database = False
    selected_database_hour = False
    selected_cleaning = True
    selected_vis = False
    selected_EDA = False

# Sidebar 3
st.sidebar.title("EDA & Data Visualization")
if st.sidebar.button("Data Visualization"):
    selected_database = False
    selected_database_hour = False
    selected_cleaning = False
    selected_vis = True
    selected_EDA = False

if st.sidebar.button("Exploratory Data Analytics"):
    selected_database = False
    selected_database_hour = False
    selected_cleaning = False
    selected_vis = False
    selected_EDA = True
     
if selected_database:
    st.header('Dataset Day')
    st.dataframe(day_df)
    st.subheader("Describe Dataset Day")
    st.write(day_df.describe())

if selected_database_hour:
    show_main_page = False
    selected_database = False
    st.header('Dataset Hour')
    st.dataframe(hour_df)
    st.subheader("Describe Dataset Hour")
    st.write(hour_df.describe())
    
if selected_cleaning:
    st.header('Data Cleaning & Fixing')
    st.subheader("1. Merubah Value 0 Pada Kolom Humidity Menggunakan Mean dari Kolom Tersebut")
    code = """
        day_df['hum'].replace(0, day_df['hum'].mean(), inplace=True)
        """
    st.code(code, language="python")
    day_df['hum'].replace(0, day_df['hum'].mean(), inplace=True)
    st.write(day_df.describe())
    
    st.subheader("2. Perubahan Tipe Data dteday menjadi Datetime")
    code = """
        datetime_columns_day = ["dteday"]
        for column in datetime_columns_day:
            day_df[column] = pd.to_datetime(day_df[column])
        """
    st.code(code, language="python")
    datetime_columns_day = ["dteday"]
    for column in datetime_columns_day:
        day_df[column] = pd.to_datetime(day_df[column])
    buffer = io.StringIO()
    day_df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    
    # Pembuatan Visualisasi Dasar untuk Key Insights
if selected_vis:
    st.header('Key Insights')
    fig, ax = plt.subplots(figsize=(16, 8))
    col1, col2, col3,col4 = st.columns(4)
 
    with col1:
        Rent_Totals = day_df['cnt'].sum()
    st.metric("Rents Totals", value=Rent_Totals)
    ax=ax
    with col2:
        Days_Total = day_df['dteday'].count() 
    st.metric("Days Total On Data", value=Days_Total)
    ax=ax
    with col3:
        Data_Total = hour_df['dteday'].count()
    st.metric("Collected Data's Counts",value = Data_Total)
    ax=ax
    with col4:
        tanggal_data = ("2011-2012")
    st.metric("Tahun Data",value= tanggal_data)



    #Vis 1
    st.markdown("<br>", unsafe_allow_html=True)
    st.header('Visualisasi Data')
    col1, col2, col3, col4, col5,col6,col7 = st.columns(7)

    with col1:
        fig, ax = plt.subplots(figsize=(10, 8))
    season_total_count = day_df.groupby('season')['cnt'].sum().reset_index()
    season = ["Spring","Summer","Fall","Winter"]
    colors = ('#8B4513', '#FFF8DC', '#93C572', '#E67F0D')
    explode = (0, 0, 0.1, 0)
    palette_color = sns.color_palette('bright') 
  
    st.subheader('1) Rent Total by Seasons')
    plt.pie(season_total_count['cnt'], labels=season, colors=palette_color, 
        explode=explode, autopct='%.0f%%')
    plt.show()
    st.pyplot(fig)
    with col2:
        mnth_total_cnt = day_df.groupby('mnth')['cnt'].sum().reset_index()

    # Mengganti label pada 'mnth' sesuai dengan nama bulan yang diinginkan
    months_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des']
    mnth_total_cnt['mnth'] = mnth_total_cnt['mnth'].map(dict(enumerate(months_labels)))

    # Membuat bar chart
    st.subheader('2) Rent Totals By Months')
    fig, ax = plt.subplots(figsize=(18, 10))
    sns.barplot(x='mnth', y='cnt', data=mnth_total_cnt, ax=ax)

    # Menambahkan label pada sumbu-sumbu
    plt.xlabel('Months',size=24)
    plt.ylabel('Rent Totals',size=20)

    # Menambahkan nilai asli count di atas setiap bar
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    fontsize=20, color='black',
                    xytext=(0, 7), 
                    textcoords='offset points')
    st.pyplot(fig)
    with col3:
        fig, ax = plt.subplots(figsize=(10, 8))
    # Grouping data berdasarkan 'workingday' dan menghitung jumlah 'cnt' pada setiap kondisi kerja
    workingday_total_cnt = day_df.groupby('workingday')['cnt'].sum().reset_index()

    # Mengganti label pada 'workingday' sesuai dengan label yang diinginkan
    workingday_labels = ['Non-Working Days', 'Working Days']
    workingday_total_cnt['workingday'] = workingday_total_cnt['workingday'].map(dict(enumerate(workingday_labels)))

    
    explode = (0.1, 0)
    palette_color = sns.color_palette('bright') 
  
    st.subheader('3) Rent Total On Working Days vs Non-Working Days')
    plt.pie(workingday_total_cnt['cnt'], labels=workingday_labels, colors=palette_color, 
        explode=explode, autopct='%.0f%%')
    plt.show()

    # Menampilkan Pie Chart di Streamlit    
    st.pyplot(fig)

    with col4:
        days_total_cnt = day_df.groupby('weekday')['cnt'].sum().reset_index()

    # Mengganti label pada 'days' sesuai dengan nama hari yang diinginkan
    days_labels = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    days_total_cnt['weekday'] = days_total_cnt['weekday'].map(dict(enumerate(days_labels)))

    # Membuat bar chart
    st.subheader('4) Rent Totals By Days')
    fig, ax = plt.subplots(figsize=(18, 10))
    sns.barplot(x='weekday', y='cnt', data=days_total_cnt, ax=ax)

    # Menambahkan label pada sumbu-sumbu
    plt.xlabel('Weekdays',size=24)
    plt.ylabel('Rent Totals',size=20)

    # Menambahkan nilai asli count di atas setiap bar
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    fontsize=20, color='black',
                    xytext=(0, 7), 
                    textcoords='offset points')
    st.pyplot(fig)

    with col5:
        hours_total_cnt = hour_df.groupby('hr')['cnt'].sum().reset_index()
    # Membuat bar chart
    st.subheader('5) Rent Totals By Hours')
    fig, ax = plt.subplots(figsize=(30, 18))
    sns.barplot(x='hr', y='cnt', data=hours_total_cnt, ax=ax)

    # Menambahkan label pada sumbu-sumbu
    plt.xlabel('Time',size=24)
    plt.ylabel('Rent Totals',size=20)

    # Menambahkan nilai asli count di atas setiap bar
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    fontsize=20, color='black',
                    xytext=(0, 7), 
                    textcoords='offset points')
    st.pyplot(fig)

    with col6:
        hours_total_cnt = day_df.groupby('dteday')['cnt'].sum().reset_index()
    # Membuat bar chart
    st.subheader('6) Rent Totals By Date')
    fig, ax = plt.subplots(figsize=(25, 10))
    ax.plot(
    day_df["dteday"],
    day_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
    )
    plt.xlabel('Date',size=24)
    plt.ylabel('Rent Totals',size=20)
    ax.tick_params(axis='y', labelsize=15)
    ax.tick_params(axis='x', labelsize=15)
 
    st.pyplot(fig)

    with col7:
        def categorize_hum(hum):
            if hum >= 0 and hum <= 10:
                return '0-10'
            elif hum > 10 and hum <= 20:
                return '10-20'
            elif hum > 20 and hum <= 30:
                return '20-30'
            elif hum > 30 and hum <= 40:
                return '30-40'
            elif hum > 40 and hum <= 50:
                return '40-50'
            elif hum > 60 and hum <= 70:
                return '60-70'
            elif hum > 70 and hum <= 80:
                return '70-85'
            elif hum > 80 and hum <= 90:
                return '80-90'
            elif hum > 90 and hum <= 100:
                return '90-100'
    day_df['original_hum'] = day_df['hum'] * 100
    # Menambahkan kolom kategori Humidity yang baru ke day_df dataframe
    day_df['hum_range'] = day_df['original_hum'].apply(categorize_hum)

    # Menghitung rata-rata jumlah penyewaan untuk setiap rentang Humidity
    avg_count_by_hum_range = day_df.groupby('hum_range')['cnt'].mean().reset_index()

    # Membuat barplot dengan Seaborn
    st.subheader('7) Rata-rata Jumlah Penyewaan Berdasarkan Rentang Humidity / Kelembapan')
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(x='hum_range', y='cnt', data=avg_count_by_hum_range, ax=ax)

    # Menambahkan label pada sumbu-sumbu
    plt.xlabel('Humidity Range')
    plt.ylabel('Average Rents')

    # Menambahkan nilai rata-rata di atas setiap bar
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    fontsize=12, color='black',
                    xytext=(0, 7), 
                    textcoords='offset points')

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

if selected_EDA:
    st.header('Business Problems and Questions')
    fig, ax = plt.subplots(figsize=(16, 8))
    col1, col2, col3,col4,col5,col6,col7 = st.columns(7)

    with col1:
        question1 = ("Rent Totals By Seasons")
    st.metric("1.Pengaruh Musim Terhadap Jumlah Peminjaman Sepeda",value= question1)
    with col2:
        question2 = ("Rent Totals By Months")
    st.metric("2.Pengaruh Bulan Terhadap Jumlah Peminjaman Sepeda",value= question2)
    with col3:
        question3 = ("Rent Totals on Working Days vs Non-Working Days")
    st.metric("3.Perbandingan Antara Hari Kerja dan Non-Hari Kerja dalam Jumlah Peminjaman Sepeda",value= question3)
    with col4:
        question4 = ("Rent Totals By Days")
    st.metric("4.Pengaruh Hari Terhadap Jumlah Peminjaman Sepeda",value= question4)
    with col5:
        question5 = ("Rent Totals By Hours/Time")
    st.metric("5.Pengaruh Jam Terhadap Jumlah Peminjaman Sepeda",value= question5)
    with col6:
        question6 = ("Rent Totals By Date")
    st.metric("6.Jumlah Peminjaman Sepeda Berdasarkan Tanggal",value= question6)
    with col7:
        question7 = ("Average Rents by Humidity Ranges")
    st.metric("7.Jumlah Rata-Rata Peminjaman Sepeda Berdasarkan Range Humiditas",value=question7)