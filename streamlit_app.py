import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Economic Trend Visualizer", layout="wide")
st.title("Economic Trend Visualizer — 10-Year Inflation Expectation (T10YIE)")

# Load data
data_path = os.path.join(os.path.dirname(__file__), 'T10YIE.csv')
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = ["Date", "Rate"]
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce")
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    df.sort_values(by="Date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

try:
    df = load_data(data_path)
except FileNotFoundError:
    st.error(f"Data file not found at {data_path}. Please add `T10YIE.csv` to the project folder.")
    st.stop()

# Sidebar
st.sidebar.header("Controls")
viz = st.sidebar.selectbox("Select visualization", [
    "Line: T10YIE Over Time",
    "Rolling Mean (90d) vs Daily",
    "Annual Average Bar",
    "Boxplot by Year",
    "Heatmap (Monthly Averages)",
    "Histogram (Rate Distribution)",
    "Violin Plot by Year",
    "Annotated Events",
    "Volatility (Std Dev)",
    "Linear Regression Trend"
])

# Common helper to render matplotlib figure in Streamlit
def render_fig(fig):
    st.pyplot(fig)
    plt.close(fig)

# Prepare some derived columns
df = df.sort_values("Date").reset_index(drop=True)
df["Year"] = df["Date"].dt.year

df["Rolling_Mean_90"] = df["Rate"].rolling(window=90, min_periods=1).mean()

annual_avg = df.groupby("Year")["Rate"].mean().reset_index()

# Visualizations
if viz == "Line: T10YIE Over Time":
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df["Date"], df["Rate"], color="navy", linewidth=1)
    ax.set_title("10-Year Inflation Expectation Rate Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Inflation Expectation Rate (%)")
    ax.grid(True, linestyle='--', alpha=0.6)
    render_fig(fig)

elif viz == "Rolling Mean (90d) vs Daily":
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df["Date"], df["Rate"], label="Daily Rate", color="lightgray", alpha=0.5)
    ax.plot(df["Date"], df["Rolling_Mean_90"], label="90-Day Average", color="purple", linewidth=2)
    ax.set_title("10-Year Inflation Expectation: Daily vs 90 Day Average")
    ax.set_xlabel("Year")
    ax.set_ylabel("Inflation Expectation Rate (%)")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    render_fig(fig)

elif viz == "Annual Average Bar":
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x="Year", y="Rate", data=annual_avg, palette="cool", ax=ax)
    ax.set_title("Average Inflation Expectation Rate by Year")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    render_fig(fig)

elif viz == "Boxplot by Year":
    fig, ax = plt.subplots(figsize=(12,6))
    sns.boxplot(x="Year", y="Rate", data=df, palette="cool", showfliers=False, ax=ax)
    ax.set_title("Distribution of Inflation Expectation Rate by Year")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    render_fig(fig)

elif viz == "Heatmap (Monthly Averages)":
    df["Month"] = df["Date"].dt.month
    monthly_avg = df.groupby(["Year", "Month"])["Rate"].mean().unstack()
    fig, ax = plt.subplots(figsize=(12,6))
    sns.heatmap(monthly_avg, cmap="YlGnBu", annot=True, fmt=".2f", ax=ax)
    ax.set_title("Heatmap of Monthly Average Inflation Rates")
    render_fig(fig)

elif viz == "Histogram (Rate Distribution)":
    fig, ax = plt.subplots(figsize=(10,6))
    sns.histplot(df["Rate"], bins=30, kde=True, color="teal", ax=ax)
    ax.set_title("Distribution of Inflation Expectation Rates")
    render_fig(fig)

elif viz == "Violin Plot by Year":
    fig, ax = plt.subplots(figsize=(12,6))
    sns.violinplot(x="Year", y="Rate", data=df, palette="viridis", inner="quartile", linewidth=1.5, ax=ax)
    ax.set_title("Violin Plot of Inflation Expectation by Year")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    render_fig(fig)

elif viz == "Annotated Events":
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df["Date"], df["Rate"], color="steelblue", label="T10YIE Rate", linewidth=1)
    ax.fill_between(df["Date"], df["Rate"], color="lightblue", alpha=0.5)

    events = {
        datetime(2020, 3, 11): "COVID-19 Pandemic Declared",
        datetime(2022, 2, 24): "Russia-Ukraine Conflict",
        datetime(2022, 3, 15): "Fed Rate Hike",
        datetime(2022, 6, 1): "US Inflation Peaks"
    }

    for date, label in events.items():
        color = "red" if "COVID" in label else "orange" if "Conflict" in label else "green" if "Hike" in label else "purple"
        ax.axvline(date, color=color, label=label, linestyle="--", alpha=0.7)
        ax.text(date, df["Rate"].max()*0.5, label, rotation=90, color=color, fontsize=10, va="center")

    ax.set_xlim(datetime(2020,1,1), datetime(2022,12,31))
    ax.set_title("Inflation Expectation Over Time with Annotated Major Events")
    ax.set_xlabel("Year")
    ax.set_ylabel("Inflation Expectation (%)")
    ax.grid(True, linestyle='--', alpha=0.6)
    render_fig(fig)

elif viz == "Volatility (Std Dev)":
    fig, ax = plt.subplots(figsize=(12,6))
    df["Volatility"] = df["Rate"].rolling(window=90, min_periods=1).std()
    ax.plot(df["Date"], df["Volatility"], color="lavender", linewidth=1.5)
    ax.fill_between(df["Date"], df["Volatility"], color="plum", alpha=0.5)
    ax.set_title("Volatility in Inflation Expectations")
    ax.set_xlabel("Year")
    ax.set_ylabel("Standard Deviation - Volatility (%)")
    ax.grid(True, linestyle='--', alpha=0.6)
    render_fig(fig)

elif viz == "Linear Regression Trend":
    df["Date_Num"] = (df["Date"] - df["Date"].min()).dt.days
    x = df["Date_Num"].values
    y = df["Rate"].values
    coeffs = np.polyfit(x, y, 1)
    slope, intercept = coeffs
    y_pred = slope * x + intercept

    fig, ax = plt.subplots(figsize=(12,6))
    ax.scatter(x, y, s=10, label = "Rates", color="steelblue", alpha=0.6)
    ax.plot(x, y_pred, color="red", linewidth=2, label=f"Trend Line: y={slope:.5f}x + {intercept:.2f}")
    ax.set_title("Scatter Plot with Linear Regression Trend Line")
    ax.set_xlabel("Days Since {}".format(df["Date"].min().date()))
    ax.set_ylabel("Inflation Expectation Rate (%)")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    render_fig(fig)

# Downloads and stats
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Yearly Average CSV")
    csv = annual_avg.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download yearly averages CSV", data=csv, file_name='Yearly_Average_Inflation_Expectation.csv', mime='text/csv')

with col2:
    st.subheader("Extremes")
    highest_rate = df.loc[df["Rate"].idxmax()]
    lowest_rate = df.loc[df["Rate"].idxmin()]
    st.write(f"Highest: {highest_rate['Rate']:.2f}% on {highest_rate['Date'].date()}")
    st.write(f"Lowest: {lowest_rate['Rate']:.2f}% on {lowest_rate['Date'].date()}")

st.markdown("\n---\n*Source: Federal Reserve Bank of St. Louis — T10YIE*")
