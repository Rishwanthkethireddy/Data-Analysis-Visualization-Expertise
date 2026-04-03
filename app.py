import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# 🎨 PAGE CONFIG
# ======================
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

st.title("📊 Retail Sales Analytics Dashboard")
st.markdown("Analyze sales performance, trends, and business insights 🚀")
st.markdown("---")

# ======================
# 📂 FILE UPLOAD
# ======================
st.sidebar.header("📂 Upload Data")
file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

def find_column(columns, options):
    for col in options:
        if col in columns:
            return col
    return None

if file:
    df = pd.read_csv(file)

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # ======================
    # 🔍 COLUMN DETECTION
    # ======================
    sales_col = find_column(df.columns, ['Sales', 'sales', 'Total', 'Revenue'])
    date_col = find_column(df.columns, ['Date', 'date'])
    product_col = find_column(df.columns, ['Product', 'Item', 'Product_Line'])
    price_col = find_column(df.columns, ['price', 'Price', 'Unit_Price'])

    # ======================
    # 🎛 FILTERS
    # ======================
    st.sidebar.subheader("🎛 Filters")

    if product_col:
        selected_products = st.sidebar.multiselect(
            "Select Product",
            df[product_col].unique(),
            default=df[product_col].unique()
        )
        df = df[df[product_col].isin(selected_products)]

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        min_date = df[date_col].min()
        max_date = df[date_col].max()

        date_range = st.sidebar.date_input(
            "Select Date Range",
            [min_date, max_date]
        )

        if len(date_range) == 2:
            df = df[
                (df[date_col] >= pd.to_datetime(date_range[0])) &
                (df[date_col] <= pd.to_datetime(date_range[1]))
            ]

    # ======================
    # 💳 KPI SECTION
    # ======================
    st.subheader("💳 Key Metrics")

    if sales_col:
        total_sales = df[sales_col].sum()
        avg_sales = df[sales_col].mean()
        max_sale = df[sales_col].max()
        profit = total_sales * 0.2

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
        col2.metric("📈 Profit", f"₹{profit:,.0f}")
        col3.metric("📊 Avg Sales", f"₹{avg_sales:,.0f}")
        col4.metric("🏆 Max Sale", f"₹{max_sale:,.0f}")

    st.markdown("---")

    # ======================
    # 📈 SALES TREND
    # ======================
    if date_col and sales_col:
        trend = df.groupby(date_col)[sales_col].sum().reset_index()

        st.subheader("📈 Sales Trend")
        fig = px.line(trend, x=date_col, y=sales_col, title="Sales Over Time")
        st.plotly_chart(fig, use_container_width=True)

    # ======================
    # 📅 MONTHLY ANALYSIS
    # ======================
    if date_col and sales_col:
        df['Month'] = df[date_col].dt.to_period('M')

        monthly = df.groupby('Month')[sales_col].sum().reset_index()

        st.subheader("📅 Monthly Sales")
        st.bar_chart(monthly.set_index('Month'))

        monthly['Growth %'] = monthly[sales_col].pct_change() * 100

        st.subheader("📈 Monthly Growth %")
        st.line_chart(monthly.set_index('Month')['Growth %'])

    st.markdown("---")

    # ======================
    # 🏆 TOP PRODUCTS
    # ======================
    if product_col:
        top_products = df[product_col].value_counts().head(10)

        st.subheader("🏆 Top Products")
        st.bar_chart(top_products)

    # ======================
    # 💰 PRICE DISTRIBUTION
    # ======================
    if price_col:
        st.subheader("💰 Price Distribution")
        fig = px.histogram(df, x=price_col, nbins=30)
        st.plotly_chart(fig, use_container_width=True)

    # ======================
    # 🔥 CORRELATION
    # ======================
    numeric_df = df.select_dtypes(include='number')

    if not numeric_df.empty:
        st.subheader("🔥 Correlation Heatmap")
        fig = px.imshow(numeric_df.corr(), text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ======================
    # 🧠 CUSTOMER SEGMENTATION
    # ======================
    if 'Customer_Type' in df.columns and sales_col:
        st.subheader("🧠 Customer Segmentation")
        customer_sales = df.groupby('Customer_Type')[sales_col].sum()
        st.bar_chart(customer_sales)

    # ======================
    # 🧠 BUSINESS INSIGHTS
    # ======================
    st.subheader("🧠 Business Insights")

    if sales_col:
        st.success(f"💰 Total Revenue: ₹{total_sales:,.0f}")

    if product_col:
        top_product = df[product_col].value_counts().idxmax()
        st.info(f"🏆 Best Product: {top_product}")

        low_product = df[product_col].value_counts().idxmin()
        st.error(f"⚠️ Low Performing Product: {low_product}")

    if date_col and sales_col:
        peak_day = df.groupby(date_col)[sales_col].sum().idxmax()
        st.warning(f"📈 Peak Sales Day: {peak_day.date()}")

else:
    st.info("👆 Upload a dataset to begin")