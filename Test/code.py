import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("store.csv")

# Display basic information
print("=" * 60)
print("DATAFRAME ANALYSIS")
print("=" * 60)
print(f"\nDataFrame Shape: {df.shape}")
print(f"\nColumn Names and Types:\n{df.dtypes}")
print(f"\nFirst few rows:\n{df.head()}")
print(f"\nBasic Statistics:\n{df.describe()}")
print(f"\nMissing Values:\n{df.isnull().sum()}")

# Convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'])

print(f"\nSales Summary by Category:\n{df.groupby('category')[['sales', 'profit', 'qty']].sum()}")
print(f"\nSales Summary by Region:\n{df.groupby('region')[['sales', 'profit', 'qty']].sum()}")

# Create visualizations
plt.style.use('seaborn-v0_8-darkgrid')
fig = plt.figure(figsize=(16, 12))

# 1. Sales by Category
ax1 = plt.subplot(2, 3, 1)
category_sales = df.groupby('category')['sales'].sum().sort_values(ascending=False)
category_sales.plot(kind='bar', ax=ax1, color='skyblue', edgecolor='black')
ax1.set_title('Total Sales by Category', fontsize=12, fontweight='bold')
ax1.set_ylabel('Sales ($)')
ax1.set_xlabel('Category')
ax1.tick_params(axis='x', rotation=45)

# 2. Profit by Region
ax2 = plt.subplot(2, 3, 2)
region_profit = df.groupby('region')['profit'].sum().sort_values(ascending=False)
region_profit.plot(kind='bar', ax=ax2, color='lightcoral', edgecolor='black')
ax2.set_title('Total Profit by Region', fontsize=12, fontweight='bold')
ax2.set_ylabel('Profit ($)')
ax2.set_xlabel('Region')
ax2.tick_params(axis='x', rotation=45)

# 3. Sales Trend Over Time
ax3 = plt.subplot(2, 3, 3)
sales_by_date = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum()
sales_by_date.index = sales_by_date.index.to_timestamp()
ax3.plot(sales_by_date.index, sales_by_date.values, marker='o', linewidth=2, markersize=6, color='green')
ax3.set_title('Sales Trend Over Time', fontsize=12, fontweight='bold')
ax3.set_ylabel('Sales ($)')
ax3.set_xlabel('Date')
ax3.tick_params(axis='x', rotation=45)

# 4. Sales by Sub-Category (Top 10)
ax4 = plt.subplot(2, 3, 4)
top_subcategories = df.groupby('sub_category')['sales'].sum().sort_values(ascending=False).head(10)
top_subcategories.plot(kind='barh', ax=ax4, color='plum', edgecolor='black')
ax4.set_title('Top 10 Sub-Categories by Sales', fontsize=12, fontweight='bold')
ax4.set_xlabel('Sales ($)')

# 5. Quantity vs Profit Scatter Plot
ax5 = plt.subplot(2, 3, 5)
ax5.scatter(df['qty'], df['profit'], alpha=0.5, s=30, color='orange', edgecolors='black')
ax5.set_title('Quantity vs Profit', fontsize=12, fontweight='bold')
ax5.set_xlabel('Quantity')
ax5.set_ylabel('Profit ($)')
ax5.axhline(y=0, color='red', linestyle='--', linewidth=1)

# 6. Profit Margin by Category
ax6 = plt.subplot(2, 3, 6)
profit_margin = (df.groupby('category')['profit'].sum() / df.groupby('category')['sales'].sum() * 100).sort_values(ascending=False)
profit_margin.plot(kind='bar', ax=ax6, color='lightgreen', edgecolor='black')
ax6.set_title('Profit Margin by Category (%)', fontsize=12, fontweight='bold')
ax6.set_ylabel('Profit Margin (%)')
ax6.set_xlabel('Category')
ax6.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('store_analysis.png', dpi=300, bbox_inches='tight')
print("\n" + "=" * 60)
print("Chart saved as 'store_analysis.png'")
print("=" * 60)
plt.show()