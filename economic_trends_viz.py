# Imported necessary libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Loaded the dataset
data_path = os.path.join(os.path.dirname(__file__), 'T10YIE.csv')
df = pd.read_csv(data_path)

#Inspect the data
print(df.head())
print(df.info())

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
print(df.info())

#Statistical Summary
print("Statistical Summary")
print(df.describe())

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
sns.boxplot(x="Year", y="Rate", hue="Year", data=annual_avg, palette="cool", legend=False)
plt.title("Distribution of Inflation Expectation Rate by Year", fontsize=16)
plt.xticks(rotation=45)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Inflation Expectation Raten(%)", fontsize=14)
plt.tight_layout()
plt.show()

#Visualization - 5
#Heatmap of Monthly Average Rates
df["Month"] = df["Date"].dt.month
monthly_avg = df.groupby(["Year", "Month"])["Rate"].mean().unstack()
plt.figure(figsize=(12,6))
sns.heatmap(monthly_avg, cmap="YlGnBu", annot=False)
plt.title("Heatmap of Monthly Average Inflation Rates", fontsize=16)
plt.xlabel("Month", fontsize=14)
plt.ylabel("Year", fontsize=14)
plt.tight_layout()
plt.show()

#Visualization - 6
#Histogram for Rate Distribution
plt.figure(figsize=(10,6))
sns.histoplot(df["Rate"], bins=30, kde=True, color="teal")
plt.title("Distribution of Inflation Expectation Rates", fontsize=16)
plt.xlabel("Inflation Expectation Rate (%)", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.tight_layout()
plt.show()

#Visualization - 7
#Scatter Plot with Regression Line
plt.figure(figsize=(12,6))
sns.regplot(x="Date", y="Rate", data=df, scatter_kws={"s":10})
plt.title("Scatter Plot with Regression of Inflation Rate Over Time", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Inflation Expectation Rate (%)", fontsize=14)
plt.tight_layout()
plt.show()

#Visualization - 8
#Pie Chart of Average Inflation by Year
plt.figure(figsize=(8,8))
plt.pie(
    annual_avg["Rate"],
    labels=annual_avg["Year"],
    autopct="%1.1f%%",
    startangle=140,
    colors=plt.cm.plasma(np.linespace(0, 1, len(annual_avg)))
)
plt.title("Proportion of Average Inflation Expectations by Year")
plt.tight_layout()
plt.show()

#Visualization - 9
#Main Trends Highlight
plt.figure(figsize=(12,6))


