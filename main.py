from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
all_books = []

class books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

db.create_all()

def create_record(name, author, rating):
    book = books(title=name, author=author, rating=rating)
    db.session.add(book)
    db.session.commit()

@app.route('/', methods=["GET", "POST"])
def home():
    book_lst = books.query.all()
    return render_template("index.html", books=book_lst)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        author = request.form["author"]
        rating = request.form["rating"]

        create_record(name, author, rating)
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    book_id = request.args.get("id")
    book_to_update = books.query.get(book_id)
    if request.method == "POST":
        book_to_update.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", book_info=book_to_update)

@app.route("/delete")
def delete():
    book_id = request.args.get("id")
    book_to_delete = books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

