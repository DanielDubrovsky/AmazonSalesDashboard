import sqlite3

conn = sqlite3.connect('amazon.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS products')
cursor.execute('DROP TABLE IF EXISTS reviews')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    discounted_price REAL,
    actual_price REAL,
    discount_percentage REAL,
    rating REAL,
    rating_count INTEGER,
    about_product TEXT,
    img_link TEXT,
    product_link TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    review_id TEXT PRIMARY KEY,
    product_id TEXT,
    user_id TEXT,
    user_name TEXT,
    review_title TEXT,
    review_content TEXT,
    FOREIGN KEY (product_id) REFERENCES products (product_id)
)
''')

conn.commit()
conn.close()