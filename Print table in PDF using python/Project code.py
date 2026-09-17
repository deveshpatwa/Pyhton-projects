import pandas as pd
import matplotlib.pyplot as plt

# 1. Create a sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'London', 'Paris', 'Tokyo']
}
df = pd.DataFrame(data)

# 2. Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(6, 2)) # Adjust size based on your data
ax.axis('tight')
ax.axis('off')

# 3. Create the table and add it to the plot
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')

# 4. Save the figure as a PDF file
# plt.savefig('dataframe.pdf', bbox_inches='tight')
plt.show()
plt.close()

# save table in html form
df.to_html('table.html') 
