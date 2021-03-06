from flask import (
    Flask,
    render_template,
    request,
    redirect,
    jsonify,
    url_for,
    flash
)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Book, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)
app.secret_key = 'JsKdsfGkd43ugukh7guyfg5FJF8'

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read()
)['web']['client_id']

# Connect to Database and create database session
engine = create_engine('postgresql:///books')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for x in xrange(32)
    )
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Route for login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print(data)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['id'] = data['id']

    indb_user = session.query(User).filter_by(
        id=login_session['id']
    ).all()
    if not indb_user:
        user = User(
            id=login_session['id'],
            name=login_session['username']
        )

        session.add(user)
        session.commit()

    output = """
        <h1>Welcome, {}!</h1>
        <img src="{}"
            style="width: 100px;
                    height: 100px;
                    border-radius: 150px;
                    -webkit-border-radius: 150px;
                    -moz-border-radius: 150px;"
        >
    """.format(login_session['username'], login_session['picture'])
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# Route for logout
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'),
            401
        )
        response.headers['Content-Type'] = 'application/json'
        return render_template(
            'logout.html',
            message='Current user not connected'
        )
    # print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    r = requests.post(
        'https://accounts.google.com/o/oauth2/revoke',
        params={'token': login_session['access_token']},
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )
    print 'result is '
    print r
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['id']
    del login_session['picture']
    response = make_response(json.dumps('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return render_template(
        'logout.html',
        message='Successfully disconnected.'
    )


# JSON APIs to view books for one category
@app.route('/category/<int:category_id>/book/JSON')
def categoryBookJSON(category_id):
    # category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Book).filter_by(category_id=category_id).all()
    return jsonify(books=[i.serialize for i in items])


# JSON APIs to view details for one book
@app.route('/category/<int:category_id>/book/<int:book_id>/JSON')
def bookJSON(category_id, book_id):
    bookItem = session.query(Book).filter_by(id=book_id).one()
    return jsonify(bookItem=bookItem.serialize)


# JSON APIs to view categories
@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# List all categories
@app.route('/')
@app.route('/category')
def categories():
    categories = session.query(Category).order_by(Category.name).all()
    return render_template(
        'categories.html',
        categories=categories,
        session=login_session
    )


# List all book within a category
@app.route('/category/<int:category_id>/book')
def categoryBooks(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(category_id=category_id).all()
    return render_template(
        'books.html',
        books=books,
        category=category,
        session=login_session
    )


# Book detail
@app.route('/category/<int:category_id>/book/<int:book_id>')
def bookDetail(category_id, book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return render_template(
        "bookDetail.html",
        book=book,
        category_id=category_id,
        session=login_session
    )


# Create a new category
@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    if "id" not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        category = None
        user = session.query(User).filter_by(id=login_session["id"]).one()
        if 'desc' in request.form and request.form['desc'] != "":
            category = Category(
                name=request.form['name'],
                desc=request.form['desc'],
                user=user
            )
        else:
            category = Category(name=request.form['name'], user=user)
        session.add(category)
        session.commit()
        return redirect(url_for('categories'))
    else:
        return render_template("newCategory.html", session=login_session)


# Delete a category
@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if "id" not in login_session:
        return redirect(url_for('showLogin'))
    category = session.query(Category).filter_by(id=category_id).one()
    if category.user_id != login_session["id"]:
        return render_template("error.html", message="You are not the owner.")
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        return redirect(url_for('categories'))
    else:
        return render_template(
            "deleteCategory.html",
            category=category,
            session=login_session
        )


# Edit a category
@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    if "id" not in login_session:
        return redirect(url_for('showLogin'))
    category = session.query(Category).filter_by(id=category_id).one()
    if category.user_id != login_session["id"]:
        return render_template("error.html", message="You are not the owner.")
    if request.method == 'POST':
        category.name = request.form['name']
        if 'desc' in request.form and request.form['desc'] != "":
            category.desc = request.form['desc']
        else:
            category.desc = None
        session.add(category)
        session.commit()
        return redirect(url_for('categories'))
    else:
        return render_template(
            "editCategory.html",
            category=category,
            session=login_session
        )


# Create a new book
@app.route('/category/<int:category_id>/book/new', methods=['GET', 'POST'])
def newBook(category_id):
    if "id" not in login_session:
        return redirect(url_for('showLogin'))
    category = session.query(Category).filter_by(id=category_id).one()
    if (category.user_id != login_session['id']):
        return render_template("error.html", message="You are not the owner.")
    if request.method == 'POST':
        user = session.query(User).filter_by(id=login_session["id"]).one()
        book = None
        book = Book(name=request.form['name'], category=category, user=user)
        if 'desc' in request.form and request.form['desc'] != "":
            book.desc = request.form['desc']
        if 'author' in request.form and request.form['author'] != "":
            book.author = request.form['author']
        session.add(book)
        session.commit()
        return redirect(url_for('categoryBooks', category_id=category.id))
    else:
        return render_template("newBook.html", session=login_session)


# Delete a book
@app.route(
    '/category/<int:category_id>/book/<int:book_id>/delete',
    methods=['GET', 'POST']
)
def deleteBook(category_id, book_id):
    if "id" not in login_session:
        return redirect(url_for('showLogin'))
    book = session.query(Book).filter_by(id=book_id).one()
    if book.user_id != login_session["id"]:
        return render_template("error.html", message="You are not the owner.")
    if request.method == 'POST':
        session.delete(book)
        session.commit()
        return redirect(url_for('categoryBooks', category_id=category_id))
    else:
        return render_template(
            "deleteBook.html",
            book=book,
            category_id=category_id,
            session=login_session
        )


# Edit a book
@app.route(
    '/category/<int:category_id>/book/<int:book_id>/edit',
    methods=['GET', 'POST']
)
def editBook(category_id, book_id):
    if "id" not in login_session:
        return redirect(url_for('showLogin'))
    book = session.query(Book).filter_by(id=book_id).one()
    if book.user_id != login_session["id"]:
        return render_template("error.html", message="You are not the owner.")
    if request.method == 'POST':
        book.name = request.form['name']
        if 'desc' in request.form and request.form['desc'] != "":
            book.desc = request.form['desc']
        else:
            book.desc = None
        if 'author' in request.form and request.form['author'] != "":
            book.author = request.form['author']
        else:
            book.author = None
        session.add(book)
        session.commit()
        return redirect(url_for('categoryBooks', category_id=category_id))
    else:
        return render_template(
            "editBook.html",
            book=book,
            category_id=category_id,
            session=login_session
        )


# List all categories created by current user
@app.route('/collection')
def myCollection():
    if "id" not in login_session:
        return redirect(url_for('showLogin'))
    categories = session.query(
        Category
    ).filter_by(
        user_id=login_session['id']
    ).order_by(
        Category.name
    ).all()
    return render_template(
        'collection.html',
        categories=categories,
        session=login_session
    )


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
