from marshmallow import Schema, fields, validates, ValidationError, post_load

from models import get_book_by_title, Book, Author


class BookAuthorNewSchema(Schema):
    id = fields.Int(required=False, allow_none=False)
    first_name = fields.Str(required=False, allow_none=False)
    last_name = fields.Str(required=False, allow_none=False)
    middle_name = fields.Str(required=False, allow_none=False)

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=False)
    author = fields.Nested(BookAuthorNewSchema, required=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )

    @post_load
    def create_book(self, data: dict) -> Book:
        data.pop('author', None)
        return Book(**data)


class BookPutSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=True)

    @post_load
    def create_book(self, data: dict) -> Book:
        return Book(**data)

class BookIdSchemaResponse(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    author_id = fields.Int(dump_only=True)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False, allow_none=False)

    @post_load
    def create_author(self, data: dict) -> Author:
        return Author(**data)

class AuthorResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    middle_name = fields.Str(dump_only=True)





