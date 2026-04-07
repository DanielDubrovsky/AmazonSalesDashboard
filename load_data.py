import sqlite3
import pandas as pd

# --------------------------
# Step 1: Load CSV
# --------------------------
df = pd.read_csv('amazon.csv')
df.columns = df.columns.str.strip()  # remove spaces from headers

# --------------------------
# Step 2: Clean numeric columns
# --------------------------
def clean_numeric(col, is_percentage=False):
    # Remove currency symbols, commas, % signs, etc.
    cleaned = df[col].astype(str).str.replace(r'[^0-9.]', '', regex=True)
    return pd.to_numeric(cleaned, errors='coerce')

numeric_cols = ['discounted_price', 'actual_price', 'discount_percentage', 'rating_count', 'rating']

df['discounted_price'] = clean_numeric('discounted_price')
df['actual_price'] = clean_numeric('actual_price')
df['discount_percentage'] = clean_numeric('discount_percentage', is_percentage=True)
df['rating_count'] = clean_numeric('rating_count')
df['rating'] = clean_numeric('rating')

# Replace NaN with None for SQLite
df[numeric_cols] = df[numeric_cols].where(pd.notnull(df[numeric_cols]), None)

# --------------------------
# Step 3: Connect to SQLite
# --------------------------
conn = sqlite3.connect('amazon.db')
cursor = conn.cursor()

# --------------------------
# Step 4: Clear old rows
# --------------------------
cursor.execute("DELETE FROM products")
cursor.execute("DELETE FROM reviews")
conn.commit()

# --------------------------
# Step 5: Insert products
# --------------------------
products = df[[
    'product_id', 'product_name', 'category', 'discounted_price', 'actual_price',
    'discount_percentage', 'rating', 'rating_count', 'about_product',
    'img_link', 'product_link'  
]].drop_duplicates(subset=['product_id'])

cursor.executemany('''
INSERT INTO products (
    product_id, product_name, category, discounted_price, actual_price,
    discount_percentage, rating, rating_count, about_product, img_link, product_link
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', products.values.tolist())

# --------------------------
# Step 6: Insert reviews
# --------------------------
reviews = df[[
    'review_id', 'product_id', 'user_id', 'user_name', 'review_title', 'review_content'
]].drop_duplicates(subset=['review_id'])

# Convert all review columns to string and replace NaN
reviews = reviews.astype(str).replace({'nan': None})

cursor.executemany('''
INSERT INTO reviews (
    review_id, product_id, user_id, user_name, review_title, review_content
) VALUES (?, ?, ?, ?, ?, ?)
''', reviews.values.tolist())

# --------------------------
# Step 7: Commit and close
# --------------------------
conn.commit()
conn.close()

print('Data cleared and re-loaded successfully!')