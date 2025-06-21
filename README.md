# OnyxForged - Premium Wheel Store

OnyxForged is a web application for a premium wheel rim store, featuring product browsing, filtering, and quote requests.

## Features

- Modern UI with yellow/red theme
- Product showcase with detailed specifications
- Filter products by design type, vehicle type, and wheel series
- Quote request system
- Admin dashboard for managing products and quotes

## Setup and Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`

## Database Management

### Checking Database Schema

Before running the application, you can check if your database schema is up to date:

```bash
python check_db.py
```

This will check if all required columns exist in your database and prompt you to run the migration if needed.

### Running Database Migrations

If you see errors about missing columns, you need to run the database migration script:

```bash
python migrate_db.py
```

This will:
1. Add any missing columns to the products table
2. Update existing products with appropriate values for design type, vehicle type, and series
3. Mark some products as new stock

### Heroku Deployment

For Heroku deployment information, see [HEROKU_DEPLOYMENT.md](HEROKU_MIGRATION.md).

## Project Structure

- `app.py`: Main application file
- `routes.py`: Route definitions and view functions
- `models.py`: Database models
- `forms.py`: Form definitions for data input
- `data_store.py`: Static data and sample data initialization
- `static/`: Static files (CSS, JS, images)
- `templates/`: HTML templates
- `migrate_db.py`: Database migration script
- `check_db.py`: Database schema check script
