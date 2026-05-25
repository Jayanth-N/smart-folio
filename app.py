from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import json

app = Flask(__name__)
app.secret_key = 'simple-secret-key'
DB_PATH = 'portfolio.db'


def load_users():
    with open('users.json') as f:
        return json.load(f)


def init_db():
    """Initialize the database with the stocks table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            symbol TEXT NOT NULL,
            company TEXT,
            percentage REAL NOT NULL,
            rationale TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('portfolio', username=session['user']))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        users = load_users()

        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('portfolio', username=username))
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/browse')
def browse():
    """Browse all users' portfolios."""
    if 'user' not in session:
        return redirect(url_for('login'))

    users = load_users()
    conn = get_db()

    user_portfolios = []
    for username in users.keys():
        stocks = conn.execute('SELECT * FROM stocks WHERE username = ? ORDER BY percentage DESC', (username,)).fetchall()
        total = conn.execute('SELECT COALESCE(SUM(percentage), 0) as total FROM stocks WHERE username = ?', (username,)).fetchone()['total']
        user_portfolios.append({
            'username': username,
            'stocks': stocks,
            'total_allocated': total,
            'stock_count': len(stocks)
        })

    conn.close()
    return render_template('browse.html', portfolios=user_portfolios, current_user=session['user'])


@app.route('/portfolio/<username>')
def portfolio(username):
    """View a user's portfolio."""
    if 'user' not in session:
        return redirect(url_for('login'))

    users = load_users()
    if username not in users:
        return redirect(url_for('browse'))

    is_owner = (session['user'] == username)

    conn = get_db()
    stocks = conn.execute('SELECT * FROM stocks WHERE username = ? ORDER BY percentage DESC', (username,)).fetchall()
    total_allocated = conn.execute('SELECT COALESCE(SUM(percentage), 0) as total FROM stocks WHERE username = ?', (username,)).fetchone()['total']
    conn.close()

    unallocated = max(0, 100 - total_allocated)

    return render_template('portfolio.html',
                           stocks=stocks,
                           total_allocated=total_allocated,
                           unallocated=unallocated,
                           portfolio_owner=username,
                           is_owner=is_owner,
                           current_user=session['user'])


@app.route('/add', methods=['POST'])
def add_stock():
    """Add a new stock entry."""
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']
    symbol = request.form.get('symbol', '').upper().strip()
    company = request.form.get('company', '').strip()
    percentage = request.form.get('percentage', type=float) or 0
    rationale = request.form.get('rationale', '').strip()

    if symbol and percentage > 0:
        conn = get_db()
        current_total = conn.execute('SELECT COALESCE(SUM(percentage), 0) as total FROM stocks WHERE username = ?', (username,)).fetchone()['total']
        if current_total + percentage <= 100:
            conn.execute(
                'INSERT INTO stocks (username, symbol, company, percentage, rationale) VALUES (?, ?, ?, ?, ?)',
                (username, symbol, company, percentage, rationale)
            )
            conn.commit()
        conn.close()

    return redirect(url_for('portfolio', username=username))


@app.route('/delete/<int:stock_id>', methods=['POST'])
def delete_stock(stock_id):
    """Delete a stock entry (only owner can delete)."""
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    # Only delete if the stock belongs to current user
    conn.execute('DELETE FROM stocks WHERE id = ? AND username = ?', (stock_id, session['user']))
    conn.commit()
    conn.close()
    return redirect(url_for('portfolio', username=session['user']))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
