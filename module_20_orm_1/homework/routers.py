from flask import Flask, jsonify, request

from crud import (
    crud_get_all_books,
    crud_get_all_debtors_students,
    crud_post_to_give_book,
    crud_post_back_book,
    book_to_dict,
    student_to_dict,
    receiving_to_dict,
    crud_search_books_by_name,

)

app = Flask(__name__)


@app.route('/books', methods=['GET'])
def get_all_books():
    results = crud_get_all_books()
    if results:
        return jsonify({'books': [book_to_dict(b) for b in results]}), 200
    return jsonify({"results": "Пустой список"}), 200


@app.route('/debtors', methods=['GET'])
def get_debtors():
    results = crud_get_all_debtors_students()
    if results:
        return jsonify({'debtors': [student_to_dict(s) for s in results]}), 200
    return jsonify({"result": "Таких учеников нет"})


@app.route('/give/book', methods=['POST'])
def get_student():
    data = request.get_json()
    if not data or 'student_id' not in data or 'book_id' not in data:
        return jsonify({'error': 'Missing student_id or book_id'}), 400
    result = crud_post_to_give_book(data['student_id'], data['book_id'])
    if result:
        return jsonify({'message': 'Book issued', 'record': receiving_to_dict(result)}), 201
    return jsonify({"result": "эта книга уже выдана"}), 400


@app.route('/back/book', methods=['POST'])
def post_back_book():
    data = request.get_json()
    if not data or 'student_id' not in data or 'book_id' not in data:
        return jsonify({'error': 'Missing student_id or book_id'}), 400
    result = crud_post_back_book(data['student_id'], data['book_id'])
    if result:
        return jsonify({'message': 'Book returned', 'record': receiving_to_dict(result)}), 200
    return jsonify({'result': 'Неверный id'}), 400

@app.route('/search/book/<string:book_name>', methods=['GET'])
def search_book(book_name):
    results = crud_search_books_by_name(book_name)
    if results:
        return jsonify({'books': [book_to_dict(b) for b in results]}), 200
    return jsonify({"result": "Список пустой"}), 200