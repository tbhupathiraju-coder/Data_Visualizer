# Imported necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Loaded the dataset
df = pd.read_csv('T10YIE.csv')

#Inspect the data
print(df.head())
print(df.info())

# Data Cleaning
#Renaming the columns
df.columns = ["Date", "Rate"]
#Converting the date column to datatime format (mm/dd/yyyy)
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%y")
#Missing Values
df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce")
#Removing Duplicates
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
#Sorting the data by date
df.sort_values(by="Date", inplace=True)


