import streamlit as st
import pandas as pd
import plotly.express as px
import os


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Website Traffic Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# 2. LOAD CLEANED DATA
# ==========================================

DATA_FILE = r"D:\OneDrive\Desktop\web_traffic_cleaning\outputs\cleaned_website_traffic.csv"


df = pd.read_csv(DATA_FILE)

df["Date"] = pd.to_datetime(df["Date"])


# ==========================================
# 3. DASHBOARD TITLE
# ==========================================

st.title("📊 Website Traffic Analysis Dashboard")

st.markdown(
    "Interactive dashboard for analyzing website visitors, "
    "page views, traffic sources and conversions."
)


# ==========================================
# 4. SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🔎 Filters")

source_options = ["All"] + sorted(df["Source"].unique().tolist())

selected_source = st.sidebar.selectbox(
    "Traffic Source",
    source_options
)


# Apply source filter

filtered_df = df.copy()

if selected_source != "All":
    filtered_df = filtered_df[
        filtered_df["Source"] == selected_source
    ]


# ==========================================
# 5. DATE FILTER
# ==========================================

min_date = filtered_df["Date"].min().date()
max_date = filtered_df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date)
        & (filtered_df["Date"] <= end_date)
    ]


# ==========================================
# 6. KPI CALCULATIONS
# ==========================================

total_visitors = filtered_df["Visitors"].sum()

total_pageviews = filtered_df["PageViews"].sum()

total_conversions = filtered_df["Conversions"].sum()

average_bounce_rate = filtered_df["BounceRate"].mean()


# ==========================================
# 7. KPI CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Total Visitors",
    f"{total_visitors:,}"
)

col2.metric(
    "📄 Total Page Views",
    f"{total_pageviews:,}"
)

col3.metric(
    "🎯 Total Conversions",
    f"{total_conversions:,}"
)

col4.metric(
    "📉 Avg Bounce Rate",
    f"{average_bounce_rate:.2f}%"
)


st.divider()


# ==========================================
# 8. DAILY VISITORS CHART
# ==========================================

st.subheader("📈 Daily Website Visitors")

daily_chart = px.line(
    filtered_df,
    x="Date",
    y="Visitors",
    markers=True,
    title="Daily Website Visitors"
)

daily_chart.update_layout(
    xaxis_title="Date",
    yaxis_title="Visitors"
)

st.plotly_chart(
    daily_chart,
    use_container_width=True
)


# ==========================================
# 9. TRAFFIC SOURCE CHART
# ==========================================

st.subheader("🌐 Visitors by Traffic Source")

source_data = (
    filtered_df
    .groupby("Source", as_index=False)["Visitors"]
    .sum()
    .sort_values("Visitors", ascending=False)
)

source_chart = px.bar(
    source_data,
    x="Source",
    y="Visitors",
    title="Visitors by Traffic Source"
)

source_chart.update_layout(
    xaxis_title="Traffic Source",
    yaxis_title="Visitors"
)

st.plotly_chart(
    source_chart,
    use_container_width=True
)


# ==========================================
# 10. CONVERSIONS BY SOURCE
# ==========================================

st.subheader("🎯 Conversions by Traffic Source")

conversion_data = (
    filtered_df
    .groupby("Source", as_index=False)["Conversions"]
    .sum()
    .sort_values("Conversions", ascending=False)
)

conversion_chart = px.bar(
    conversion_data,
    x="Source",
    y="Conversions",
    title="Conversions by Traffic Source"
)

conversion_chart.update_layout(
    xaxis_title="Traffic Source",
    yaxis_title="Conversions"
)

st.plotly_chart(
    conversion_chart,
    use_container_width=True
)


# ==========================================
# 11. PAGE PERFORMANCE
# ==========================================

st.subheader("📄 Page Performance")

page_data = (
    filtered_df
    .groupby("Page", as_index=False)
    .agg(
        Visitors=("Visitors", "sum"),
        PageViews=("PageViews", "sum"),
        Conversions=("Conversions", "sum")
    )
    .sort_values("Visitors", ascending=False)
)

page_chart = px.bar(
    page_data,
    x="Visitors",
    y="Page",
    orientation="h",
    title="Visitors by Page"
)

page_chart.update_layout(
    xaxis_title="Visitors",
    yaxis_title="Page"
)

st.plotly_chart(
    page_chart,
    use_container_width=True
)


# ==========================================
# 12. DATA TABLE
# ==========================================

st.subheader("📋 Filtered Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.caption(
    "Website Traffic Analysis Dashboard | "
    "Created using Python, Pandas, Streamlit and Plotly"
)