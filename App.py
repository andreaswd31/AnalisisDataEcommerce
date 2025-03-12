import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Load Data
all_df = pd.read_csv("all_df.csv")

all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
latest_date = all_df['order_purchase_timestamp'].max()


all_df['seller_state'] = all_df['seller_state'].fillna('Unknown')
all_df['seller_state'] = all_df['seller_state'].astype(str)
seller_count = all_df.groupby('seller_state')['seller_id'].nunique().reset_index()
seller_count = seller_count.sort_values(by='seller_id', ascending=False)
seller_count['seller_state'] = seller_count['seller_state'].astype(str)  # Pastikan string
all_df = all_df[(all_df['delivery_time'] >= 0) & (all_df['delivery_time'] < 100)]

with st.sidebar:
    st.image("logo.png",  use_container_width=False, width=250)
    
# Sidebar Navigation
menu = st.sidebar.selectbox("📌 Pilih Analisis:", ["Home", "Analisis Produk", "Rating Review Produk", "Analisis Pola Transaksi","Analysis RFM", "Customer Clustering"])
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

# rentang waktu minimum dan maksimum dari dataset
min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

with st.sidebar:
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    st.markdown("---")
    st.markdown("### 🆔 Identitas")
    st.write("**Nama:** Andreas Wirawan Dananjaya")  
    st.write("**Cohort ID:** MC006D5Y1285")  
    st.write("**Kelas:** MC - 23")  
    
    st.markdown("---")
    st.markdown("### 📥 Download Dataset")
    st.markdown("[DATASET All_df](https://drive.google.com/file/d/1kcSbfn_P7_GtT3GDSxdryL8hBADp_GUs/view?usp=sharing)")

# Konversi input pengguna ke datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan rentang tanggal
main_df = all_df[(all_df["order_purchase_timestamp"] >= start_date) & 
                 (all_df["order_purchase_timestamp"] <= end_date)]


