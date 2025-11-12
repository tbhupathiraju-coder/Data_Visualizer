#This project analyzes and visualizes the 10 Year Inflation Expectation Rate (T10YIE) using data from the Federal Reserve Bank of St. Louis
#It includes data cleaning, compares averages, and generates 11 different visualizations to illustrate economic trends over time.
#Some of the graphs include line plots, bar charts, box plots, heatmaps, histograms, violin plots, pie charts, and regression analysis to show trends in multiple ways. 
# It also highlights major ecnonomic events! 

# Imported necessary libraries
import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Economic Trend Visualization")
st.title("Economic Trend Visualization")
st.markdown("Explores different trends in inflation, averages, and economic events during previous years")

# Loaded the dataset
data_path = os.path.join(os.path.dirname(__file__), 'T10YIE.csv')
df = pd.read_csv(data_path)

print("Welcome to the Economic Trend Visualizer. This project visualizes the 10-Year Inflation Expectation Rate (T10YIE) using data from the Federal Reserve Bank of St. Louis.")
print("Explores trends, cleans data, and points out major economic events")
print("Gain insights into inflation expectations over time through informative visualizations")


#Inspect the data
print(df.head())
#print(df.info())

# Data Cleaning
#Minimal AI assistance
#Renaming the columns
df.columns = ["Date", "Rate"]
#Converting the date column to datatime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
#Missing Values
df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce")
#Removing Duplicates
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
#Sorting the data by date
df.sort_values(by="Date", inplace=True)
#Sequential Indexing
df.reset_index(drop=True, inplace=True)
#print(df.info())

#Statistical Summary
#print("Statistical Summary")
#print(df.describe())

#Data Visualizations
#Visualization - 1
#Line plot of Inflation Expectation Rate over time
#plt.figure(figsize=(12,6))
#plt.plot(df["Date"], df["Rate"], color="navy", linewidth=1)
#plt.title("10-Year Inflation Expectation Rate Over Time", fontsize=16)
#plt.xlabel("Year", fontsize=14)
#plt.ylabel("Inflation Expectation Rate (%)", fontsize=14)
#plt.grid(True, linestyle='--', alpha=0.6)
#plt.tight_layout()
#plt.show()

st.subheader("10-Year Inflation Expectation Rate Over Time")
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(df["Date"], df["Rate"], color="navy", linewidth=1)
ax.set_title("10-Year Inflation Expectation Rate Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Inflation Expectation Rate (%)")
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

#Visualization - 2
#Rolling Average (90 days) vs Daily Rate
#Used https://youtube.com/shorts/OCNbHw4kDco?si=xqSk7qFHUcb0oPL0 - though about using the df[].rolling
#df = df.sort_values("Date").reset_index(drop=True)
#df["Rolling_Mean_90"] = df["Rate"].rolling(window=90, min_periods=1).mean()
#plt.figure(figsize=(12,6))
#plt.plot(df["Date"], df["Rate"], label="Daily Rate", color="lightgray", alpha=0.5)
#plt.plot(df["Date"], df["Rolling_Mean_90"], label="90-Day Average", color="purple", linewidth=2)plt.title("10-Year Inflation Expectation: Daily vs 90 Day Average")
#plt.xlabel("Year")
#plt.ylabel("Inflation Expectation Rate (%)")
#plt.legend()
#plt.grid(True, linestyle='--', alpha=0.6)
#plt.tight_layout()
#plt.show()

st.subheader("10-Year Inflation Expectation: Daily vs 90 Day Average")
df["Rolling_Mean_90"] = df["Rate"].rolling(window=90, min_periods=1).mean()
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(df["Date"], df["Rate"], label="Daily Rate", color="lightgray", alpha=0.5)
ax.plot(df["Date"], df["Rolling_Mean_90"], label="90-Day Average", color="purple", linewidth=2)
ax.set_xlabel("Year")
ax.set_ylabel("Inflation Expectation Rate (%)")
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

#Visualization - 3
#Average Bar Plot by Year
#df["Year"] = df["Date"].dt.year
#annual_avg = df.groupby("Year")["Rate"].mean().reset_index()
#plt.figure(figsize=(12,6))
#sns.barplot(x="Year", y="Rate", data=annual_avg, palette="cool")
#plt.title("Average Inflation Expectation Rate by Year", fontsize=16)
#plt.xticks(rotation=45)
#plt.xlabel("Year", fontsize=14)
#plt.ylabel("Average Rate (%)", fontsize=14)
#plt.tight_layout()
#plt.show()

