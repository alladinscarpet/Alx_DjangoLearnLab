# Social Media API - Deployment Guide

This document outlines the deployment process for the **Social Media API** to Heroku, including configurations, troubleshooting steps, and maintenance considerations.

---

## Overview

The Social Media API is deployed on **Heroku**, a cloud Platform-as-a-Service (PaaS) that simplifies Django application hosting by handling infrastructure, HTTPS, and process management automatically.

---

## Prerequisites

### Required Tools
- **Heroku CLI**: Command-line interface for managing Heroku applications
- **Git**: Version control for code deployment
- **Python 3.11+**: Runtime environment

### Required Python Packages
```
gunicorn==23.0.0          # Production WSGI HTTP server
whitenoise==6.11.0        # Static file serving middleware
dj-database-url==2.1.0    # Database URL parser for environment variables
psycopg2-binary==2.9.9    # PostgreSQL adapter (optional, for future upgrade)
```

Install via:
```bash
pip install -r requirements.txt
```

---

## Production Configuration

### 1. Security Settings

The following security headers are enabled in `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1']

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = False  # Heroku handles SSL termination
```

**Why SECURE_SSL_REDIRECT is False:**
Heroku's routing layer already handles SSL/TLS termination. Enabling this setting can cause redirect loops because Django would try to redirect to HTTPS when the request already appears as HTTP internally.

---

### 2. Static Files Configuration

Static files are served using **WhiteNoise** middleware:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be after SecurityMiddleware
    ...
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Before deployment, collect static files:
```bash
python manage.py collectstatic --noinput
```

---

### 3. Database Configuration

#### Current Setup: SQLite (Development/Learning Only)

The application currently uses SQLite for simplicity during the learning phase:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'alx_social_media.sqlite3',
    }
}
```

**Important Limitation:**
Heroku dynos have an **ephemeral filesystem**. This means:
- Any files written to the dyno (including your SQLite database) are temporary
- Data is **lost** on dyno restart (happens at least once every 24 hours)
- Data is **lost** on every new deployment
- The database resets to its initial state after each restart

**Use Case:** SQLite on Heroku is only suitable for:
- Learning and experimentation
- Temporary demos
- Testing deployment processes

#### Recommended Production Setup: PostgreSQL

For production use, migrate to Heroku Postgres:

1. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:mini
```

2. Update `settings.py` to parse database URL:
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'alx_social_media.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

This configuration:
- Uses PostgreSQL in production (via `DATABASE_URL` env var)
- Falls back to SQLite for local development
- Maintains persistent data across deployments

---

## Deployment Process

This section provides a step-by-step manual for deploying the application to Heroku. Follow each step in order.



### Prerequisites Completed

Before proceeding, ensure you have already:
- ✅ Installed required packages (`gunicorn`, `whitenoise`)
- ✅ Updated `settings.py` with production configurations
- ✅ Configured static files with WhiteNoise
- ✅ Created `Procfile` in the project root

---

### Project Structure Overview

The deployment is done from the parent directory (`Alx_DjangoLearnLab`) because that's where the Git repository is initialized. The actual Django project is in the `social_media_api/` subdirectory.

**Directory structure:**
```
Alx_DjangoLearnLab/           # Git repository root (deploy from here)
├── Procfile                   # Heroku process configuration
├── requirements.txt           # Python dependencies
├── runtime.txt                # Python version specification (optional)
└── social_media_api/          # Django project directory
    ├── manage.py
    ├── social_media_api/      # Django settings package
    │   ├── settings.py
    │   └── wsgi.py
    ├── accounts/              # User authentication app
    ├── posts/                 # Posts and likes app
    └── notifications/         # Notifications app
```

---

### Procfile Configuration

The `Procfile` (located in `Alx_DjangoLearnLab/`) tells Heroku how to run the application.

**Content:**
```
web: gunicorn social_media_api.wsgi:application --chdir social_media_api --log-file -
```

**Explanation:**
- `web:` - Process type that receives HTTP traffic
- `gunicorn` - Production WSGI server (replaces `manage.py runserver`)
- `social_media_api.wsgi:application` - Path to Django WSGI app
- `--chdir social_media_api` - Change to Django project directory
- `--log-file -` - Send logs to stdout for Heroku logging