# ====================== HOME ======================
if menu == "Home":
    st.title("Brazilian E-Commerce Public Dashboard")
    st.write("Selamat datang! Dashboard ini menampilkan analisis data penjualan e-commerce.")

    # Rangkuman Kinerja Penjualan
    st.header("Tren Penjualan dan Revenue (2016 - 2018)")

    # Konversi Tanggal
    all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
    all_df['order_month'] = all_df['order_purchase_timestamp'].dt.strftime('%Y-%m')

    # Grouping Data
    monthly_sales = all_df.groupby('order_month').agg(
        total_orders=('order_id', 'count'),
        total_revenue=('payment_value', 'sum')
    ).reset_index()

    # Visualisasi 
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Month')
    ax1.set_ylabel('Number of Orders', color='tab:blue')
    ax1.plot(monthly_sales['order_month'], monthly_sales['total_orders'], marker='o', label='Number of Orders', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_xticks(range(len(monthly_sales['order_month'])))  
    ax1.set_xticklabels(monthly_sales['order_month'], rotation=45, ha='right')

    ax2 = ax1.twinx()

    # Plot Total Revenue
    sns.lineplot(data=monthly_sales, x='order_month', y='total_revenue', marker='s', ax=ax2, label='Total Revenue', color='red')
    ax2.set_ylabel('Total Revenue (Million Dollars)', color='red')
    ax2.tick_params(axis='y', colors='red')

    fig.suptitle('Number of Orders and Total Revenue per Month (2016 - 2018)')
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9), bbox_transform=ax1.transAxes)

    st.pyplot(fig)

    # Statistik 
    total_orders = all_df['order_id'].nunique()
    total_customers = all_df['customer_unique_id'].nunique()
    total_revenue = all_df['payment_value'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Orders", value=f"{total_orders:,}")
    col2.metric(label="Unique Customers", value=f"{total_customers:,}")
    col3.metric(label="Total Revenue ($)", value=f"{total_revenue:,.0f}")

    # Insight
    st.write("""
    **Analisis :**
    - Sejak akhir 2016 hingga pertengahan 2018, terdapat peningkatan jumlah pesanan dan pendapatan secara bertahap. Hal ini menunjukkan adanya pertumbuhan bisnis yang stabil dalam rentang waktu tersebut.
    - Kedua metrik ini memiliki pola yang hampir serupa, yang mengindikasikan bahwa peningkatan jumlah pesanan berdampak langsung terhadap peningkatan pendapatan.
    - Terjadi lonjakan signifikan pada November 2017, diikuti dengan penurunan tajam di bulan berikutnya.
    - Setelah lonjakan tersebut, jumlah pesanan dan pendapatan mulai stabil di angka yang relatif tinggi, meskipun terdapat fluktuasi kecil di beberapa bulan.
    """)
    
        # Visualisasi 
    st.subheader("Perbandingan Revenue per Bulan")
    fig2, ax3 = plt.subplots(figsize=(12,6))
    sns.barplot(data=monthly_sales, x='order_month', y='total_revenue', ax=ax3, color = "blue")
    ax3.set_xticklabels(monthly_sales['order_month'], rotation=45)
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Total Revenue ($)')
    ax3.set_title('Perbandingan Revenue per Bulan')

    st.pyplot(fig2)

    # Tabel Data Penting dari EDA
    st.subheader("Data Pendukung")

    # Top 5 Kota dengan Order Terbanyak
    st.write("**5 Kota dengan Order Terbanyak**")
    top_cities = all_df.groupby('customer_city')['order_id'].count().reset_index().sort_values(by='order_id', ascending=False).head(5)
    st.dataframe(top_cities)

    # Ringkasan Insight
    st.write("""
    **📌 Analisis :**
    - Sejalan dengan grafik pertama, pendapatan tertinggi terjadi pada November 2017.
    - Grafik ini mengindikasikan pertumbuhan bisnis yang pesat dengan adanya momentum kuat pada akhir 2017, yang kemudian diikuti oleh fase stabilisasi pada tahun 2018
    """)
    
# ====================== ANALISIS PRODUK ======================
elif menu == "Analisis Produk":
    st.title("Analisis Produk: Paling Laris & Paling Sedikit Terjual")

    # 15 Produk Paling Laris
    st.subheader("15 Produk Paling Laris")
    top_products = all_df.groupby('product_category_name_english')['order_item_id'].count().reset_index()
    top_products = top_products.sort_values(by='order_item_id', ascending=False).head(15)

    fig, ax = plt.subplots(figsize=(15, 6))
    sns.barplot(data=top_products, x='order_item_id', y='product_category_name_english', palette='Blues_r', ax=ax)
    ax.set_xlabel('Number of Orders')
    ax.set_ylabel('Product Categories')
    ax.set_title('Top 15 Best-Selling Products')

    for index, value in enumerate(top_products['order_item_id']):
        ax.text(value, index, f'({value})', color='black', va="center")

    st.pyplot(fig)

    # **Tabel: Top 15 Produk Paling Laris**
    st.write("**Tabel: Top 15 Produk Paling Laris**")
    st.dataframe(top_products.rename(columns={'order_item_id': 'Total Orders'}))

    # 15 Produk Paling Sedikit Terjual
    st.subheader("5 Produk Paling Sedikit Terjual")
    bottom_products = all_df.groupby('product_category_name_english')['order_item_id'].count().reset_index()
    bottom_products = bottom_products.sort_values(by='order_item_id', ascending=True).head(15)

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=bottom_products, x='order_item_id', y='product_category_name_english', palette='Reds_r', ax=ax2)
    ax2.set_xlabel('Number of Orders')
    ax2.set_ylabel('Product Categories')
    ax2.set_title('Bottom 15 Best-Selling Products')

    for index, value in enumerate(bottom_products['order_item_id']):
        ax2.text(value, index, f'({value})', color='black', va="center")

    st.pyplot(fig2)

    # **Tabel: 15 Produk dengan Penjualan Terendah**
    st.write("**Tabel: 15 Produk dengan Penjualan Terendah**")
    st.dataframe(bottom_products.rename(columns={'order_item_id': 'Total Orders'}))

    # **Insight dari Analisis Produk**
    st.subheader("Insight dari Analisis Produk")
    st.write("""
    **📌 Analisis :**
    - Kategori "bed_bath_table" menempati posisi pertama dengan jumlah pesanan terbanyak, yaitu 11.680 pesanan, Kategori "health_beauty" (9.747 pesanan) berada di posisi kedua, menandakan tingginya permintaan terhadap produk kesehatan dan kecantikan, yang mungkin mencakup skincare, suplemen, atau alat kesehatan.
    - Kategori "security_and_services" memiliki jumlah pesanan paling sedikit (2 pesanan), menunjukkan bahwa layanan keamanan atau produk terkait kurang diminati atau memiliki pangsa pasar yang sangat kecil.
    - Produk dalam kategori "fashion_childrens_clothes" dan "cds_dvds_musicals" juga memiliki permintaan yang sangat rendah (di bawah 20 pesanan), yang bisa menandakan pergeseran tren dalam industri fashion anak-anak serta berkurangnya minat terhadap media fisik seperti CD dan DVD.
    - Produk dalam kategori rumah tangga, kecantikan, olahraga, dan teknologi memiliki permintaan tinggi, sehingga bisnis dapat fokus pada kategori ini untuk meningkatkan profitabilitas.
    - Tren digitalisasi terlihat dari rendahnya permintaan terhadap produk seperti DVD/CD, yang menunjukkan bahwa bisnis sebaiknya berfokus pada distribusi digital atau produk berbasis online.
    """)
