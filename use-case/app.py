# app.py
# This is the main Flask application that handles search requests and renders the search page.

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, _

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)
db = SQLAlchemy(app)

from models import Hotel

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en', 'fr', 'de', 'uk'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')

    if len(query) > 200 or any(char in query for char in set("!@#$%^&*(){}[]|:;'<>,.?/`~\"")):
        return jsonify(error=_("Search input cannot contain special symbols.")), 400

    search_results = perform_search(query)
    return jsonify(results=search_results)

def perform_search(query):
    filtered_query = query.replace('%', ' ').replace('_', ' ').split()
    if not filtered_query:
        return []

    search_results = Hotel.query.filter(
        db.or_(
            *[db.func.lower(Hotel.city).like(f"%{term.lower()}%") for term in filtered_query],
            *[db.func.lower(Hotel.name).like(f"%{term.lower()}%") for term in filtered_query],
            *[db.func.lower(Hotel.street).like(f"%{term.lower()}%") for term in filtered_query]
        )
    ).all()

    return [{'name': hotel.name, 'location': f'{hotel.city}, {hotel.street}'} for hotel in search_results]

if __name__ == '__main__':
    app.run(debug=True)