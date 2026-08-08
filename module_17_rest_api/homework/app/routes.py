from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id,
    get_all_authors,
    add_author,
    get_author_all_book_by_id,
    delete_author_by_id,
    get_author_by_id,
    Author,
    Book
)

from schemas import BookSchema, BookIdSchemaResponse, BookPutSchema, AuthorResponseSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        author_data = data['author']
        if author_data.get('id') is not None:
            res = get_author_by_id(author_data['id'])
            if not res:
                return {'message': 'Author not found'}, 404
            data['author_id'] = res.id
        elif author_data.get('first_name') is not None and author_data.get('last_name') is not None:
            new_author = Author(
                first_name=author_data.get('first_name'),
                last_name=author_data.get('last_name'),
                middle_name=author_data.get('middle_name'),
            )
            res = add_author(new_author)
            data['author_id'] = res.id
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        book = add_book(book)
        return schema.dump(book), 201

def put(self):
    data = request.json
    schema = BookPutSchema()
    try:
        book = schema.load(data)
    except ValidationError as exc:
        return exc.messages, 400
    update_book_by_id(book)
    return schema.dump(book), 200


class BookItem(Resource):
    def get(self, book_id: int | None):
        if book_id is None:
            return {'message': 'Author not found'}, 404
        schema = BookIdSchemaResponse()
        book = get_book_by_id(book_id)
        return schema.dump(book), 200

    def delete(self, book_id: int | None):
        if book_id is None:
            return {'message': 'Author not found'}, 404
        delete_book_by_id(book_id)
        return {"response": "Книга с id {} успешно удалена".format(book_id)}, 200


class Author(Resource):
    def get(self):
        shema = AuthorResponseSchema()
        return shema.dump(get_all_authors(), many=True), 200

    def post(self):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        res = add_author(author)
        return schema.dump(res), 201


class AuthorItem(Resource):

    def get(self, author_id: int | None):
        if author_id is None:
            return {'message': 'Author not found'}, 404
        shema = BookIdSchemaResponse()
        author_books = get_author_all_book_by_id(author_id)
        return shema.dump(author_books, many=True), 200

    def delete(self, author_id: int | None):
        if author_id is None:
            return {'message': 'Author not found'}, 404
        delete_author_by_id(author_id)
        return {"response": "Автор с id {} успешно удален".format(author_id)}, 200


api.add_resource(BookList, '/api/books')
api.add_resource(BookItem, '/api/books/<int:book_id>')
api.add_resource(Author, '/api/authors')
api.add_resource(AuthorItem, '/api/authors/<int:author_id>')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)