st.subheader("Average Inflation Expectation Rate by Year")
df["Year"] = df["Date"].dt.year
annual_avg = df.groupby("Year")["Rate"].mean().reset_index()
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x="Year", y="Rate", data=annual_avg, palette="cool", ax=ax)
plt.xticks(rotation=45)
ax.set_title("Average Inflation Expectation Rate by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Average Rate (%)")
st.pyplot(fig)


#Visualization - 4
#Box Plot by Year
#Used https://youtu.be/MmApBcxSgMk?si=5ysE_IfStKIp43yU to help make graph on box plot code
#plt.figure(figsize=(12,6))
#sns.boxplot(x="Year", y="Rate", data=df, palette="cool", showfliers=False)
#plt.title("Distribution of Inflation Expectation Rate by Year", fontsize=16)
#plt.xticks(rotation=45)
#plt.xlabel("Year", fontsize=14)
#plt.ylabel("Inflation Expectation Rate(%)", fontsize=14)
#plt.tight_layout()
#plt.show()

st.subheader("Distribution of Inflation Expectation Rate by Year")
fig, ax = plt.subplots(figsize=(12,6))
sns.boxplot(x="Year", y="Rate", data=df, palette="cool", showfliers=False, ax=ax)
ax.set_title("Distribution of Inflation Expectation Rate by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Inflation Expectation Rate (%)")
plt.xticks(rotation=45)
st.pyplot(fig)

#Visualization - 5
#Heatmap of Monthly Average Rates
# Used https://youtube.com/shorts/PlSP8jPsrXc?si=haWb85ZnQ6DYhr6C as a starting reference on the heatmap code
#df["Month"] = df["Date"].dt.month
#monthly_avg = df.groupby(["Year", "Month"])["Rate"].mean().unstack()
#plt.figure(figsize=(12,6))
#sns.heatmap(monthly_avg, cmap="YlGnBu", annot=True, fmt=".2f")
#plt.title("Heatmap of Monthly Average Inflation Rates", fontsize=16)
#plt.xlabel("Month", fontsize=14)
#plt.ylabel("Year", fontsize=14)
#plt.tight_layout()
#plt.show()

st.subheader("Heatmap of Monthly Average Inflation Rates")
df["Month"] = df["Date"].dt.month
monthly_avg = df.groupby(["Year", "Month"])["Rate"].mean().unstack()
fig, ax = plt.subplots(figsize=(12,6))
sns.heatmap(monthly_avg, cmap="YlGnBu", annot=True, fmt=".2f", ax=ax)
ax.set_title("Heatmap of Monthly Average Inflation Rates")
ax.set_xlabel("Month")
ax.set_ylabel("Year")
st.pyplot(fig)

#Visualization - 6
#Histogram for Rate Distribution
#plt.figure(figsize=(10,6))
#sns.histplot(df["Rate"], bins=30, kde=True, color="teal")
#plt.title("Distribution of Inflation Expectation Rates", fontsize=16)
#plt.xlabel("Inflation Expectation Rate (%)", fontsize=14)
#plt.ylabel("Frequency", fontsize=14)
#plt.tight_layout()
#plt.show()

st.subheader("Distribution of Inflation Expectation Rates")
fig, ax = plt.subplots(figsize=(10,6))
sns.histplot(df["Rate"], bins=30, kde=True, color="teal", ax=ax)
ax.set_title("Distribution of Inflation Expectation Rates")
ax.set_xlabel("Inflation Expectation Rate (%)")
ax.set_ylabel("Frequency")
st.pyplot(fig)

#Visualization - 7
#Violin Plot of Inflation Expectation by Year
#Used https://youtube.com/shorts/-mxp1wLBWgo?si=xOIckBoO18A_DTlL for the sns.violinplot part
#plt.figure(figsize=(12,6))
#sns.violinplot(x="Year", y="Rate", data=df, palette="viridis", inner="quartile", linewidth=1.5)
#plt.title("Violin Plot of Inflation Expectation by Year", fontsize=16)
#plt.xlabel("Year", fontsize=14)
#plt.ylabel("Inflation Expectation Rate (%)", fontsize=14)
#plt.xticks(rotation=45)
#plt.tight_layout()
#plt.show()

