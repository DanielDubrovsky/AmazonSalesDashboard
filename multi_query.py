import sqlite3

def get_connection():
    conn = sqlite3.connect('amazon.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_top_rated_products(min_reviews=50, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT product_name, rating, rating_count
    from products
    WHERE rating_count >= ?
    ORDER BY rating DESC, rating_count DESC
    LIMIT ?
    '''

    results = cursor.execute(query, (min_reviews, limit)).fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_most_reviewed_products(limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT product_name, rating_count
    FROM products
    ORDER BY rating_count DESC
    LIMIT ?
    '''

    results = cursor.execute(query, (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_discounted_products(min_discount=20, limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT product_name, actual_price, discount_percentage
    FROM products
    WHERE discount_percentage >= ?
    ORDER BY discount_percentage DESC
    LIMIT ?
    '''

    results = cursor.execute(query, (min_discount, limit)).fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_category_avg_ratings(category):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT AVG(rating) as avg_rating
    FROM products
    WHERE category = ?
    '''

    result = cursor.execute(query, (category,)).fetchone()
    conn.close()
    return result['avg_rating'] if result else None

def get_category_top_discounted_products(category, min_discount=20, limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT product_name, actual_price, discount_percentage
    FROM products
    WHERE category = ? AND discount_percentage >= ?
    ORDER BY discount_percentage DESC
    LIMIT ?
    '''

    results = cursor.execute(query, (category, min_discount, limit)).fetchall()
    conn.close()
    return [dict(row) for row in results]

def search_reviews(keyword, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT review_content, rating
    FROM reviews
    WHERE review_content LIKE ?
    LIMIT ?
    '''

    results = cursor.execute(query, (f'%{keyword}%', limit)).fetchall()
    conn.close()
    return [dict(row) for row in results]

def search_products(keyword, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT product_name, actual_price, rating
    FROM products
    WHERE product_name LIKE ?
    ORDER BY rating DESC
    LIMIT ?
    '''

    results = cursor.execute(query, (f'%{keyword}%', limit)).fetchall()
    conn.close()
    return [dict(row) for row in results]

def filtered_products(category=None, min_price=None, max_price=None, min_rating=None, limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    query = '''SELECT product_name, actual_price, rating FROM products WHERE 1=1'''
    params = []

    if category:
        query += ' AND category = ?'
        params.append(category)

    if min_price is not None:
        query += ' AND actual_price >= ?'
        params.append(min_price)

    if max_price is not None:
        query += ' AND actual_price <= ?'
        params.append(max_price)
    
    if min_rating is not None:
        query += ' AND rating >= ?'
        params.append(min_rating)
    
    query += ' ORDER BY rating DESC LIMIT ?'
    params.append(limit)

    results = cursor.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in results]

def weighted_rating(min_reviews=50, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT product_name, rating, rating_count,
        (rating * rating_count) / (rating_count + ?) AS weighted_rating
    FROM products
    WHERE rating_count >= ?
    ORDER BY weighted_rating DESC
    LIMIT ?
    '''

    results = cursor.execute(query, (min_reviews, min_reviews, limit)).fetchall()
    conn.close()
    return [dict(row) for row in results]

def similar_products(product_id, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT p2.product_name, p2.actual_price, p2.rating
    FROM products p1
    JOIN products p2 
        ON p1.category = p2.category 
        AND p1.product_id != p2.product_id
    WHERE p1.product_id = ?
    LIMIT ?
    '''

    results = cursor.execute(query, (product_id, limit)).fetchall()
    conn.close()
    return [dict(row) for row in results]
    
def get_total_products():
    conn = get_connection()
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) as total FROM products'
    result = cursor.execute(query).fetchone()
    conn.close()
    return result['total'] if result else 0

def get_avg_rating():
    conn = get_connection()
    cursor = conn.cursor()
    query = 'SELECT AVG(rating) as avg_rating FROM products'
    result = cursor.execute(query).fetchone()
    conn.close()
    return result['avg_rating'] if result else None

def get_avg_discount():
    conn = get_connection()
    cursor = conn.cursor()
    query = 'SELECT AVG(discount_percentage) as avg_discount FROM products'
    result = cursor.execute(query).fetchone()
    conn.close()
    return result['avg_discount'] if result else None

