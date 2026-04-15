from unicodedata import category

from flask import Blueprint, request, jsonify
from services import analytics

products_bp = Blueprint('products', __name__)

@products_bp.route('/total-products')
def total_products():
    data = analytics.get_total_products()
    return jsonify({
        'success': True,
        'total_products': data
    })
    
@products_bp.route('/top-rated')
def top_rated_products():
    min_reviews = request.args.get('min_reviews', default=50, type=int)
    limit = request.args.get('limit', default=10, type=int)

    data = analytics.get_top_rated_products(min_reviews, limit)
    return jsonify({
        'success': True,
        'top_rated': data    
    })

@products_bp.route('/most-reviewed')
def most_reviewed_products():
    limit = request.args.get('limit', default=10, type=int)

    data = analytics.get_most_reviewed_products(limit)
    return jsonify({
        'success': True,
        'most_reviewed': data
    })
    
@products_bp.route('/discounted')
def discounted_products():
    min_discount = request.args.get('min_discount', default=20, type=int)
    limit = request.args.get('limit', default=10, type=int)

    data = analytics.get_discounted_products(min_discount, limit)
    return jsonify({
        'success': True,
        'discounted': data
    })


@products_bp.route('/avg-rating')
def avg_rating():
    avg_rating = analytics.get_avg_rating()

    return jsonify({
        'success': True,
        'avg_rating': avg_rating
    })

@products_bp.route('/top-discounted')
def category_top_discounted_products():
    category = request.args.get('category')
    min_discount = request.args.get('min_discount', default=20, type=int)
    limit = request.args.get('limit', default=10, type=int)
    data = analytics.get_category_top_discounted_products(category, min_discount, limit)
    return jsonify({
        'success': True,
        'category': category,
        'top_discounted': data
    })
    
@products_bp.route('/total-reviews')
def total_reviews():
    data = analytics.get_total_reviews()
    return jsonify({
        'success': True,
        'total_reviews': data
    })
    
@products_bp.route('/total-discounted')
def total_discounted_products():
    data = analytics.get_total_discounted_products()
    return jsonify({
        'success': True,
        'total_discounted': data
    })
    
@products_bp.route('/filtered-products')
def filtered_products():
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)

    results = analytics.filtered_products(category, min_price, max_price, min_rating)
    return jsonify({
        'success': True,
        'filtered_products': results
    })