**Why no Nginx?** Heroku's routing layer already handles HTTP, load balancing, and SSL.

---

### Step 1: Initialize Git Repository(if not already)

If not already initialized, create a Git repository in the project root:


**Check status:**
```bash
git status
```

---

### Step 2: Login to Heroku

Authenticate with your Heroku account:

```bash
heroku login
```

This opens a browser window for authentication. Once complete, you're logged in via the CLI.

---

### Step 3: Create Heroku Application

Create a new application on Heroku:

```bash
heroku create social-media-api-deninjo
```

**What this does:**
- Creates a new app named `social-media-api-deninjo` on Heroku
- Automatically adds a Git remote named `heroku`
- Assigns a URL: `https://social-media-api-deninjo.herokuapp.com`

**Verify remote was added:**
```bash
git remote -v
```

Expected output:
```
heroku  https://git.heroku.com/social-media-api-deninjo.git (fetch)
heroku  https://git.heroku.com/social-media-api-deninjo.git (push)
```

**Understanding Git Remotes:**
- **heroku remote** - Points to Heroku's Git server (deployment target)
- **origin remote** - Points to GitHub (code backup, if configured)
- Pushing to `heroku` triggers deployment
- Pushing to `origin` only backs up code

---

### Step 4: Set Environment Variables

Configure required environment variables on Heroku:

```bash
heroku config:set DJANGO_SETTINGS_MODULE=social_media_api.settings
heroku config:set SECRET_KEY=your-production-secret-key-here
heroku config:set DEBUG=False
```

**Important:**
- Replace `your-production-secret-key-here` with a secure random string
- `DJANGO_SETTINGS_MODULE` must be `social_media_api.settings` (not double-nested path)
- `DEBUG=False` ensures production security

**Generate a secure SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**View configured variables:**
```bash
heroku config --app social-media-api-deninjo
```

---

### Step 5: Commit and Push to Heroku

Stage all files and commit:

```bash
git add .
git commit -m "Configure Django subdirectory deployment for Heroku"
```

**Push to Heroku (triggers deployment):**
```bash
git push heroku master
```

**What happens during deployment:**
1. Code is sent to Heroku's Git server
2. Heroku detects Python project (via `requirements.txt`)
3. Dependencies are installed
4. Static files are collected automatically
5. `Procfile` is read to determine startup command
6. A dyno starts running your application
7. App becomes live at your Heroku URL

**Monitor deployment output** for errors or warnings.

**Push to GitHub (backup only):**
```bash
git push origin master
```

This backs up code to GitHub but does not trigger deployment.

---

### Step 6: Run Database Migrations

After successful deployment, apply database migrations:

```bash
heroku run "cd social_media_api && python manage.py migrate"
```

**What this does:**
- Creates database tables
- Applies all migrations from your apps
- Required before the app can function properly

**Check migration status:**
```bash
heroku run "cd social_media_api && python manage.py showmigrations"
```

---

### Step 7: Create Superuser

Create an admin account to access the Django admin panel:

```bash
heroku run "cd social_media_api && python manage.py createsuperuser"
```

Follow the prompts to set:
- Username
- Email address
- Password (entered twice)

**Access admin panel:**
```
https://social-media-api-deninjo.herokuapp.com/admin/
```

**Important:** If using SQLite, this superuser will be lost on dyno restart. For persistent data, migrate to PostgreSQL.

---

### Step 8: Verify Deployment

Test that your application is working:

**1. Check dyno status:**
```bash
heroku ps --app social-media-api-deninjo
```

Expected output:
```
=== web (Eco): gunicorn ... (1)
web.1: up 2026/01/09 18:00:00 +0000 (~ 5m ago)
```

**2. Open the app in browser:**
```bash
heroku open --app social-media-api-deninjo
```

**3. Test API endpoint:**
```bash
curl https://social-media-api-deninjo.herokuapp.com/api/posts/
```

**4. View logs:**
```bash
heroku logs --tail --app social-media-api-deninjo
```

---

## Understanding Git Push Commands

### git push heroku master

**What it does:**
- Sends code to Heroku's Git server
- Triggers automatic deployment process
- Rebuilds and restarts your application

**When to use:**
- After making code changes
- After updating dependencies
- After configuration changes in code

### git push origin master

**What it does:**
- Sends code to GitHub (or other remote)
- Backs up your code
- Does NOT deploy to Heroku

