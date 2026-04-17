import sqlite3
import pandas as pd

# Load CSV into DataFrame
df = pd.read_csv('amazon.csv')
df.columns = df.columns.str.strip()  # remove spaces from headers

# Clean Numeric Columns
def clean_numeric(col, is_percentage=False):
    # Remove currency symbols, commas, % signs, etc.
    cleaned = df[col].astype(str).str.replace(r'[^0-9.]', '', regex=True)
    return pd.to_numeric(cleaned, errors='coerce')


numeric_cols = ['discounted_price', 'actual_price', 'discount_percentage', 'rating_count', 'rating']

df['discounted_price'] = clean_numeric('discounted_price') / 100
df['actual_price'] = clean_numeric('actual_price') / 100
df['discount_percentage'] = clean_numeric('discount_percentage', is_percentage=True)
df['rating_count'] = clean_numeric('rating_count')
df['rating'] = clean_numeric('rating')
# Calling clean_numeric on numeric columns

# Replace NaN with None for SQLite
df[numeric_cols] = df[numeric_cols].where(pd.notnull(df[numeric_cols]), None)

# Connect to SQLite and insert data
conn = sqlite3.connect('amazon.db')
cursor = conn.cursor()

# Clear the exisiting data prior to inserting new data
cursor.execute("DELETE FROM products")
cursor.execute("DELETE FROM reviews")
conn.commit()

# Products table dataframe for inserting to sqlite db
products = df[[
    'product_id', 'product_name', 'category', 'discounted_price', 'actual_price',
    'discount_percentage', 'rating', 'rating_count', 'about_product',
    'img_link', 'product_link'  
]].drop_duplicates(subset=['product_id'])

# Insert products into the database
cursor.executemany('''
INSERT INTO products (
    product_id, product_name, category, discounted_price, actual_price,
    discount_percentage, rating, rating_count, about_product, img_link, product_link
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', products.values.tolist())

# Reviews table dataframe for inserting to sqlite db
reviews = df[[
    'review_id', 'product_id', 'user_id', 'user_name', 'review_title', 'review_content'
]].drop_duplicates(subset=['review_id'])

# Convert all review columns to string and replace NaN
reviews = reviews.astype(str).replace({'nan': None})

# Inswert reviews into the database
cursor.executemany('''
INSERT INTO reviews (
    review_id, product_id, user_id, user_name, review_title, review_content
) VALUES (?, ?, ?, ?, ?, ?)
''', reviews.values.tolist())

# Commit changes and close connection
conn.commit()
conn.close()

print('Data cleared and re-loaded successfully!')