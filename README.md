# Book List Application

## Description
This is a Flask application for users to share their book list with others.

## Requirements
This project need to be run with `Python 2.7`, and the libraries required in this project are included in `requirement.txt`. To install the libraries, you can just simply run `pip install -r requirements.txt`

For Google login feature, you need to include your client secrect file downloaded from Google API console as `client_secret.json` and to replace following lines in `login.html` with your own client ID.
```html
            <!-- GOOGLE PLUS SIGN IN BUTTON-->        
            <div id="signinButton">
                <span class="g-signin"
                    ...
                    data-clientid="YOUR_CLIENT_ID.apps.googleusercontent.com"
                    ...>
                </span>
            </div>

            ...
            <script>

            auth2 = gapi.auth2.init({
                client_id: 'YOUR_CLIENT_ID.apps.googleusercontent.com',
                scope: 'profile'
            })

            ...
            </script>
            ...

```

## Usage
After meeting mentioned requirements, simply type `python project.py` to start the server, and the website will be served at `http://localhost:5000`

## JSON endpoint
When the server is on, it can provide 3 JSON API
* `/category/JSON` for getting all categories
* `/category/<int:category_id>/book/JSON` for getting all books within a given category
* `/category/<int:category_id>/book/<int:book_id>/JSON` for getting details for a given book