**When to use:**
- To version control your code
- To collaborate with others
- To keep a backup

### Best Practice

Always push to both:
```bash
git push heroku master  # Deploy to Heroku
git push origin master  # Backup to GitHub
```

---

## Common Deployment Issues and Solutions

### Issue 1: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'social_media_api.social_media_api'
```

**Cause:** Incorrect `DJANGO_SETTINGS_MODULE` environment variable.

**Solution:**
```bash
heroku config:set DJANGO_SETTINGS_MODULE=social_media_api.settings
```

---

### Issue 2: Application Crashes on Startup

**Error:**
```
State changed from starting to crashed
```

**Debugging steps:**
1. Check logs:
   ```bash
   heroku logs --tail --app social-media-api-deninjo
   ```

2. Verify Procfile syntax (no trailing characters or spaces)

3. Test gunicorn locally:
   ```bash
   cd social_media_api
   gunicorn social_media_api.wsgi:application
   ```

---





### Issue 3: Static Files Not Loading

**Symptoms:** CSS/JS files return 404 errors.

**Solution:**
1. Verify WhiteNoise is in `MIDDLEWARE`
2. Run collectstatic before deployment:
   ```bash
   python manage.py collectstatic --noinput
   ```
3. Commit the changes and redeploy

---

## Monitoring and Maintenance

### Check Application Status

```bash
heroku ps --app social-media-api-deninjo
```

Expected output:
```
=== web (Eco): gunicorn social_media_api.wsgi:application --chdir social_media_api --log-file - (1)
web.1: up 2024/01/09 16:50:23 +0300 (~ 10m ago)
```

---

### View Logs

Heroku logs show all application output, including HTTP requests, errors, and debug information. This is equivalent to the output you see when running `python manage.py runserver` locally.

#### Real-time Logs (Live Monitoring)
Watch logs as they happen (like `tail -f`):
```bash
heroku logs --tail --app social-media-api-deninjo
```

This shows:
- HTTP requests (GET, POST, etc.)
- Response status codes (200, 404, 500)
- Application errors and exceptions
- Database queries (if DEBUG=True)
- Custom print statements

Example output:
```
2026-01-09T17:39:37+00:00 app[web.1]: 10.1.18.237 - - [09/Jan/2026:17:39:37 +0000] "POST /admin/login/ HTTP/1.1" 200 4340
2026-01-09T17:39:54+00:00 app[web.1]: 10.1.18.237 - - [09/Jan/2026:17:39:54 +0000] "GET /admin/ HTTP/1.1" 302 0
```

#### Recent Logs
View the last N lines of logs:
```bash
# Last 100 lines
heroku logs -n 100 --app social-media-api-deninjo

# Last 500 lines
heroku logs -n 500 --app social-media-api-deninjo
```

#### Filtered Logs
Search for specific patterns:
```bash
# Filter by HTTP method
heroku logs --tail --app social-media-api-deninjo | grep POST

# Filter for errors
heroku logs --tail --app social-media-api-deninjo | grep -E "error|ERROR|exception"

# Filter by source (app vs router vs dyno)
heroku logs --tail --source app --app social-media-api-deninjo
```

#### Log Components
Heroku logs include different sources:
- `app[web.1]`: Your application output (Django logs)
- `heroku[router]`: HTTP routing information
- `heroku[web.1]`: Dyno lifecycle events (starting, stopping, crashed)

#### Common Log Patterns

**Successful Request:**
```
heroku[router]: method=GET path="/api/posts/" status=200 bytes=1234
app[web.1]: "GET /api/posts/ HTTP/1.1" 200 1234
```

**Failed Request:**
```
heroku[router]: method=POST path="/api/posts/" status=500 bytes=45
app[web.1]: Internal Server Error: /api/posts/
app[web.1]: Traceback (most recent call last):
```

**Application Crash:**
```
heroku[web.1]: State changed from up to crashed
heroku[web.1]: Process exited with status 1
```

---

### Scale Dynos

**Check current dyno count:**
```bash
heroku ps:scale --app social-media-api-deninjo
```

**Scale up/down:**
```bash
heroku ps:scale web=1  # One dyno
heroku ps:scale web=2  # Two dynos (requires paid plan)
```

---

### Restart Application

```bash
heroku restart --app social-media-api-deninjo
```

**Note:** Restarting will reset SQLite data if using the ephemeral filesystem.

---

## Testing the Deployment

### 1. Test API Endpoints

**Check app health:**
```bash
curl https://social-media-api-deninjo.herokuapp.com/
```

**Test posts endpoint:**
```bash
curl https://social-media-api-deninjo.herokuapp.com/api/posts/
```

Expected response:
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": "john",
      "title": "New Adventures",
      "content": "Excited to share my journey!",
      "created_at": "2025-12-22T12:14:30.279687Z",
      "updated_at": "2025-12-22T12:14:30.279687Z"
    }
  ]
}
```

