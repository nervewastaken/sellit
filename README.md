# ZestMoney Analytics Dashboard

A comprehensive analytics platform for ZestMoney performance analysis and strategic planning.

## Features

- Executive Dashboard
- Financial Analysis
- Operations Intelligence
- Strategic Planning
- Customer Analytics
- Market Intelligence
- Risk Assessment

## Local Development

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python app.py
```

3. Open browser to `http://localhost:8050`

## Heroku Deployment

1. Install Heroku CLI
2. Login to Heroku: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`

## Environment Variables

- `PORT`: Port number (set by Heroku)
- `HOST`: Host address (default: 0.0.0.0)
- `DEBUG`: Debug mode (default: False)

## Technology Stack

- Python 3.11
- Dash & Plotly
- Bootstrap Components
- Gunicorn (Production)
