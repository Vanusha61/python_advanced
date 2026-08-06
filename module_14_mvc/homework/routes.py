from flask import Flask, render_template, request, url_for, redirect
from typing import List

from werkzeug import Response

from models import init_db, get_all_books, DATA, add_book, author_all_books, add_views_count
from flaskform.main import FormAddBook

app: Flask = Flask(__name__)


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books()
    )


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form() -> Response | str:
    form = FormAddBook()
    if form.validate_on_submit():
        name_book = form.book_title.data
        author_name = form.author_name.data
        add_book(name_book, author_name)
        return redirect(url_for('all_books'))
    return render_template('add_book.html', form=form)

@app.route('/author/books', methods=['GET'])
def get_author_books():
    author_name = request.args.get('author_name')
    books = None
    if author_name:
        books = author_all_books(author_name)
    return render_template('author_books.html', books=books, author_name=author_name)

@app.route("/book/id", methods=['GET'])
def get_book():
    book_id = request.args.get('book_id')
    if book_id:
        book = add_views_count(int(book_id))
    else:
        book = None
    return render_template("add_views_count.html", book=book, book_id=book_id)



if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    init_db(DATA)
    app.run(debug=True)
