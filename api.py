from flask import Flask, render_template, render_template, request, jsonify, send_from_directory
from routes.products import products_bp


app = Flask(__name__)
app.register_blueprint(products_bp, url_prefix='/products')


@app.route('/')
def homepage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)