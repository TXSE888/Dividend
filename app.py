import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
holdings = pd.read_csv("holdings.csv")
dividends = pd.read_csv("dividends.csv")

# Computations
holdings['Total Value'] = holdings['Quantity'] * holdings['Current Price']
total_value = holdings['Total Value'].sum()
annual_div = holdings['Annual Dividend'].sum()
avg_yield = (annual_div / total_value) * 100 if total_value > 0 else 0
monthly_income = annual_div / 12

# UI
st.title("📊 Dividend Dashboard")
st.metric("Portfolio Value", f"${total_value:,.2f}")
st.metric("Annual Dividends", f"${annual_div:,.2f}")
st.metric("Average Yield", f"{avg_yield:.2f}%")
st.metric("Monthly Income", f"${monthly_income:,.2f}")

# Chart
dividends['Pay Date'] = pd.to_datetime(dividends['Pay Date'])
dividends['Month'] = dividends['Pay Date'].dt.strftime('%b')
monthly_chart = dividends.groupby('Month')['Amount'].sum().reindex(
    ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
)
fig = px.bar(monthly_chart, x=monthly_chart.index, y=monthly_chart.values,
             labels={'x':'Month', 'y':'Dividends'},
             title="Monthly Dividend Income")
st.plotly_chart(fig)
