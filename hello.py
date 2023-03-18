

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read in data
df = pd.read_csv('stock_data.csv')

# Get best performing stocks
best_stocks = df.sort_values(by='returns', ascending=False).head(10)

# Plot best performing stocks using seaborn
sns.barplot(x='stock', y='returns', data=best_stocks, palette='Blues_d')
plt.title('Best Performing Stocks')
plt.xlabel('Stock')
plt.ylabel('Returns')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()