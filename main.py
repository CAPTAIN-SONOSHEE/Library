from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"

db.init_app(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html", books = db.session.execute(db.select(Books).order_by(Books.title)).scalars().all())

@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = db.get_or_404(Books,id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == 'POST':
        new_book = Books(title=request.form['title'], author=request.form['author'], rating=float(request.form['rating']))
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template("add.html")

@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        book_to_update = db.get_or_404(Books, id)
        book_to_update.rating = request.form['rate']
        db.session.commit()
        return redirect(url_for('home'))
    
    book_name = db.get_or_404(Books, id).title
    book_rating = db.get_or_404(Books, id).rating
    return render_template("edit.html", name = book_name, rating = book_rating, id=id)

if __name__ == "__main__":
    app.run(debug=True)

