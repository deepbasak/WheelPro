# Heroku Database Migration Guide

This guide explains how to run the database migration script to add the new fields required for the wheel filtering functionality.

## Issue

The application is currently crashing because the `products` table in the database doesn't have the new columns that were added to the `Product` model:

- `design_type`
- `vehicle_type`
- `series`
- `is_new_stock`

## Running the Migration

There are two ways to run the migration:

### Method 1: Run Locally

1. Push your code changes to Heroku:

```bash
git add .
git commit -m "Add database migration script"
git push heroku main
```

2. Run the migration script using Heroku CLI:

```bash
heroku run python migrate_db.py
```

### Method 2: Run Directly on Heroku

You can also run a one-off command to execute the migration:

```bash
heroku run python -c "from migrate_db import run_migration; run_migration()"
```

## Verify the Migration

After running the migration, you can verify that the columns were added by running:

```bash
heroku pg:psql
```

Then, in the PostgreSQL shell:

```sql
\d products
```

This will show the table schema with the new columns.

## Restart the Application

Finally, restart the application to apply the changes:

```bash
heroku restart
```

## Troubleshooting

If you encounter any issues, check the Heroku logs:

```bash
heroku logs --tail
```

If the application continues to crash, you might need to drop the table and let SQLAlchemy recreate it:

```bash
heroku pg:psql
```

Then in the PostgreSQL shell:

```sql
DROP TABLE products CASCADE;
```

After that, restart the application. SQLAlchemy will recreate the table with the correct schema.
