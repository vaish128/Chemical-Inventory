from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "very_secret_key_123" # Secure key for login sessions

# Admin Credentials
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin@123"

def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    # Create Table based on assignment requirements
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cas_number TEXT UNIQUE, unit TEXT, stock INTEGER)''')
    # History Table (For Movement Tracking)
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, type TEXT, amount INTEGER, date TEXT)''')
    conn.commit()
    conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash("Invalid Credentials. Please try again.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():

    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    search = request.args.get('search', '')
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    # Search logic: filtering by Name or CAS
    query = "SELECT * FROM inventory WHERE name LIKE ? OR cas_number LIKE ?"
    cursor.execute(query, (f'%{search}%', f'%{search}%'))
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', inventory=items, search_val=search)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    cas = request.form['cas']
    unit = request.form['unit']
    stock = int(request.form['stock'])
    
    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (name, cas_number, unit, stock) VALUES (?,?,?,?)", 
                       (name, cas, unit, stock))
        conn.commit()
    except sqlite3.IntegrityError:
        flash("Error: CAS Number must be unique!")
    finally:
        conn.close()
    return redirect('/')

@app.route('/update_stock/<int:id>', methods=['POST'])
def update_stock(id):
    action = request.form['action']
    amount = int(request.form['amount'])
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT stock, name FROM inventory WHERE id=?", (id,))
    res = cursor.fetchone()
    current_stock, name = res[0], res[1]

    if action == 'OUT' and (current_stock - amount) < 0:
        flash(f"Insufficient stock for {name}!")
    else:
        new_stock = (current_stock + amount) if action == 'IN' else (current_stock - amount)
        cursor.execute("UPDATE inventory SET stock=? WHERE id=?", (new_stock, id))
        # Log the movement
        cursor.execute("INSERT INTO history (product_id, type, amount, date) VALUES (?,?,?,?)", 
                       (id, action, amount, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_product(id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)