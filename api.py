from flask import Flask, render_template, render_template, request, jsonify, send_from_directory
import multi_query
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/products/top-rated')
def top_rated_products():
    min_reviews = request.args.get('min_reviews', default=50, type=int)
    limit = request.args.get('limit', default=10, type=int)

    data = multi_query.get_top_rated_products(min_reviews, limit)
    return jsonify(data)

@app.route('/products/most-reviewed')
def most_reviewed_products():
    limit = request.args.get('limit', default=10, type=int)

    data = multi_query.get_most_reviewed_products(limit)
    return jsonify(data)

@app.route('/products/discounted')
def discounted_products():
    min_discount = request.args.get('min_discount', default=20, type=int)
    limit = request.args.get('limit', default=10, type=int)

    data = multi_query.get_discounted_products(min_discount, limit)
    return jsonify(data)

@app.route('/products/category/avg-rating')
def category_avg_ratings():
    category = request.args.get('category')
    avg_rating = multi_query.get_category_avg_ratings(category)
    return jsonify({'category': category, 'avg_rating': avg_rating})

@app.route('/products/category/top-discounted')
def category_top_discounted_products():
    category = request.args.get('category')
    min_discount = request.args.get('min_discount', default=20, type=int)
    limit = request.args.get('limit', default=10, type=int)
    data = multi_query.get_category_top_discounted_products(category, min_discount, limit)
    return jsonify(data)

@app.route('/products/search')
def search_products():
    keyword = request.args.get('keyword', default='', type=str)
    limit = request.args.get('limit', default=10, type=int)

    data = multi_query.search_products(keyword, limit)
    return jsonify(data)

@app.route('/reviews/search')
def search_reviews():
    keyword = request.args.get('keyword', default='', type=str)
    limit = request.args.get('limit', default=10, type=int)
    
    data = multi_query.search_reviews(keyword, limit)
    return jsonify(data)

@app.route('/products/filter')
def filtered_products():
    category = request.args.get('category')
    min_price = request.args.get('min_price', default=None, type=float)
    max_price = request.args.get('max_price', default=None, type=float)
    min_rating = request.args.get('min_rating', default=None, type=float)
    limit = request.args.get('limit', default=50, type=int)

    data = multi_query.filtered_products(category, min_price, max_price, min_rating, limit)
    return jsonify(data)

@app.route('/products/weighted-rating')
def weighted_rating():
    min_reviews = request.args.get('min_reviews', default=50, type=int)
    limit = request.args.get('limit', default=10, type=int)

    data = multi_query.weighted_rating(min_reviews, limit)
    return jsonify(data)

@app.route('/products/<product_id>/similar')
def similar_products(product_id):
    limit = request.args.get('limit', default=10, type=int)

    data = multi_query.similar_products(product_id, limit)
    return jsonify(data)

@app.route('/products/total_products')
def total_products():
    data = multi_query.get_total_products()
    return jsonify(data)

@app.route('/products/avg_rating')
def avg_rating():
    data = multi_query.get_avg_rating()
    return jsonify(data)

@app.route('/products/total_discounted')
def avg_discount():
    data = multi_query.get_total_discounted_products()
    return jsonify(data)

@app.route('/products/total_reviews')
def total_ratings():
    data = multi_query.get_total_reviews()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)