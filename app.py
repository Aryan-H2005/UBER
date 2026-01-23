import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Uber Ride Analysis", layout="wide")

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv("uber_bookings.csv")

df = load_data()

st.title("🚗 Uber Ride Analysis Dashboard")
st.caption("Bookings • Cancellations • Revenue • Ratings")

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")

vehicle_type = st.sidebar.multiselect(
    "Vehicle Type",
    df["Vehicle Type"].dropna().unique()
)

if vehicle_type:
    df = df[df["Vehicle Type"].isin(vehicle_type)]


# -----------------------
# KPIs
# -----------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Bookings", len(df))
col2.metric("Completed Rides", (df["Booking Status"] == "Completed").sum())
col3.metric("Total Revenue", f"₹ {df['Booking Value'].sum():,.0f}")
col4.metric("Avg Ride Distance", round(df["Ride Distance"].mean(), 2))

# -----------------------
# 1. Booking Status Distribution
# -----------------------
st.subheader("📊 Booking Status Distribution")

fig_status = px.pie(
    df,
    names="Booking Status",
    title="Booking Status Breakdown"
)
st.plotly_chart(fig_status, use_container_width=True)

# -----------------------
# 2. Vehicle Type Usage
# -----------------------
st.subheader("🚙 Vehicle Type Usage")

fig_vehicle = px.bar(
    df["Vehicle Type"].value_counts().reset_index(),
    x="Vehicle Type",
    y="count",
    title="Rides by Vehicle Type"
)
st.plotly_chart(fig_vehicle, use_container_width=True)

# -----------------------
# 3. Top Pickup Locations
# -----------------------
st.subheader("📍 Top 10 Pickup Locations")

pickup_counts = df["Pickup Location"].value_counts().head(10).reset_index()
pickup_counts.columns = ["Pickup Location", "Count"]

fig_pickup = px.bar(
    pickup_counts,
    x="Pickup Location",
    y="Count",
    title="Top Pickup Locations"
)
st.plotly_chart(fig_pickup, use_container_width=True)

# -----------------------
# 4. Revenue by Vehicle Type
# -----------------------
st.subheader("💰 Revenue by Vehicle Type")

revenue_vehicle = (
    df.groupby("Vehicle Type")["Booking Value"]
    .sum()
    .reset_index()
)

fig_revenue = px.bar(
    revenue_vehicle,
    x="Vehicle Type",
    y="Booking Value",
    title="Revenue by Vehicle Type"
)
st.plotly_chart(fig_revenue, use_container_width=True)

# -----------------------
# 5. Distance vs Booking Value
# -----------------------
st.subheader("📏 Distance vs Booking Value")

fig_distance_value = px.scatter(
    df,
    x="Ride Distance",
    y="Booking Value",
    color="Vehicle Type",
    title="Ride Distance vs Booking Value"
)
st.plotly_chart(fig_distance_value, use_container_width=True)

# -----------------------
# 6. Ratings Distribution
# -----------------------
st.subheader("⭐ Ratings Distribution")

col1, col2 = st.columns(2)

with col1:
    fig_driver_rating = px.histogram(
        df,
        x="Driver Ratings",
        nbins=10,
        title="Driver Ratings"
    )
    st.plotly_chart(fig_driver_rating, use_container_width=True)

with col2:
    fig_customer_rating = px.histogram(
        df,
        x="Customer Rating",
        nbins=10,
        title="Customer Ratings"
    )
    st.plotly_chart(fig_customer_rating, use_container_width=True)

# -----------------------
# 7. Cancellation Reasons
# -----------------------
st.subheader("❌ Cancellation Reasons")

cancel_customer = df["Reason for cancelling by Customer"].dropna().value_counts().head(10)
cancel_driver = df["Driver Cancellation Reason"].dropna().value_counts().head(10)

col1, col2 = st.columns(2)

with col1:
    st.write("Customer Cancellations")
    st.bar_chart(cancel_customer)

with col2:
    st.write("Driver Cancellations")
    st.bar_chart(cancel_driver)

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.markdown("Built by Aryan | Uber Dataset | Streamlit Dashboard")
