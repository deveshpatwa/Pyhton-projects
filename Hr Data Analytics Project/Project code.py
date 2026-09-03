# get the data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("HR Analytics.csv")
df.head()
# know about your data
df.info()
df.describe().round(1).T
df.shape
df.columns
df.isnull().sum()

# analyse data using EDA or use chatgpt to generate questions
data =  df['Gender'].value_counts() / df['Gender'].count() * 100
data.plot(kind='bar')
plt.title('Gender Distribution in percentage')
plt.xlabel('Gender')
plt.ylabel('Percentage %')
plt.savefig('Gender Distribution.png')

df.columns
df['Attrition'].value_counts()

df.pivot_table(
    index='Department',
    columns='Gender',
    values='EmployeeID',
    aggfunc='count'
).plot(kind='bar', stacked=True)
plt.show()




