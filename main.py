from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.getenv("CANVAS_API_KEY")

# Configure OAuth for Canvas
oauth = OAuth(app)
canvas = oauth.register(
    name='canvas',
    client_id='YOUR_CANVAS_CLIENT_ID',
    client_secret= app.secret_key,
    access_token_url='https://canvas.instructure.com/login/oauth2/token',
    authorize_url='https://canvas.instructure.com/login/oauth2/auth',
    client_kwargs={'scope': 'url:GET|/api/v1/courses'},
)

@app.route('/')
def home():
    return 'Welcome to the Canvas OAuth demo'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return canvas.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = canvas.authorize_access_token()
    session['token'] = token
    return redirect(url_for('get_courses'))

@app.route('/get_courses')
def get_courses():
    token = session.get('token')
    if not token:
        return redirect(url_for('login'))

    # Make a request to the Canvas API to retrieve the user's courses
    resp = canvas.get('https://canvas.instructure.com/api/v1/courses', token=token)
    courses = resp.json()
    return f'Courses: {courses}'

if __name__ == '__main__':
    app.run(debug=True)
