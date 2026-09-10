import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

df = pd.read_excel("coffeeshop_sales.xlsx")
conn = sqlite3.connect(":memory:")
df.to_sql("sales", conn, index=False)

query = '''
SELECT
    Branch,
    Promotion,
    COUNT(*) AS Transactions,
    SUM(Revenue) AS TotalRevenue,
    ROUND(AVG(Revenue), 2) AS AvgRevenuePerTransaction
FROM sales
GROUP BY Branch, Promotion
ORDER BY Branch, Promotion;
'''

result = pd.read_sql(query, conn)
pivot = result.pivot(index="Branch", columns="Promotion", values="AvgRevenuePerTransaction")
pivot.columns = ["No Promotion", "With Promotion"]
pivot["Difference"] = pivot["With Promotion"] - pivot["No Promotion"]
print(pivot)

ax = pivot[["No Promotion", "With Promotion"]].plot(
    kind="bar", figsize=(8,5), color=["#4C72B0", "#DD8452"]
)
ax.set_ylabel("Average Revenue per Transaction (PHP)")
ax.set_title("Average Transaction Value: Promotion vs. No Promotion, by Branch")
ax.set_xticklabels(pivot.index, rotation=20)
plt.tight_layout()
plt.savefig("promo_comparison.png", dpi=150)
plt.show()