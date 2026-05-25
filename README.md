# Smart Folio

A simple single-page stock portfolio tracker. Add stocks with your rationale and track them in a clean table.

## Features

- Add stocks with symbol, company name, quantity, price, and rationale
- View all stocks in a table with calculated values
- Delete stocks from your portfolio
- Total portfolio value calculation

## Quick Start

```bash
# Install Flask
pip install flask

# Run the app
python app.py
```

Open http://localhost:5000 in your browser.

## Project Structure

```
smart-folio/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Single page UI
├── portfolio.db        # SQLite database (auto-created)
├── requirements.txt
└── README.md
```

## License

MIT