st.subheader("Violin Plot of Inflation Expectation by Year")
fig, ax = plt.subplots(figsize=(12,6))
sns.violinplot(x="Year", y="Rate", data=df, palette="viridis", inner="quartile", linewidth=1.5, ax=ax)
plt.xticks(rotation=45)
ax.set_title("Violin Plot of Inflation Expectation by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Inflation Expectation Rate (%)")
st.pyplot(fig)

#Visualization - 8
#Pie Chart of Average Inflation by Year
#Used https://youtu.be/MPiz50TsyF0?si=i-OcrfoK7xtaEunw for a tutorial on Matplotlib for Pie Charts
#explode = [0.05]*len(annual_avg)
#plt.figure(figsize=(8,8))
#plt.pie(
#    annual_avg["Rate"],
#    labels=annual_avg["Year"],
#    autopct="%1.1f%%",
#    startangle=140,
#    colors=plt.cm.plasma(np.linspace(0, 1, len(annual_avg))),
#    explode=explode,
#    wedgeprops={"edgecolor":"black", "linewidth":1.5}
#)
#plt.title("Proportion of Average Inflation Expectations by Year")
#plt.tight_layout()
#plt.show()

st.subheader("Proportion of Average Inflation Expectations by Year")
explode = [0.05]*len(annual_avg)
fig, ax = plt.subplots(figsize=(8,8))
ax.pie(
    annual_avg["Rate"],
    labels=annual_avg["Year"],
    autopct="%1.1f%%",
    startangle=140,
    colors=plt.cm.plasma(np.linspace(0, 1, len(annual_avg))),
    explode=explode,
    wedgeprops={"edgecolor":"black", "linewidth":1.5}
)
ax.set_title("Proportion of Average Inflation Expectations by Year")
st.pyplot(fig)

#Visualization - 9
#Main Trends Highlight
#plt.figure(figsize=(12,6))
#plt.plot(df["Date"], df["Rate"], color="steelblue", label="T10YIE Rate", linewidth=1)
#plt.fill_between(df["Date"], df["Rate"], color="lightblue", alpha=0.5)

#events = {
#    datetime(2020, 3, 11): "COVID-19 Pandemic Declared",
#    datetime(2022, 2, 24): "Russia-Ukraine Conflict",
#    datetime(2022, 3, 15): "Fed Rate Hike",
#    datetime(2022, 6, 1): "US Inflation Peaks"
#}

st.subheader("Inflation Trends with Major Economic Events")
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(df["Date"], df["Rate"], color="steelblue", label="T10YIE Rate", linewidth=1)
ax.fill_between(df["Date"], df["Rate"], color="lightblue", alpha=0.5)

events = {
    datetime(2020, 3, 11): "COVID-19 Pandemic Declared",
    datetime(2022, 2, 24): "Russia-Ukraine Conflict",
    datetime(2022, 3, 15): "Fed Rate Hike",
    datetime(2022, 6, 1): "US Inflation Peaks"
}

#Minimal AI assistance in the for loop
for date, label in events.items():
    color = "red" if "COVID" in label else "orange" if "Conflict" in label else "green" if "Hike" in label else "purple"
    ax.axvline(date, color=color, label=label, linestyle="--", alpha=0.7)

    rate_on_date = df.loc[df["Date"] == date, "Rate"].values
    if len(rate_on_date) > 0:
        y_pos = rate_on_date[0]
    else:
        y_pos = df["Rate"].mean()

    ax.text(date, df["Rate"].max()*0.5, label, rotation=90, color=color, fontsize=10, va="center")

#plt.xlim(datetime(2020,1,1), datetime(2022,12,31))
#plt.title("Inflation Expectation Over Time with Annotated Major Events", fontsize=16)
#plt.xlabel("Year", fontsize=14)
#plt.ylabel("Inflation Expectation (%)", fontsize=14)
#plt.legend().set_title("Major Events")
#plt.grid(True, linestyle='--', alpha=0.6)
#plt.tight_layout()
#plt.show()


ax.legend()
ax.set_title("Inflation Expectation Over Time with Annotated Major Events")
ax.set_xlabel("Year")
ax.set_ylabel("Inflation Expectation Rate (%)")
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)


#Visualization - 10
#Standard Deviation Over Time
#plt.figure(figsize=(12,6))
#df["Volatility"] = df["Rate"].rolling(window=90, min_periods=1).std()
#plt.plot(df["Date"], df["Volatility"], color="lavender", linewidth=1.5)
#plt.fill_between(df["Date"], df["Volatility"], color="plum", alpha=0.5)
#plt.title("Volatility in Inflation Expectations", fontsize=16)
#plt.xlabel("Year", fontsize=14)
#plt.ylabel("Standard Deviation - Volatility (%)", fontsize=14)
#plt.grid(True, linestyle='--', alpha=0.6)
#plt.tight_layout()
#plt.show()