# ====================== Rating Review Produk======================
elif menu == "Rating Review Produk":
    st.title("Analisis Produk Bedasarkan Rating User")

    # Menghitung rating rata-rata per kategori dengan minimal 10 transaksi
    top_rated_products = all_df.groupby('product_category_name_english').filter(lambda x: len(x) >= 10)
    top_rated_products = top_rated_products.groupby('product_category_name_english')['review_score'].mean().reset_index()
    top_rated_products = top_rated_products.sort_values(by='review_score', ascending=False).head(10)

    bottom_rated_products = all_df.groupby('product_category_name_english').filter(lambda x: len(x) >= 10)
    bottom_rated_products = bottom_rated_products.groupby('product_category_name_english')['review_score'].mean().reset_index()
    bottom_rated_products = bottom_rated_products.sort_values(by='review_score', ascending=True).head(10)

    # 10 Produk dengan Rating Tertinggi
    st.subheader("10 Produk dengan Rating Tertinggi")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_rated_products, x='review_score', y='product_category_name_english', palette='Greens_r', ax=ax)
    ax.set_xlabel('Average Rating')
    ax.set_ylabel('Product Categories')
    ax.set_title('10 Products with the Top Ratings')
    ax.set_xlim(1, 5.0)

    for index, value in enumerate(top_rated_products['review_score']):
        ax.text(value, index, f'({value:.2f})', color='black', va='center')

    st.pyplot(fig)

    # Tabel: 10 Produk dengan Rating Tertinggi
    st.write("**Tabel: 10 Produk dengan Rating Tertinggi**")
    st.dataframe(top_rated_products.rename(columns={'review_score': 'Average Rating'}))

    # 10 Produk dengan Rating Terendah
    st.subheader("10 Produk dengan Rating Terendah")

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=bottom_rated_products, x='review_score', y='product_category_name_english', palette='Oranges_r', ax=ax2)
    ax2.set_xlabel('Average Rating')
    ax2.set_ylabel('Product Categories')
    ax2.set_title('10 Products with the Lowest Ratings')
    ax2.set_xlim(1, 4.5)

    for index, value in enumerate(bottom_rated_products['review_score']):
        ax2.text(value, index, f'({value:.2f})', color='black', va='center')

    st.pyplot(fig2)

    # Tabel: 10 Produk dengan Rating Terendah
    st.write("**Tabel: 10 Produk dengan Rating Terendah**")
    st.dataframe(bottom_rated_products.rename(columns={'review_score': 'Average Rating'}))

    # 📌 **Insight dari Analisis Rating Produk**
    st.subheader("Insight dari Analisis Rating Produk")
    st.write("""
    **📌 Temuan Utama:**
    - Kategori dengan rating tertinggi adalah cds_dvds_musicals dengan rata-rata rating 4.64. Kategori buku mendominasi daftar ini, seperti books_imported (4.53), books_general_interest (4.50), dan books_technical (4.40). Hal ini menunjukkan bahwa pelanggan cenderung memberikan rating tinggi untuk produk buku
    - Kategori dengan rating terendah adalah diapers_and_hygiene (3.38). Ini bisa menunjukkan adanya ketidakpuasan terhadap kualitas, daya tahan, atau ekspektasi yang tidak terpenuhi.
    - Produk yang berkaitan dengan kenyamanan rumah dan kebersihan (popok, furnitur, perlengkapan rumah) memiliki tingkat kepuasan lebih rendah, kemungkinan karena kualitas tidak sesuai ekspektasi.
    """)
