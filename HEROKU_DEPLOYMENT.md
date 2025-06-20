# Heroku Deployment Guide for WheelPro

This document outlines the steps to deploy this Flask application to Heroku.

## Prerequisites

1. A Heroku account (sign up at https://signup.heroku.com/ if you don't have one)
2. Heroku CLI installed on your computer (https://devcenter.heroku.com/articles/heroku-cli)
3. Git installed on your computer

## Deployment Steps

### 1. Login to Heroku CLI

```bash
heroku login
```

### 2. Initialize a Git Repository (if not done already)

```bash
# Navigate to your project directory
cd path/to/WheelPro

# Initialize Git
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

### 3. Create a Heroku App

```bash
heroku create wheelrpo-app-name  # Replace with your preferred app name
```

### 4. Add a PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:mini
```

### 5. Set Environment Variables

```bash
# Set secret key for Flask sessions
heroku config:set SESSION_SECRET="your-secure-random-string"
```

### 6. Deploy to Heroku

```bash
git push heroku main
```
If your main branch is named 'master' instead, use:
```bash
git push heroku master
```

### 7. Run Database Migrations

The application is set up to initialize the database automatically when it starts.

### 8. Open the Application

```bash
heroku open
```

## Maintenance and Monitoring

- View application logs: `heroku logs --tail`
- Scale your application: `heroku ps:scale web=1`
- Access PostgreSQL database: `heroku pg:psql`

## Troubleshooting

If you encounter issues:

1. Check the logs: `heroku logs --tail`
2. Ensure all required environment variables are set
3. Verify your Procfile is correctly set up
4. Make sure the PostgreSQL add-on is provisioned

## Local Testing of Production Configuration

To test your application with production settings locally:

```bash
# Set environment variables locally
$env:DATABASE_URL = "your-local-postgresql-url"
$env:SESSION_SECRET = "your-secure-random-string"

# Run using Gunicorn
gunicorn app:app
```
