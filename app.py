import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("🛒 E-Commerce Sales Dashboard")

df = pd.read_csv("ecommerce_project_dataset.csv", encoding='ISO-8859-1')

# Data Cleaning
df = df.dropna(subset=['CustomerID'])
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df = df.drop_duplicates()

# Feature Engineering
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df['Month'] = df['InvoiceDate'].dt.month
df['Hour'] = df['InvoiceDate'].dt.hour

# KPIs
total_revenue = df['TotalPrice'].sum()
total_orders = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Revenue", f"{round(total_revenue,2)}")
col2.metric("📦 Orders", total_orders)
col3.metric("👥 Customers", total_customers)

st.divider()

# Monthly Sales
st.subheader("📈 Monthly Revenue")
monthly_sales = df.groupby('Month')['TotalPrice'].sum()
fig, ax = plt.subplots()
monthly_sales.plot(marker='o', ax=ax)
st.pyplot(fig)

# Top Countries
st.subheader("🌍 Top Countries")
top_countries = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
top_countries.plot(kind='bar', ax=ax)
st.pyplot(fig)

# Hourly Sales
st.subheader("⏰ Sales by Hour")
hourly_sales = df.groupby('Hour')['TotalPrice'].sum()
fig, ax = plt.subplots()
hourly_sales.plot(marker='o', ax=ax)
st.pyplot(fig)

# RFM Segmentation (FIXED)
st.subheader("🧠 Customer Segments")

latest_date = df['InvoiceDate'].max()

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (latest_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'TotalPrice': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']
rfm = rfm.dropna()

# FIXED SCORING
rfm['R_score'] = pd.qcut(rfm['Recency'].rank(method='first'), 4, labels=[4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm['M_score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 4, labels=[1,2,3,4])

rfm['Segment'] = rfm.apply(
    lambda row: 'VIP' if row['R_score']==4 and row['F_score']==4 else 'Regular',
    axis=1
)

fig, ax = plt.subplots()
rfm['Segment'].value_counts().plot(kind='bar', ax=ax)
st.pyplot(fig)

st.success("✅ Dashboard Running Successfully!")