st.subheader("Volatility in Inflation Expectations")
df["Volatility"] = df["Rate"].rolling(window=90, min_periods=1).std()
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(df["Date"], df["Volatility"], color="plum", linewidth=1.5)
ax.fill_between(df["Date"], df["Volatility"], color="lavender", alpha=0.5)
ax.set_title("Volatility in Inflation Expectations")
ax.set_xlabel("Year")
ax.set_ylabel("Standard Deviation - Volatility (%)")
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

#Visualization - 11
#Forecasting Future Trends w/ Linear Regression
#df["Date_Num"] = (df["Date"] - df["Date"].min()).dt.days
#x = df["Date_Num"].values
#y = df["Rate"].values

#coeffs = np.polyfit(x, y, 1)
#slope, intercept = coeffs
#y_pred = slope * x + intercept

#plt.figure(figsize=(12,6))
#plt.scatter(x, y, s=10, label = "Rates", color="steelblue", alpha=0.6)
#plt.plot(x, y_pred, color="red", linewidth=2, label=f"Trend Line: y={slope:.5f}x + {intercept:.2f}")
#plt.title("Scatter Plot with Linear Regression Trend Line", fontsize=16)
#plt.xlabel("Days Since 2015-10-26", fontsize=14)
#plt.ylabel("Inflation Expectation Rate (%)", fontsize=14)
#plt.legend()
#plt.grid(True, linestyle='--', alpha=0.6)
#plt.tight_layout()
#plt.show()

st.subheader("Scatter Plot with Linear Regression Trend Line")
df["Date_Num"] = (df["Date"] - df["Date"].min()).dt.days
x = df["Date_Num"].values
y = df["Rate"].values
slope, intercept = np.polyfit(x, y, 1)
y_pred = slope * x + intercept
fig, ax = plt.subplots(figsize=(12,6))
ax.scatter(x, y, s=10, label="Rates", color="steelblue", alpha=0.6)
ax.plot(x, y_pred, color="red", linewidth=2, label=f"Trend Line: y={slope:.5f}x + {intercept:.2f}")
ax.set_title("Scatter Plot with Linear Regression Trend Line")
ax.set_xlabel("Days Since 2015-10-26")
ax.set_ylabel("Inflation Expectation Rate (%)")
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
st.pyplot(fig)


#Closure
ax.close('all')
st.success("All 11 visualizations have been generated successfully.")

#Extremes
st.subheader("Stats")
highest_rate = df.loc[df["Rate"].idxmax()]
lowest_rate = df.loc[df["Rate"].idxmin()]
st.write(f"\nHighest Inflation Expectation Rate: {highest_rate['Rate']:.2f}% on {highest_rate['Date'].date()}")
st.write(f"Lowest Inflation Expectation Rate: {lowest_rate['Rate']:.2f}% on {lowest_rate['Date'].date()}")

#Saving the Results
output_path = os.path.join(os.path.dirname(__file__), "Yearly_Average_Inflation_Expectation.csv")
annual_avg.to_csv(output_path, index=False)
print(f"\nYearly Average Inflation Expectation Rates saved as '{output_path}'")

#Cleanup
#Minimal AI assistance in the debugging portion here
for col in ["Date_Num", "Year", "Month", "Rolling_Mean_90"]:
    if col in df.columns:
        df.pop(col)
print("\nTemporary columns removed. Data cleaning complete.")

#Citation
print("\nSource: Federal Reserve Bank of St. Louis, 10-Year Breakeven Inflation Rate [T10YIE], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/T10YIE, October 26, 2025.")

# End of Script

#Disclaimer on timing:
#This project took longer than expeted as it was my first time creating multiple Python visualizations at this scope. 
#Debugging syntax errors, re-importing and cleaning the 10-year dataset (after mistakenly using a 5-hour one), adjusting code, and adding 2 more visualizations for insight extended the time.
#Overall, I spent 11+ hours coding, debugging, and learning how to create meaningful graphs using Mathplotlib and Seaborn. Despite the challenges, it was a valuable learning experience and I'm pleased with the final results.

#Additional Note:
#I used minimul AI tools to help in the startup/little bit in the end code as I am new to Python coding. Most of it was my own work and researching, after getting a sense and guideline from the starting code snippets.
