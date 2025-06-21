#!/bin/bash
# This script will run the database migration on Heroku

echo "Running database migration on Heroku..."
echo "Uploading changes to Heroku..."
git add .
git commit -m "Add database migration scripts"
git push heroku main

echo "Running migration script..."
heroku run python migrate_db.py

echo "Restarting application..."
heroku restart

echo "Migration completed! Check application status:"
heroku logs --tail
