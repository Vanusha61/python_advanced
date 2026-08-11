import csv
from flask import Flask, jsonify, request
from io import StringIO
from config import Session, Student
# from crud import (
#     crud_get_all_books,
#     crud_get_all_debtors_students,
#     crud_post_to_give_book,
#     crud_post_back_book,
#     book_to_dict,
#     student_to_dict,
#     receiving_to_dict,
#     crud_search_books_by_name,
#
# )
from crud import (
    get_count_books,
    get_books_student_not_author,
    get_month_books,
    book_to_dict,
    books_to_list,
    get_student_balls_avg,
    get_top_10_student,
    student_with_books_to_dict
)
app = Flask(__name__)


@app.route('/students/upload', methods=['POST'])
def upload_students():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    stream = StringIO(file.stream.read().decode('utf-8'))
    reader = csv.DictReader(stream, delimiter=';')
    students_data = list(reader)
    if not students_data:
        return jsonify({'error': 'Empty CSV'}), 400
    with Session() as session:
        session.bulk_insert_mappings(Student, students_data)
        session.commit()

    return jsonify({'message': f'Inserted {len(students_data)} students'}), 201
@app.route('/students/top10', methods=['GET'])
def top10():
    students = get_top_10_student()
    if students:
        return jsonify([student_with_books_to_dict(s) for s in students]), 200
    return jsonify({"result": "-"})


@app.route('/books/<int:author_id>', methods=['GET'])
def get_books_author(author_id: int):
    result = get_count_books(author_id)
    return jsonify({"counts": result}), 200

@app.route('/books/available/<int:student_id>', methods=['GET'])
def get_books_student(student_id: int):
    result = get_books_student_not_author(student_id)
    if result:
        return jsonify({
            'student_id': student_id,
            'books': books_to_list(result)
        }), 200
    return jsonify({"result": "Данный студент не брал книг"}), 200

@app.route('/student/avg', methods=['GET'])
def get_avg_student():
    result = get_month_books()
    return jsonify({'result': result}), 200

@app.route('/books/popular', methods=['GET'])
def get_popular_books():
    result = get_student_balls_avg()
    if result:
        return jsonify({'book': book_to_dict(result)}), 200
    return jsonify({'book': "-"}), 200

# @app.route('/books', methods=['GET'])
# def get_all_books():
#     results = crud_get_all_books()
#     if results:
#         return jsonify({'books': [book_to_dict(b) for b in results]}), 200
#     return jsonify({"results": "Пустой список"}), 200
#
#
# @app.route('/debtors', methods=['GET'])
# def get_debtors():
#     results = crud_get_all_debtors_students()
#     if results:
#         return jsonify({'debtors': [student_to_dict(s) for s in results]}), 200
#     return jsonify({"result": "Таких учеников нет"})
#
#
# @app.route('/give/book', methods=['POST'])
# def get_student():
#     data = request.get_json()
#     if not data or 'student_id' not in data or 'book_id' not in data:
#         return jsonify({'error': 'Missing student_id or book_id'}), 400
#     result = crud_post_to_give_book(data['student_id'], data['book_id'])
#     if result:
#         return jsonify({'message': 'Book issued', 'record': receiving_to_dict(result)}), 201
#     return jsonify({"result": "эта книга уже выдана"}), 400
#
#
# @app.route('/back/book', methods=['POST'])
# def post_back_book():
#     data = request.get_json()
#     if not data or 'student_id' not in data or 'book_id' not in data:
#         return jsonify({'error': 'Missing student_id or book_id'}), 400
#     result = crud_post_back_book(data['student_id'], data['book_id'])
#     if result:
#         return jsonify({'message': 'Book returned', 'record': receiving_to_dict(result)}), 200
#     return jsonify({'result': 'Неверный id'}), 400
#
# @app.route('/search/book/<string:book_name>', methods=['GET'])
# def search_book(book_name):
#     results = crud_search_books_by_name(book_name)
#     if results:
#         return jsonify({'books': [book_to_dict(b) for b in results]}), 200
#     return jsonify({"result": "Список пустой"}), 200