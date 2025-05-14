import os
import sqlalchemy

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    render_template,
    make_response,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
db_link = "postgresql://hello_flask:hello_flask@localhost:5432/hello_flask_dev"



@app.route('/')
def root():

    messages = [{}]
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_credentials = are_credentials_good(username, password)
    #sql = sqlalchemy.sql.text('''
    #SELECT screen_name, created_at, text, place_name
    #FROM tweets
    #JOIN users USING (id_users)
    #ORDER BY created_at DESC
    #LIMIT 20 :tweets;
    #''');

    page = request.args.get('page', 1, type=int)

    # Raw SQL query for the latest 20 tweets with pagination
    sql = sqlalchemy.sql.text('''
    SELECT screen_name, created_at, text
    FROM tweets
    JOIN users ON tweets.id_users = users.id_users
    ORDER BY created_at DESC
    LIMIT 20 OFFSET :offset
    ''')

    # Calculate offset based on the current page
    offset = (page - 1) * 20

    # Execute the query with the offset parameter
    result = db.session.execute(sql, {'offset': offset}).fetchall()

    # Prepare the messages for the template
    messages = [{
        'screen_name': row[0],
        'created_at': row[1],
        'text': row[2]
    } for row in result]

    # Render the template with the messages and logged-in status
    return render_template('root.html', logged_in=good_credentials, messages=messages, page=page)

def print_debug_info():
    username = request.args.get('username')
    password = request.args.get('password')
    # print('request.args.get(username)=', request.args.get('username'))
    # print('request.args.get(password)=', request.args.get('password'))

def are_credentials_good(username, password):
    #FIXME:
    #look inside databse and check if password is correct for the user
    if not username or not password:
        return False


    sql = sqlalchemy.text('''
    SELECT screen_name, password 
    FROM users
    WHERE screen_name = :username 
    AND password = :password
    ''')

    result = db.session.execute(sql, {'username': username, 'password': password}).first()
    return result is not None

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # print('username=', username)
    good_credentials = are_credentials_good(username, password)
    if username is None:
        return render_template('login.html', bad_credentials=False)
    else:
        if not good_credentials:
            return render_template('login.html', bad_credentials=True)
        else:

            #return 'skibidi success :D'
            #template =  render_template('root.html', logged_in=True, bad_credentials=False, messages=[], page=1)
            response = make_response(redirect(url_for('root')))
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            return response


@app.route('/logout')
def logout():
    response = make_response(render_template('logout.html', logged_in=False))
    response.set_cookie('username', '', expires=0)
    response.set_cookie('password', '', expires=0)
    return response


def username_dne(username):
    sql = sqlalchemy.text('''
    SELECT screen_name
    FROM users
    where screen_name = :username
    LIMIT 1
    ''')
    result = db.session.execute(sql, {'username': username}).first()
    return result is None

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('retype-password')
    valid_user = username_dne(username)
    if password2 is None:
       return render_template('create_user.html')
    else:
       if not username or not password or not password2:
            return render_template('create_user.html', error="All fields are required.")
       if password != password2:
            return render_template('create_user.html', error="Passwords do not match.")
       if not valid_user:
            return render_template('create_user.html', error="Username already taken.")

            #return 'skibidi success :D'
            #template =  render_template('root.html', logged_in=True, bad_credentials=False, messages=[], page=1)
       sql_insert = sqlalchemy.text('''
                INSERT INTO users (screen_name, password)
                VALUES (:username, :password)
            ''')
       db.session.execute(sql_insert, {'username': username, 'password': password})
       db.session.commit()
       return render_template('create_user.html', account_created=True)

@app.route('/create_message', methods=['GET', 'POST'])
def create_message():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_credentials = are_credentials_good(username, password)

    if not good_credentials:
        return redirect(url_for('login'))

    sql = sqlalchemy.text('''
    SELECT id_users, screen_name
    FROM users
    where screen_name = :username
    LIMIT 1
    ''')

    res = db.session.execute(sql, {'username': username}).first()
    if res:
        id_users = res.id_users
    else:
        id_users = None
    created_at = db.func.now()
    #created_at = cur_time.replace(microsecond=0)
    if request.method == 'POST':

        message = request.form.get('message')

        if message:
            sql = sqlalchemy.sql.text('''
            INSERT INTO tweets (id_users, created_at, text)
            VALUES (:id_users, NOW(), :text) ''')

            db.session.execute(sql, {
                'id_users': id_users,
                #'created_at': created_at,
                'text': message
                })
            db.session.commit()
            return render_template('create_message.html', logged_in=good_credentials, message_created=True)
    return render_template('create_message.html', logged_in=good_credentials)

@app.route('/search_message', methods=['GET', 'POST'])
def search_message():
    
#class User(db.Model):
#    __tablename__ = "users"
#    id = db.Column(db.Integer, primary_key=True)
#    email = db.Column(db.String(128), unique=True, nullable=False)
#    active = db.Column(db.Boolean(), default=True, nullable=False)
#
#    def __init__(self, email):
#        self.email = email
#
#
#@app.route("/")
#def hello_world():
#    return jsonify(hello="world")
#
#
#@app.route("/static/<path:filename>")
#def staticfiles(filename):
#    return send_from_directory(app.config["STATIC_FOLDER"], filename)
#
#
#@app.route("/media/<path:filename>")
#def mediafiles(filename):
#    return send_from_directory(app.config["MEDIA_FOLDER"], filename)
#
#
#@app.route("/upload", methods=["GET", "POST"])
#def upload_file():
#    if request.method == "POST":
#        file = request.files["file"]
#        filename = secure_filename(file.filename)
#        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
#    return """
#    <!doctype html>
#    <title>upload new File</title>
#    <form action="" method=post enctype=multipart/form-data>
#      <p><input type=file name=file><input type=submit value=Upload>
#    </form>
#    """
