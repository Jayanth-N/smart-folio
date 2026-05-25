from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_PATH = 'portfolio.db'


def init_db():
    """Initialize the database with the stocks table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS stocks')
    c.execute('''
        CREATE TABLE stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    """Main page - show all stocks and pie chart."""
    conn = get_db()
    stocks = conn.execute('SELECT * FROM stocks ORDER BY percentage DESC').fetchall()
    total_allocated = conn.execute('SELECT COALESCE(SUM(percentage), 0) as total FROM stocks').fetchone()['total']
    conn.close()

    unallocated = max(0, 100 - total_allocated)

    return render_template('index.html', stocks=stocks, total_allocated=total_allocated, unallocated=unallocated)


@app.route('/add', methods=['POST'])
def add_stock():
    """Add a new stock entry."""
    symbol = request.form.get('symbol', '').upper().strip()
    company = request.form.get('company', '').strip()
    percentage = request.form.get('percentage', type=float) or 0
    rationale = request.form.get('rationale', '').strip()

    if symbol and percentage > 0:
        conn = get_db()
        # Check total won't exceed 100%
        current_total = conn.execute('SELECT COALESCE(SUM(percentage), 0) as total FROM stocks').fetchone()['total']
        if current_total + percentage <= 100:
            conn.execute(
                'INSERT INTO stocks (symbol, company, percentage, rationale) VALUES (?, ?, ?, ?)',
                (symbol, company, percentage, rationale)
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
