from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Book

#Connect to Database and create database session
engine = create_engine('sqlite:///books.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#JSON APIs to view books for one category
@app.route('/category/<int:category_id>/book/JSON')
def categoryBookJSON(category_id):
    # category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Book).filter_by(category_id=category_id).all()
    return jsonify(books=[i.serialize for i in items])


#JSON APIs to view details for one book
@app.route('/category/<int:category_id>/book/<int:book_id>/JSON')
def bookJSON(category_id, book_id):
    bookItem = session.query(Book).filter_by(id = book_id).one()
    return jsonify(bookItem = bookItem.serialize)


#JSON APIs to view categories
@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories= [c.serialize for c in categories])


@app.route('/')
@app.route('/category')
def categories():
    categories = session.query(Category).order_by(Category.name).all()
    return render_template('categories.html', categories=categories)


@app.route('/category/<int:category_id>/book')
def categoryBooks(category_id):
	books = session.query(Book).filter_by(category_id=category_id).all()
	return render_template('books.html', books=books)


@app.route('/category/<int:category_id>/book/<int:book_id>')
def bookDetail(category_id, book_id):
    book = session.query(Book).filter_by(id = book_id).one()
    return render_template("bookDetail.html", book=book)


@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        category = None
        if 'desc' in request.form and request.form['desc'] != "":
            category = Category(name=request.form['name'], desc=request.form['desc'])
        else:
            category = Category(name=request.form['name'])
        session.add(category)
        session.commit()
        return redirect(url_for('categories'))
    else:
        return render_template("newCategory.html")


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        return redirect(url_for('categories'))
    else:
        return render_template("deleteCategory.html", category=category)

if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
