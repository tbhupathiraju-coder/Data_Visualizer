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