# ====================== ANALISIS POLA TRANSAKSI ======================
elif menu == "Analisis Pola Transaksi":
    st.title("Analisis Pola Volume Transaksi")

    # Mengkonversi kolom order_purchase_timestamp ke datetime
    all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

    #  jumlah transaksi per hari
    daily_orders = all_df.groupby(all_df['order_purchase_timestamp'].dt.date).size().reset_index(name='order_count')

    # Visualisasi Tren Transaksi Harian
    st.subheader("Tren Volume Transaksi Harian")

    fig, ax = plt.subplots(figsize=(15, 6))
    sns.lineplot(data=daily_orders, x='order_purchase_timestamp', y='order_count', color='blue', ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Transactions')
    ax.set_title('Daily Transaction Volume Trend')

    # Format sumbu x untuk menampilkan bulan
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(fig)

    # Tabel: Jumlah Transaksi Per Hari
    st.write("**Tabel: Jumlah Transaksi Per Hari**")
    st.dataframe(daily_orders.rename(columns={'order_purchase_timestamp': 'Date', 'order_count': 'Number of Transactions'}))

    # 🔹 Ekstraksi data bulan dan hari
    all_df['month'] = all_df['order_purchase_timestamp'].dt.month
    all_df['day'] = all_df['order_purchase_timestamp'].dt.day

    # 🔹 Menghitung jumlah transaksi per kombinasi bulan & hari
    seasonal_orders = all_df.groupby(['month', 'day']).size().unstack()

    # Visualisasi Heatmap untuk Pola Musiman
    st.subheader("Pola Musiman dalam Volume Transaksi")

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.heatmap(seasonal_orders, cmap="coolwarm", linewidths=0.5, annot=False, ax=ax2)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Month')
    ax2.set_title('Seasonal Transaction Pattern Heatmap')

    st.pyplot(fig2)

    # Tabel: Jumlah Transaksi Per Bulan
    monthly_orders = all_df.groupby(all_df['order_purchase_timestamp'].dt.to_period("M")).size().reset_index(name='order_count')
    st.write("**Tabel: Jumlah Transaksi Per Bulan**")
    st.dataframe(monthly_orders.rename(columns={'order_purchase_timestamp': 'Month', 'order_count': 'Number of Transactions'}))

    # 📌 **Insight dari Analisis Pola Transaksi**
    st.subheader("Insight dari Analisis Pola Transaksi")
    st.write("""
    **📌 Temuan Utama:**
      - Volume transaksi secara umum meningkat dari awal periode hingga akhir, tetapi terdapat fluktuasi yang signifikan. Terdapat lonjakan transaksi yang sangat tinggi sekitar November 2017, yang kemungkinan besar disebabkan oleh suatu kejadian spesifik (misalnya, promo besar atau peristiwa lain).
      - Setelah lonjakan tersebut, volume transaksi kembali ke tingkat yang lebih rendah tetapi masih lebih tinggi dibandingkan periode awal.
      - Pada pola Heatmap, Mayoritas transaksi berada dalam kisaran rendah hingga sedang (diwakili oleh warna biru muda dan biru tua). Ada satu titik merah yang menandakan lonjakan transaksi sangat tinggi pada tanggal 24 bulan tertentu (kemungkinan sekitar November 2017, sesuai dengan lonjakan di grafik pertama).
      - Tidak ada tren musiman yang sangat konsisten di setiap tahun, tetapi ada peningkatan transaksi pada beberapa bulan tertentu.
    """)
    
# ====================== RFM ANALYSIS ======================
elif menu == "Analysis RFM":
    st.title("RFM Analysis - Customer Segmentation")

    # Konversi order_purchase_timestamp ke datetime
    all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

    latest_date = all_df['order_purchase_timestamp'].max()

    rfm_category = all_df.groupby('product_category_name').agg({
        'order_purchase_timestamp': lambda x: (latest_date - x.max()).days,
        'order_id': 'count',
        'payment_value': 'sum'
    }).reset_index()

    rfm_category.columns = ['Product_Category', 'Recency', 'Frequency', 'Monetary']

    # **Tabel RFM untuk Kategori Produk (Sesuai Colab)**
    st.subheader("📌 Tabel: RFM Analysis for Product Categories")
    st.dataframe(rfm_category.sort_values(by='Monetary', ascending=False))

    # **Visualisasi RFM untuk Kategori Produk (Sesuai Colab)**
    st.subheader("📌 RFM Analysis by Product Category")

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.scatterplot(
        x='Recency', 
        y='Frequency', 
        size='Monetary', 
        data=rfm_category, 
        sizes=(20, 500), 
        alpha=0.7, 
        palette='coolwarm', 
        ax=ax
    )

    ax.set_xlabel("Recency (days)", fontsize=14)
    ax.set_ylabel("Frequency (transactions)", fontsize=14)
    ax.set_title("RFM Distribution by Product Category", fontsize=16)
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

    # 📌 **Insight dari RFM Analysis**
    st.subheader("Insights & Business Strategy from RFM Analysis")
    st.write("""
    **📌 Analisis **
  - Kategori Produk dengan Penjualan & Transaksi Tertinggi Berdasarkan data, kategori "cama_mesa_banho" (produk tempat tidur, meja, dan kamar mandi) memiliki: 
  - Frequency = 11.680 (paling sering dibeli) 
  - Monetary = 1.706.355,29 (pendapatan tertinggi)
    """)


elif menu == "Customer Clustering":
    st.title("Customer Clustering")

    def categorize_product(freq):
        if freq == 1:
            return 'Low Demand'
        elif freq <= 50:
            return 'Moderate Demand'
        else:
            return 'High Demand'

    # Clustering pelanggan berdasarkan Product Category
    st.subheader("Clustering Pelanggan per Product Category")

    rfm_category = all_df.groupby('product_category_name').agg({
        'order_purchase_timestamp': lambda x: (latest_date - x.max()).days,  # Recency
        'order_id': 'count',  # Frequency
        'payment_value': 'sum'  # Monetary
    }).reset_index()

    rfm_category.rename(columns={'order_id': 'Frequency', 'payment_value': 'Monetary', 'order_purchase_timestamp': 'Recency'}, inplace=True)

    # Terapkan fungsi categorize_product untuk membuat kategori produk
    rfm_category['Product Category Group'] = rfm_category['Frequency'].apply(categorize_product)
    product_category_counts = rfm_category.groupby('Product Category Group').size()

    # Tampilkan hasil clustering per kategori produk
    st.write("**Tabel: Jumlah Produk berdasarkan Kategori**")
    st.dataframe(product_category_counts)

    # Visualisasi Clustering per Product Category
    fig, ax = plt.subplots(figsize=(10, 6))
    product_category_counts.plot(kind='bar', color=['blue', 'orange', 'green'], ax=ax)
    ax.set_xlabel("Product Category Group", fontsize=14)
    ax.set_ylabel("Number of Products", fontsize=14)
    ax.set_title("Clustering Produk berdasarkan Kategori", fontsize=16)
    st.pyplot(fig)

    # **Clustering Pelanggan**
    st.write("""
    **📌 Analisis :**
    - 59 kategori produk memiliki permintaan tinggi. 
    - 15 kategori produk memiliki permintaan sedang.
    """)

