from flask import *
from werkzeug.exceptions import RequestEntityTooLarge
from flask_mysqldb import MySQL
import MySQLdb.cursors
from backend.functions import *
from werkzeug.utils import secure_filename
import os, re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS_EXCEL'] = ['.csv']

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return render_template("upload.html")

# ADMIN
@app.route('/admin', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin_user WHERE email = % s AND password = % s',(email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Logged in successfully !'
            return render_template('admin.html', message=message)
    else:
        message = 'Please enter correct email / password !'
        return render_template('admin_login.html', message=message)


#USER REGISTRATION
@app.route('/user_register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'first_name' in request.form and 'last_name' in request.form and 'phone' in request.form and 'company_name' in request.form:
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        company_name = request.form['company_name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetch_one()
        if account:
            message = 'Username Taken'
        elif not username or not password or not first_name or not last_name or not phone or not company_name:
            message = "Please Fill out the Form"
        else:
            cursor.execute('INSERT INTO user VALUES (%s, %s, %s, %s, %s, %s, %s)', (username, password,first_name, last_name, phone, company_name))
            mysql.connection.commit()
            message = "You have successfully registered"
            return render_template('user_resigter.html', message=message)
# USER LOGIN
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password))
        user = cursor.fetchone()
        return render_template('home.html', user=user)

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    return redirect(url_for('user_login'))

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        if file:
            if extension not in app.config['ALLOWED_EXTENSIONS_EXCEL']:
                return "This File is not Supported"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            print(secure_filename(file.filename))
            # Linear Regression
            data = linear_regression('static/uploads/{0}'.format(secure_filename(file.filename)))
            return render_template("regression.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
