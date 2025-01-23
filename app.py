from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for session management

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('student.sqlite')  # Path to your SQLite database file
    conn.row_factory = sqlite3.Row        # Enables accessing columns by name
    return conn

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # Renders the home page

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM sample WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['user_id']  # Store the user ID in the session
            return redirect(url_for('profile'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

# Route for the profile page
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM sample  WHERE user_id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    if user:
        return render_template('profile.html', user=user)
    else:
        return "User not found."

if __name__ == '__main__':
    app.run(debug=True)
