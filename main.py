from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
#all_books = []


class Base(DeclarativeBase):
    pass

#Creating dataBase for the books.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True,  nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0, nullable=False )


    def __repr__(self):
        return f"<Book id={self.id} title={self.title} author={self.author}>"

with app.app_context():
    db.create_all()



@app.route('/', methods=['GET', 'POST'])
def home():

    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()

    return render_template("index.html", books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(title=request.form['title'],
                        author=request.form['book_author'],
                        rating=request.form['rating'])

        with app.app_context():
            db.session.add(new_book)
            db.session.commit()

        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':

        book_id = request.form['id']
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))

    book_id = request.args.get('id')
    book_to_update = db.get_or_404(Book, book_id)
    return render_template("edit_rating.html", book=book_to_update)

@app.route("/delete", methods=['GET', 'POST'])
def delete():
    book_id = request.args.get('id')

    book_to_delete = db.get_or_404(Book, book_id)

    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
