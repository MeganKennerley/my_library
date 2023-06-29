from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.FLOAT, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


""" CREATE DATABASE """
# with app.app_context():
#     """ CREATE DATABASE """
#     db.create_all()


@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        with app.app_context():
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        with app.app_context():
            book_id = request.form["id"]
            book_to_update = db.get_or_404(Book, book_id)
            book_to_update.rating = request.form["rating"]
            db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit.html", book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    with app.app_context():
        current_db_sessions = db.session.object_session(book_to_delete)
        current_db_sessions.delete(book_to_delete)
        current_db_sessions.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
