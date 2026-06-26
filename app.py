import os
import sqlite3
from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)
VULNERABLE = True
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
    
@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    if VULNERABLE:
        import sqlite3
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        unsecure_query = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
        try:
            cursor.execute(unsecure_query)
            products = cursor.fetchall()
        except Exception as e:
            products = []
        conn.close()
        
        return render_template_string(f"<h2>Suchergebnisse für: {query}</h2><ul>" + 
                                      "".join([f"<li>{p[1]}</li>" for p in products]) + "</ul>")
    else:
        import sqlite3
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        secure_query = "SELECT * FROM products WHERE name LIKE ?"
        cursor.execute(secure_query, ('%' + query + '%',))
        products = cursor.fetchall()
        conn.close()
        
        return render_template('index.html', products=products, query=query)
@app.route('/view-file')
def view_file():
    filename = request.args.get('file', '')
    
    if VULNERABLE:
        import os
        if os.path.exists(filename):
            with open(filename, 'r', errors='ignore') as f:
                return f.read()
        return "File not found", 404
    else:
        import os
        base_dir = os.path.join(os.getcwd(), 'static')
        safe_path = os.path.abspath(os.path.join(base_dir, filename))
        if safe_path.startswith(os.path.abspath(base_dir)) and os.path.exists(safe_path):
            with open(safe_path, 'r', errors='ignore') as f:
                return f.read()
        return "Access Denied / File not found", 403        
@app.route('/invoice')
def invoice():
    invoice_id = request.args.get('id', '')
    
    if VULNERABLE:
        import sqlite3
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM products WHERE id = {invoice_id}")
            invoice_data = cursor.fetchone()
        except Exception as e:
            invoice_data = None
        conn.close()
        
        if invoice_data:
            return f"<h1>Invoice details for ID {invoice_id}</h1><p>Product: {invoice_data[1]}</p><p>Price: {invoice_data[2]}</p>"
        return "Invoice not found", 404
    else:
        current_user_allowed_ids = ['1', '2']
        if invoice_id not in current_user_allowed_ids:
            return "Access Denied: You do not own this invoice", 403
            
        import sqlite3
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (invoice_id,))
        invoice_data = cursor.fetchone()
        conn.close()
        
        if invoice_data:
            return f"<h1>Invoice details for ID {invoice_id}</h1><p>Product: {invoice_data[1]}</p><p>Price: {invoice_data[2]}</p>"
        return "Invoice not found", 404
        
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if VULNERABLE:
            if username == 'admin' and password == 'admin':
                return "<h1>Welcome Admin! (Security Misconfiguration: Default Credentials)</h1>"
            if username == "' OR '1'='1":
                return "<h1>Welcome Admin! (Broken Authentication: Bypass Successful)</h1>"
            return "Login Failed", 401
        else:
            if username == 'admin' and password == 'Secure_Password_2026_!#X':
                return "<h1>Welcome Admin!</h1>"
            return "Login Failed", 401
            
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''        
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    import sqlite3
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if VULNERABLE:
            try:
                cursor.execute(f"INSERT INTO products (name, price) VALUES ('{comment}', 0)")
                conn.commit()
            except Exception as e:
                pass
        else:
            cursor.execute("INSERT INTO products (name, price) VALUES (?, 0)", (comment,))
            conn.commit()
        conn.close()
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    
    if VULNERABLE:
        html = "<h1>Product Feedback</h1><form method='post'><textarea name='comment'></textarea><br><input type='submit'></form><ul>"
        for p in products:
            html += f"<li>{p[1]}</li>"
        html += "</ul>"
        return render_template_string(html)
    else:
        return render_template('index.html', products=products, query='')
@app.route('/update-profile', methods=['POST'])
def update_profile():
    email = request.form.get('email', '')
    if VULNERABLE:
        return f"<h1>Profile updated successfully to {email} (CSRF Vulnerable)</h1>"
    else:
        token = request.form.get('csrf_token', '')
        if token != "Secure_CSRF_Token_2026":
            return "CSRF Token Invalid", 403
        return f"<h1>Profile updated safely to {email}</h1>"

@app.route('/config-backup')
def config_backup():
    if VULNERABLE:
        return "DEBUG_MODE=True\nSECRET_KEY=12345\nDB_PASSWORD=admin_pass"
    else:
        return "Access Denied", 403        
        
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
    

