import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel("global_superstore.xlsx")
df.head()

population_mean =  df['Sales'].mean()
population_mean

sns.histplot(data=df,x="Sales")
plt.title("Population hist plot")
plt.show()

data = []

for i in range(800):
    data.append(int(df.sample(35)['Sales'].mean()))

data

sns.histplot(x=data)
plt.show()

sample_mean = sum(data)/len(data)

print(population_mean)
print(sample_mean)