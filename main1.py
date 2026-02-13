from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

class Base(DeclarativeBase):
    pass


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



with app.app_context():
    new_book = Book(id=1, title="New Book", author="suda", rating=10)
    db.session.add(new_book)
    db.session.commit()