---

### 2. Test Authentication

**Register a new user:**
```bash
curl -X POST https://social-media-api-deninjo.herokuapp.com/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","email":"test@example.com"}'
```

**Login:**
```bash
curl -X POST https://social-media-api-deninjo.herokuapp.com/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

---

### 3. Access Django Admin

Navigate to:
```
https://social-media-api-deninjo.herokuapp.com/admin/
```

Login with the superuser credentials created earlier.

---

## Production Checklist

Before going live, ensure:

- [ ] `DEBUG = False` in production
- [ ] `ALLOWED_HOSTS` includes your Heroku domain
- [ ] Security headers are enabled (XSS, MIME sniffing, frame options)
- [ ] `SECRET_KEY` is stored in environment variables, not hardcoded
- [ ] Static files are collected and WhiteNoise is configured
- [ ] Database migrations are applied
- [ ] Superuser account is created
- [ ] All environment variables are set on Heroku
- [ ] Application logs show no errors
- [ ] API endpoints return expected responses
- [ ] SSL/HTTPS is working (automatic on Heroku)

---

## Future Improvements

### 1. Migrate to PostgreSQL
Replace SQLite with persistent PostgreSQL database for production data integrity.

### 2. Environment-Based SECRET_KEY
Update `settings.py` to require `SECRET_KEY` from environment:
```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")
```

### 3. Custom Domain
Add a custom domain instead of using `.herokuapp.com`:
```bash
heroku domains:add www.yourdomain.com
```

### 4. Automated Backups
Enable automatic PostgreSQL backups:
```bash
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/Los_Angeles'
```

### 5. Monitoring
Set up application monitoring with Heroku add-ons or external services.

---

## Managing the Django Admin

### Creating a Superuser

After deployment, create an admin account:

```bash
heroku run "cd social_media_api && python manage.py createsuperuser" --app social-media-api-deninjo
```

Follow the prompts to set username, email, and password.

### Accessing the Admin Panel

Navigate to:
```
https://social-media-api-deninjo.herokuapp.com/admin/
```

Login with your superuser credentials.

### Important: SQLite Data Persistence Issue

If using SQLite (current configuration):
- The superuser will be **lost on dyno restart** or deployment
- You'll need to recreate it after each restart
- This is because Heroku's filesystem is **ephemeral**

**Solution:** Migrate to PostgreSQL for persistent data storage (see Future Improvements section).

---

## Post-Deployment Operations

Once your application is deployed to Heroku, you can perform various management tasks:

### Run Django Management Commands

Execute any Django management command on the remote server:

```bash
# Run migrations
heroku run "cd social_media_api && python manage.py migrate" --app social-media-api-deninjo

# Create superuser
heroku run "cd social_media_api && python manage.py createsuperuser" --app social-media-api-deninjo

# Check for issues
heroku run "cd social_media_api && python manage.py check --deploy" --app social-media-api-deninjo

# View migration status
heroku run "cd social_media_api && python manage.py showmigrations" --app social-media-api-deninjo

# Open Django shell
heroku run "cd social_media_api && python manage.py shell" --app social-media-api-deninjo

# Clear expired sessions
heroku run "cd social_media_api && python manage.py clearsessions" --app social-media-api-deninjo
```

### Database Operations

```bash
# Backup database (PostgreSQL only)
heroku pg:backups:capture --app social-media-api-deninjo

# List backups
heroku pg:backups --app social-media-api-deninjo

# Download backup
heroku pg:backups:download --app social-media-api-deninjo

