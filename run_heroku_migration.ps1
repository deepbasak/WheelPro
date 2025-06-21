# This script will run the database migration on Heroku
Write-Host "Running database migration on Heroku..." -ForegroundColor Green
Write-Host "Uploading changes to Heroku..." -ForegroundColor Yellow
git add .
git commit -m "Add database migration scripts"
git push heroku main

Write-Host "Running migration script..." -ForegroundColor Yellow
heroku run python migrate_db.py

Write-Host "Restarting application..." -ForegroundColor Yellow
heroku restart

Write-Host "Migration completed! Check application status:" -ForegroundColor Green
heroku logs --tail
