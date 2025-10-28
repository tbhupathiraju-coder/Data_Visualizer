# Imported necessary libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Loaded the dataset
data_path = os.path.join(os.path.dirname(__file__), 'T10YIE.csv')
df = pd.read_csv(data_path)

#Inspect the data
print(df.head())
#print(df.info())

# Data Cleaning
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
plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["Rate"], color="navy", linewidth=1)
plt.title("10-Year Inflation Expectation Rate Over Time", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Inflation Expectation Rate (%)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

#Visualization - 2
#Rolling Average (90 days) vs Daily Rate
df = df.sort_values("Date").reset_index(drop=True)
df["Rolling_Mean_90"] = df["Rate"].rolling(window=90, min_periods=1).mean()
plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["Rate"], label="Daily Rate", color="lightgray", alpha=0.5)
plt.plot(df["Date"], df["Rolling_Mean_90"], label="90-Day Average", color="purple", linewidth=2)
plt.title("10-Year Inflation Expectation: Daily vs 90 Day Average")
plt.xlabel("Year")
plt.ylabel("Inflation Expectation Rate (%)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

#Visualization - 3
#Average Bar Plot by Year
df["Year"] = df["Date"].dt.year
annual_avg = df.groupby("Year")["Rate"].mean().reset_index()
plt.figure(figsize=(12,6))
sns.barplot(x="Year", y="Rate", data=annual_avg, palette="cool")
plt.title("Average Inflation Expectation Rate by Year", fontsize=16)
plt.xticks(rotation=45)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Average Rate (%)", fontsize=14)
plt.tight_layout()
plt.show()

#Visualization - 4
#Box Plot by Year
plt.figure(figsize=(12,6))
sns.boxplot(x="Year", y="Rate", data=df, palette="cool", showfliers=False)
plt.title("Distribution of Inflation Expectation Rate by Year", fontsize=16)
plt.xticks(rotation=45)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Inflation Expectation Rate(%)", fontsize=14)
plt.tight_layout()
plt.show()

#Visualization - 5
#Heatmap of Monthly Average Rates
df["Month"] = df["Date"].dt.month
monthly_avg = df.groupby(["Year", "Month"])["Rate"].mean().unstack()
plt.figure(figsize=(12,6))
sns.heatmap(monthly_avg, cmap="YlGnBu", annot=True, fmt=".2f")
plt.title("Heatmap of Monthly Average Inflation Rates", fontsize=16)
plt.xlabel("Month", fontsize=14)
plt.ylabel("Year", fontsize=14)
plt.tight_layout()
plt.show()

#Visualization - 6
#Histogram for Rate Distribution
plt.figure(figsize=(10,6))
sns.histplot(df["Rate"], bins=30, kde=True, color="teal")
plt.title("Distribution of Inflation Expectation Rates", fontsize=16)
plt.xlabel("Inflation Expectation Rate (%)", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.tight_layout()
plt.show()

#Visualization - 7
#Scatter Plot with Regression Line
df["Date_Num"] = (df["Date"] - df["Date"].min()).dt.days
plt.figure(figsize=(12,6))
sns.regplot(x="Date_Num", y="Rate", data=df, scatter_kws={"s":10})
plt.title("Scatter Plot with Regression of Inflation Rate Over Time", fontsize=16)
plt.xlabel("Days Since 2020-10-26", fontsize=14)
plt.ylabel("Inflation Expectation Rate (%)", fontsize=14)
plt.tight_layout()
plt.show()

#Visualization - 8
#Pie Chart of Average Inflation by Year
explode = [0.05]*len(annual_avg)
plt.figure(figsize=(8,8))
plt.pie(
    annual_avg["Rate"],
    labels=annual_avg["Year"],
    autopct="%1.1f%%",
    startangle=140,
    colors=plt.cm.plasma(np.linspace(0, 1, len(annual_avg))),
    explode=explode,
    wedgeprops={"edgecolor":"black", "linewidth":1.5}
)
plt.title("Proportion of Average Inflation Expectations by Year")
plt.tight_layout()
plt.show()

#Visualization - 9
#Main Trends Highlight
plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["Rate"], color="steelblue", label="T10YIE Rate", linewidth=1)
plt.fill_between(df["Date"], df["Rate"], color="lightblue", alpha=0.5)

events = {
    datetime(2022, 2, 24): "Russia-Ukraine Conflict",
    datetime(2022, 3, 15): "Fed Rate Hike",
    datetime(2022, 6, 1): "US Inflation Peaks"
}

for date, label in events.items():
    color = "red" if "Conflict" in label else "orange" if "Fed" in label else "green"
    plt.axvline(date, color=color, label=label, linestyle="--", alpha=0.7)

    rate_on_date = df.loc[df["Date"] == date, "Rate"].values
    if len(rate_on_date) > 0:
        y_pos = rate_on_date[0]
    else:
        y_pos = df["Rate"].mean()

    plt.text(date, df["Rate"].max()*0.5, label, rotation=90, color=color, fontsize=10, va="center")

plt.xlim(datetime(2022,1,1), datetime(2022,12,31))
plt.title("Inflation Expectation Over Time with Annotated Major Events", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Inflation Expectation (%)", fontsize=14)
plt.legend().set_title("Major Events")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

#Closure
print("All 9 visualizations have been generated success fully.")

#Extemes
highest_rate = df.loc[df["Rate"].idxmac()]
lowest_rate = df.loc[df["Rate"].idxmin()]
print(f"\nHighest Inflation Expectation Rate: {highest_rate['Rate']:.2f}% on {highest_rate['Date'].date()}")
print(f"Lowest Inflation Expectation Rate: {lowest_rate['Rate']:.2f}% on {lowest_rate['Date'].date()}")

#Saving the Results
output_path = os.path.join(os.path.dirname(__file__), "Yealy_Average_Inflation_Expectation.csv")
annual_avg.to_csv(output_path, index=False)
print(f"\nYearly Average Inflation Expectation Rates saved as '{output_path}")

#Cleanup
for col in ["Data_Num", "Year", "Month", "Rolling_Mean_90"]:
    df.pop(col, None)
print("\nTemporary columns removed. Data cleaning complete.")

#Citation
print("\nSource: Federal Reserve Bank of St. Louis, 10-Year Breakeven Inflation Rate [T10YIE], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/T10YIE, October 26, 2025.")

# End of Script