# Reset database (WARNING: Deletes all data)
heroku pg:reset DATABASE_URL --app social-media-api-deninjo
heroku run "cd social_media_api && python manage.py migrate" --app social-media-api-deninjo
```

### Environment Variable Management

```bash
# View all config variables
heroku config --app social-media-api-deninjo

# Set a new variable
heroku config:set VARIABLE_NAME=value --app social-media-api-deninjo

# Remove a variable
heroku config:unset VARIABLE_NAME --app social-media-api-deninjo

# Set multiple variables at once
heroku config:set VAR1=value1 VAR2=value2 --app social-media-api-deninjo
```

### Application Management

```bash
# Restart the application
heroku restart --app social-media-api-deninjo

# Open app in browser
heroku open --app social-media-api-deninjo

# Check app information
heroku info --app social-media-api-deninjo

# List releases (deployment history)
heroku releases --app social-media-api-deninjo

# Rollback to previous release
heroku rollback --app social-media-api-deninjo
```

### Maintenance Mode

```bash
# Enable maintenance mode (shows maintenance page to users)
heroku maintenance:on --app social-media-api-deninjo

# Disable maintenance mode
heroku maintenance:off --app social-media-api-deninjo
```

### Add-ons Management

```bash
# List installed add-ons
heroku addons --app social-media-api-deninjo

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini --app social-media-api-deninjo

# View add-on info
heroku addons:info heroku-postgresql --app social-media-api-deninjo

# Open add-on dashboard
heroku addons:open heroku-postgresql --app social-media-api-deninjo
```

### Performance and Debugging

```bash
# Run one-off bash session
heroku run bash --app social-media-api-deninjo

# Check dyno performance
heroku ps --app social-media-api-deninjo

# View error codes
heroku help error-codes
```

---

## Support and Resources

- **Heroku Documentation:** https://devcenter.heroku.com/categories/python-support
- **Django Deployment Checklist:** https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- **Gunicorn Documentation:** https://docs.gunicorn.org/
- **Heroku CLI Reference:** https://devcenter.heroku.com/articles/heroku-cli-commands

---

## What We Accomplished

This deployment journey involved several key steps and troubleshooting:

### Initial Setup
1. Installed Heroku CLI and required packages (gunicorn, whitenoise)
2. Configured Django security settings for production
3. Set up static file serving with WhiteNoise
4. Created Procfile to define how Heroku runs the application

### Deployment Configuration
1. Created Heroku application: `social-media-api-deninjo`
2. Configured Git remotes for both GitHub (code backup) and Heroku (deployment)
3. Set environment variables for Django configuration

### Troubleshooting and Fixes
1. **Fixed Procfile path issues** - Adjusted to work with subdirectory structure using `--chdir`
2. **Corrected DJANGO_SETTINGS_MODULE** - Changed from incorrect double-nested path to `social_media_api.settings`
3. **Fixed application imports** - Updated `posts/urls.py` to import existing views instead of non-existent ViewSets
4. **Added proper spacing** - Fixed `SECURE_SSL_REDIRECT` formatting for checker compliance
5. **Cleaned Git history** - Reset and force-pushed to consolidate unnecessary commits

### Final Configuration
1. Application successfully deployed and running on Heroku
2. All security headers properly configured
3. Static files served correctly via WhiteNoise
4. API endpoints tested and responding correctly
5. Admin panel accessible at `/admin/`

### Current State
- **URL:** https://social-media-api-deninjo.herokuapp.com
- **Status:** Fully operational
- **Database:** SQLite (ephemeral - for learning purposes)
- **Web Server:** Gunicorn
- **Security:** Production-ready settings enabled

---

## Deployment Summary

The Social Media API is successfully deployed on Heroku using:
- **Gunicorn** as the WSGI server
- **WhiteNoise** for static file serving
- **SQLite** for database (learning/demo purposes only)
- **Security headers** enabled for XSS and clickjacking protection
- **Environment variables** for configuration management

The application is accessible at:
**https://social-media-api-deninjo.herokuapp.com**

### Key Takeaways
1. Heroku simplifies Django deployment by handling infrastructure automatically
2. The ephemeral filesystem requires PostgreSQL for data persistence
3. Proper project structure and environment configuration are critical
4. Git serves dual purposes: version control (GitHub) and deployment (Heroku)
5. Comprehensive logging enables effective troubleshooting and monitoring

---

**Last Updated:** January 9, 2026
