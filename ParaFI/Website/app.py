import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g

# Path to the SQLite database
DATABASE = 'C:/Users/Omar/Desktop/ParaFI/data/users.db'

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Necessary for session management

def get_db():
    """ Get a database connection. """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """ Close the database connection at the end of the request. """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """ Execute a database query and fetch results. """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def home():
    """ Render the home page. """
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Handle login for the user. """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Omar' and password == 'Pass':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """ Render the dashboard page only if logged in. """
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/users')
def users():
    """ Fetch all users and display them. """
    user_data = query_db('SELECT username, password FROM users')
    return render_template('users.html', users=user_data)

@app.route('/logout')
def logout():
    """ Logout the user and clear the session. """
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/new-user')
def new_user():
    """ Render the page to create a new user. """
    return render_template('newuser.html')

@app.route('/create-user', methods=['POST'])
def create_user():
    """ Create a new user in the database. """
    user_details = request.get_json()
    db = get_db()
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
               (user_details['username'], user_details['password']))
    db.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/update-user', methods=['POST'])
def update_user():
    """ Update an existing user in the database. """
    data = request.get_json()
    db = get_db()
    db.execute('UPDATE users SET username = ?, password = ? WHERE username = ?',
               (data['username'], data['password'], data['oldUsername']))
    db.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/delete-user', methods=['POST'])
def delete_user():
    """ Delete a user from the database. """
    data = request.get_json()
    username = data['username']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({'message': 'No user found with that username'}), 404
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
