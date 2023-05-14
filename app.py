from flask import Flask, render_template, url_for, redirect, session, request, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Python'  # ან app.secret_key="Python"
# ბაზის მისამართის დამატება
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.sqlite"
# ბაზის ობიექტის შექმნა
db = SQLAlchemy(app)


# ბაზის შესაბამისი ცხრილის მოდელის(კლასის შექმნა): კლასის სახელი = ცხრილის სახელს და სვეტების სახელები = ცხრილის სვეტების სახელებს

class Books(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(30))
    author = db.Column('author', db.String(40))
    price = db.Column('price', db.Integer)

# https://github.com/ninikvinikadze02/FinalExam

@app.route('/')
def hello_world():
    # ყველა ჩანაწერის წამოღება ცხრილიდან
    books = Books.query.all()
    if books:
        messages = [message for message in get_flashed_messages()]
        return render_template('index.html', books=books, messages=messages)
    else:
        return "No books found in the database."


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form["username"]
        return redirect(url_for("hello_world"))
    return render_template('login.html')


@app.route("/books", methods=['GET', 'POST'])
def books():
    # ცხრილში სტრიქონის შემოტანა
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        price = request.form["price"]
        book = Books(title=title, author=author, price=price)
        db.session.add(book)
        db.session.commit()
        flash("Added Successfully! ")
        return redirect(url_for("hello_world"))
    return render_template("books.html")


if __name__ == '__main__':
    app.run()
