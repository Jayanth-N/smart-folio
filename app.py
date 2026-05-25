from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'portfolio.db'


def init_db():
    """Initialize the database with the stocks table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            company TEXT,
            quantity REAL,
            price REAL,
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
    """Main page - show all stocks and add form."""
    conn = get_db()
    stocks = conn.execute('SELECT * FROM stocks ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', stocks=stocks)


@app.route('/add', methods=['POST'])
def add_stock():
    """Add a new stock entry."""
    symbol = request.form.get('symbol', '').upper().strip()
    company = request.form.get('company', '').strip()
    quantity = request.form.get('quantity', type=float)
    price = request.form.get('price', type=float)
    rationale = request.form.get('rationale', '').strip()

    if symbol:
        conn = get_db()
        conn.execute(
            'INSERT INTO stocks (symbol, company, quantity, price, rationale) VALUES (?, ?, ?, ?, ?)',
            (symbol, company, quantity, price, rationale)
        )
        conn.commit()
        conn.close()

    return redirect(url_for('index'))


@app.route('/delete/<int:stock_id>', methods=['POST'])
def delete_stock(stock_id):
    """Delete a stock entry."""
    conn = get_db()
    conn.execute('DELETE FROM stocks WHERE id = ?', (stock_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
