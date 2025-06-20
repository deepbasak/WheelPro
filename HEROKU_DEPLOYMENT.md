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

# Set Cloudinary environment variables
heroku config:set CLOUDINARY_CLOUD_NAME="your-cloud-name"
heroku config:set CLOUDINARY_API_KEY="your-api-key"
heroku config:set CLOUDINARY_API_SECRET="your-api-secret"
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

## Setting Up Cloudinary for File Storage

This application uses Cloudinary for storing uploaded images to ensure they persist between Heroku dyno restarts.

### 1. Create a Cloudinary Account

1. Sign up for a free Cloudinary account at https://cloudinary.com/users/register/free
2. After registration, go to your Cloudinary dashboard

### 2. Get Your Cloudinary Credentials

From your Cloudinary dashboard, note down the following:
- Cloud Name
- API Key
- API Secret

### 3. Configure Cloudinary in Heroku

Set the Cloudinary environment variables in Heroku:

```bash
heroku config:set CLOUDINARY_CLOUD_NAME="your-cloud-name"
heroku config:set CLOUDINARY_API_KEY="your-api-key"
heroku config:set CLOUDINARY_API_SECRET="your-api-secret"
```

### 4. Verify Configuration

After deployment, upload a test image and verify that it is being stored in Cloudinary by:
1. Checking the Cloudinary dashboard for the uploaded image
2. Confirming that the image URL starts with your Cloudinary domain

## Adding Cloudinary via Heroku Add-ons (Recommended)

The easiest way to add Cloudinary to your Heroku app is through the Heroku add-ons marketplace:

1. **Log in to Heroku Dashboard**: https://dashboard.heroku.com

2. **Navigate to your app**: Select your app from the dashboard

3. **Go to the Resources tab**: From your app's dashboard, click on "Resources" in the top navigation

4. **Add Cloudinary Add-on**:
   - In the "Add-ons" section, click on "Find more add-ons"
   - Search for "Cloudinary" in the search box
   - Select the Cloudinary add-on
   - Choose a plan (the "Starter" plan is free and sufficient for most small applications)
   - Click "Submit Order Form"

5. **Verify Installation**:
   - Once installed, Cloudinary will appear in your add-ons list
   - The add-on automatically sets the `CLOUDINARY_URL` environment variable
   - No need to manually configure the Cloudinary credentials!

This method is preferred over manual configuration as it simplifies the setup process and provides direct access to your Cloudinary dashboard from Heroku.

## Local Testing of Production Configuration

To test your application with production settings locally:

```bash
# Set environment variables locally
$env:DATABASE_URL = "your-local-postgresql-url"
$env:SESSION_SECRET = "your-secure-random-string"

# Run using Gunicorn
gunicorn app:app
```
