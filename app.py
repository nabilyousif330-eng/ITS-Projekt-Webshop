import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT
            )
        ''')
        conn.execute("INSERT INTO products (name, description, price, image_url) VALUES ('Sicherer Laptop', 'Ein ultra-sicherer Laptop für IT-Security Experten.', 999.99, 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500')")
        conn.execute("INSERT INTO products (name, description, price, image_url) VALUES ('Hacker Gadget Flipper', 'Ein vielseitiges Werkzeug für Penetration Testing.', 169.00, 'https://images.unsplash.com/photo-1601597111158-2fceff292cdc?w=500')")
        conn.execute("INSERT INTO products (name, description, price, image_url) VALUES ('Krypto-Buch', 'Einführung in die moderne Kryptographie.', 49.95, 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500')")
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0
            )
        ''')
        conn.execute("INSERT INTO users (username, password, is_admin) VALUES ('admin', 'admin123', 1)")
        conn.execute("INSERT INTO users (username, password, is_admin) VALUES ('user1', 'password123', 0)")
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
