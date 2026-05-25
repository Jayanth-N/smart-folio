# Smart Folio

A simple single-page portfolio allocation tracker with a beautiful pie chart visualization.

## Features

- Add stocks with symbol, company name, percentage allocation, and rationale
- Interactive doughnut chart showing portfolio allocation
- Unallocated portion automatically calculated and displayed
- Prevents allocation from exceeding 100%
- Dark themed modern UI

## Quick Start

```bash
pip install flask
python app.py
```

Open http://localhost:5001

## Screenshot

The app shows:
- **Pie Chart**: Visual breakdown of your portfolio allocation
- **Add Form**: Enter stock details with percentage allocation
- **Holdings Table**: List of all stocks with rationale

## Project Structure

```
smart-folio/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Single page UI with Chart.js
├── portfolio.db        # SQLite database (auto-created)
└── requirements.txt
```

## License

MIT
