import pandas as pd
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
print(result)