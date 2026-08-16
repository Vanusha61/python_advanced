from flask import Flask, request, jsonify
import requests
import random
from sqlalchemy import func
from model import Coffee, User
from config import session

app = Flask(__name__)

# Флаг, чтобы данные создавались только один раз
data_initialized = False

def create_test_data():
    global data_initialized
    if data_initialized:
        return
    with session() as db:
        if db.query(Coffee).first():
            data_initialized = True
            return

        coffee_response = requests.get('https://dummyjson.com/products/search?q=coffee')
        coffee_data = coffee_response.json()

        if coffee_data['products']:
            first_coffee = coffee_data['products'][0]
            reviews_list = [review['comment'] for review in first_coffee.get('reviews', [])]
            coffee = Coffee(
                title=first_coffee['title'],
                category=first_coffee.get('category'),
                description=first_coffee.get('description'),
                reviews=reviews_list
            )
            db.add(coffee)
            db.commit()

        users_response = requests.get('https://dummyjson.com/users?limit=10')
        users_data = users_response.json()

        for user_data in users_data['users']:
            user = User(
                name=f"{user_data['firstName']} {user_data['lastName']}",
                has_sale=random.choice([True, False]),
                address=user_data['address'],
                coffee_id=coffee.id
            )
            db.add(user)

        db.commit()
        data_initialized = True

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'name' not in data or 'address' not in data or 'coffee_id' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    with session() as db:
        user = User(
            name=data['name'],
            has_sale=data.get('has_sale', random.choice([True, False])),
            address=data['address'],
            coffee_id=data['coffee_id']
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        coffee_name = user.coffee.title if user.coffee else None

        return jsonify({
            'id': user.id,
            'name': user.name,
            'coffee': coffee_name
        }), 201

@app.route('/coffee/search', methods=['GET'])
def search_coffee():
    q = request.args.get('q', '')
    if not q:
        return jsonify({'error': 'Missing search query'}), 400

    with session() as db:
        results = db.query(Coffee).filter(
            func.to_tsvector('russian', Coffee.title).match(q)
        ).all()

    return jsonify([{
        'id': c.id,
        'title': c.title,
        'category': c.category,
        'description': c.description
    } for c in results])

@app.route('/coffee/reviews/unique', methods=['GET'])
def unique_reviews():
    coffee_id = request.args.get('coffee_id', type=int)
    with session() as db:
        if coffee_id:
            coffee = db.get(Coffee, coffee_id)
            if not coffee:
                return jsonify({'error': 'Coffee not found'}), 404
            reviews = coffee.reviews or []
        else:
            all_coffee = db.query(Coffee).all()
            reviews = []
            for c in all_coffee:
                if c.reviews:
                    reviews.extend(c.reviews)

    unique = list(set(reviews))
    return jsonify({'unique_reviews': unique})

@app.route('/users/by_country', methods=['GET'])
def users_by_country():
    country = request.args.get('country', '')
    if not country:
        return jsonify({'error': 'Missing country parameter'}), 400

    with session() as db:
        users = db.query(User).filter(
            User.address['country'].astext == country
        ).all()

    return jsonify([{
        'id': u.id,
        'name': u.name,
        'address': u.address,
        'coffee': u.coffee.title if u.coffee else None
    } for u in users])

if __name__ == '__main__':
    # Создаём тестовые данные при старте
    with app.app_context():
        create_test_data()
    app.run(debug=True, host='0.0.0.0')