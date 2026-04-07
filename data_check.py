import sqlite3

conn = sqlite3.connect("amazon.db")
cursor = conn.cursor()

# Count rows
cursor.execute("SELECT COUNT(*) FROM products")
print("Products:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM reviews")
print("Reviews:", cursor.fetchone()[0])

# Sample data
cursor.execute("SELECT product_name, discounted_price, actual_price, discount_percentage, rating_count FROM products LIMIT 5")
for row in cursor.fetchall():
    print(row)

conn.close()