import matplotlib.pyplot as plt
import numpy as np

# 1. Generate 3D surface data
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# 2. Initialize 3D axis
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# 3. Plot 3D surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis')
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

ax.set_title("3D Surface Plot")
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")

plt.show()




# using plotly -------------------->

import plotly.express as px
import pandas as pd

# 1. Prepare sample 3D data
df = px.data.iris()

# 2. Create interactive 3D scatter plot
fig = px.scatter_3d(
    df, 
    x='sepal_length', 
    y='sepal_width', 
    z='petal_width',
    color='species',
    title="3D Iris Scatter Plot"
)

# 3. Show plot
fig.show()