# PostgreSQL Migration Guide - Social Media API

## Overview

This guide explains how to migrate from SQLite to PostgreSQL for persistent data storage. PostgreSQL is essential for production deployment on Heroku because:

- **SQLite on Heroku is ephemeral** - All data is lost every 24 hours when dynos restart
- **PostgreSQL is persistent** - Data survives restarts, deployments, and scaling
- **PostgreSQL is production-ready** - Better performance, concurrency, and reliability

---

## ✅ What's Already Done

Your project is **already configured** for PostgreSQL! Here's what's in place:

1. ✅ **psycopg2-binary** (PostgreSQL adapter) installed in `requirements.txt`
2. ✅ **dj-database-url** (Database URL parser) installed
3. ✅ **settings.py** configured to auto-detect and use PostgreSQL

Your `settings.py` now supports **three modes**:

### Mode 1: SQLite (Default - Local Development)
```python
# No environment variables needed
# Uses: alx_social_media.sqlite3
```

### Mode 2: PostgreSQL via DATABASE_URL (Heroku Production)
```python
# Automatically used when DATABASE_URL exists
# Heroku sets this automatically when you add PostgreSQL addon
```

### Mode 3: Local PostgreSQL (Optional Development)
```python
# Set USE_POSTGRESQL=True to use local PostgreSQL
# Configure with DB_NAME, DB_USER, DB_PASSWORD, etc.
```

---

## 🚀 Deploying to Heroku with PostgreSQL

### Step 1: Add PostgreSQL to Your Heroku App

```bash
# Add PostgreSQL addon (choose a plan)
heroku addons:create heroku-postgresql:mini --app social-media-api-deninjo
```

**Available Plans:**
- `mini` - $5/month - 10,000 rows (perfect for small projects)
- `basic` - $9/month - 10 million rows
- `hobby-dev` - Free tier (limited to 10,000 rows, may be deprecated)

### Step 2: Verify PostgreSQL Was Added

```bash
# Check DATABASE_URL was set
heroku config --app social-media-api-deninjo | grep DATABASE_URL

# Check addon status
heroku addons --app social-media-api-deninjo
```

You should see output like:
```
DATABASE_URL: postgres://username:password@host:5432/database_name
```

### Step 3: Deploy Your Code (If Not Already Done)

```bash
# Commit any changes
git add .
git commit -m "Configure PostgreSQL support"

# Push to Heroku
git push heroku master
```

### Step 4: Run Migrations on PostgreSQL

```bash
# Apply all migrations to the new PostgreSQL database
heroku run "cd social_media_api && python manage.py migrate" --app social-media-api-deninjo

# Verify migrations
heroku run "cd social_media_api && python manage.py showmigrations" --app social-media-api-deninjo
```

### Step 5: Create a New Superuser

```bash
# Create admin account (previous SQLite superuser is gone)
heroku run "cd social_media_api && python manage.py createsuperuser" --app social-media-api-deninjo
```

Follow the prompts to set username, email, and password.

### Step 6: Verify Everything Works

```bash
# Check app status
heroku ps --app social-media-api-deninjo

# Open your app
heroku open --app social-media-api-deninjo

# Test the admin panel
# Navigate to: https://social-media-api-deninjo.herokuapp.com/admin/
```

---

## 🎉 Success! Your Data Is Now Persistent

After completing these steps:
- ✅ All data is stored in PostgreSQL
- ✅ Data survives dyno restarts
- ✅ Data survives deployments
- ✅ No more 24-hour data loss
- ✅ Production-ready database

---

## 🖥️ Optional: Using PostgreSQL Locally

If you want to develop with PostgreSQL locally (optional):

### Step 1: Install PostgreSQL

**macOS:**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download installer from: https://www.postgresql.org/download/windows/

### Step 2: Create Local Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE social_media_db;
CREATE USER social_media_user WITH PASSWORD 'your_secure_password';
ALTER ROLE social_media_user SET client_encoding TO 'utf8';
ALTER ROLE social_media_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE social_media_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO social_media_user;

# Exit
\q
```

### Step 3: Configure Environment Variables

Create a `.env` file in your project root:

```bash
USE_POSTGRESQL=True
DB_NAME=social_media_db
DB_USER=social_media_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

**Note:** Add `.env` to your `.gitignore` to keep passwords secret!

### Step 4: Load Environment Variables and Migrate

```bash
# Load environment variables (one-time per terminal session)
export $(cat .env | xargs)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## 📊 Accessing Your PostgreSQL Database

### On Heroku (Production)

#### Method 1: Using Heroku CLI

```bash
# Open PostgreSQL shell
heroku pg:psql --app social-media-api-deninjo
```

Once connected, you can run SQL queries:

```sql
-- List all tables
\dt

-- View all users
SELECT * FROM accounts_user;

-- View all posts
SELECT * FROM posts_post;

-- Count users
SELECT COUNT(*) FROM accounts_user;

-- View recent posts with author info
SELECT p.id, p.title, p.content, u.username, p.created_at 
FROM posts_post p 
JOIN accounts_user u ON p.author_id = u.id 
ORDER BY p.created_at DESC 
LIMIT 10;

-- Exit
\q
```

#### Method 2: Using Django Shell

```bash
# Open Python shell with Django environment
heroku run "cd social_media_api && python manage.py shell" --app social-media-api-deninjo
```

Then run Python/Django ORM commands:

```python
# Import models
from accounts.models import User
from posts.models import Post, Like
from notifications.models import Notification

# View all users
users = User.objects.all()
for user in users:
    print(f"{user.username} - {user.email}")

# View all posts
posts = Post.objects.all()
for post in posts:
    print(f"{post.title} by {post.author.username}")

# Get specific user
user = User.objects.get(username='admin')
print(user.bio)

# Get user's posts
user_posts = Post.objects.filter(author=user)
print(f"{user.username} has {user_posts.count()} posts")

# Create a new post
post = Post.objects.create(
    author=user,
    title="My First Post",
    content="Hello from PostgreSQL!"
)

# Exit shell
exit()
```

#### Method 3: Database GUI Tools

Get your database credentials:

```bash
heroku config:get DATABASE_URL --app social-media-api-deninjo
```

This returns a URL like:
```
postgres://username:password@hostname:5432/database_name
```

Use these credentials with GUI tools like:
- **pgAdmin** (https://www.pgadmin.org/)
- **TablePlus** (https://tableplus.com/)
- **DBeaver** (https://dbeaver.io/)

---

### On Local PostgreSQL

#### Method 1: Command Line (psql)

```bash
# Connect to your database
psql -U social_media_user -d social_media_db

# Run SQL queries (same as above)
\dt
SELECT * FROM accounts_user;
\q
```

#### Method 2: Django Shell

```bash
# Make sure environment variables are set
export $(cat .env | xargs)

# Open Django shell
python manage.py shell

# Run Django ORM commands (same as above)
```

#### Method 3: Django Admin Panel

```bash
# Run server
python manage.py runserver

# Open browser to:
# http://localhost:8000/admin/
```

---

## 🔧 Common PostgreSQL Commands

### Database Management

```bash
# View database info
heroku pg:info --app social-media-api-deninjo

# View database credentials
heroku pg:credentials:url --app social-media-api-deninjo

# View database size
heroku pg:psql --app social-media-api-deninjo -c "SELECT pg_size_pretty(pg_database_size('DATABASE_NAME'));"
```

### Backup and Restore

```bash
# Create manual backup
heroku pg:backups:capture --app social-media-api-deninjo

# List all backups
heroku pg:backups --app social-media-api-deninjo

# Download backup to local file
heroku pg:backups:download --app social-media-api-deninjo

# Restore from backup
heroku pg:backups:restore BACKUP_ID DATABASE_URL --app social-media-api-deninjo

# Schedule automatic daily backups
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/Los_Angeles' --app social-media-api-deninjo
```

### Database Reset (⚠️ WARNING: Deletes All Data)

```bash
# Reset database (destroys all data)
heroku pg:reset DATABASE_URL --app social-media-api-deninjo --confirm social-media-api-deninjo

# Run migrations again
heroku run "cd social_media_api && python manage.py migrate" --app social-media-api-deninjo

# Create new superuser
heroku run "cd social_media_api && python manage.py createsuperuser" --app social-media-api-deninjo
```

---

## 📈 Monitoring Your Database

### Check Connection Count

```bash
heroku pg:psql --app social-media-api-deninjo -c "SELECT count(*) FROM pg_stat_activity;"
```

### Check Table Sizes

```bash
heroku pg:psql --app social-media-api-deninjo -c "
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

### View Recent Activity

```bash
heroku pg:psql --app social-media-api-deninjo -c "
SELECT 
    datname, 
    usename, 
    application_name, 
    state, 
    query 
FROM pg_stat_activity 
WHERE datname = current_database();"
```

---

## 🚨 Troubleshooting

### Issue: "DATABASE_URL not found"

**Solution:** Make sure you've added the PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:mini --app social-media-api-deninjo
```

### Issue: "could not connect to server"

**Solution:** Check if PostgreSQL addon is active:
```bash
heroku addons:info heroku-postgresql --app social-media-api-deninjo
```

### Issue: "relation does not exist"

**Solution:** Run migrations:
```bash
heroku run "cd social_media_api && python manage.py migrate" --app social-media-api-deninjo
```

### Issue: Local PostgreSQL connection refused

**Solution:** Start PostgreSQL service:
```bash
# macOS
brew services start postgresql@16

# Ubuntu/Linux
sudo systemctl start postgresql
```

---

## 🎓 Understanding the Database Configuration

### How Django Chooses the Database

Your `settings.py` now has this smart configuration:

```python
# 1. Default: SQLite (no env vars needed)
DATABASES = {'default': {...sqlite3...}}

# 2. If DATABASE_URL exists → Use it (Heroku auto-sets this)
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(...)

# 3. If USE_POSTGRESQL=True → Use local PostgreSQL
elif os.environ.get('USE_POSTGRESQL') == 'true':
    DATABASES = {'default': {...postgresql...}}
```

**Priority Order:**
1. DATABASE_URL (highest priority) - Heroku
2. USE_POSTGRESQL=True - Local PostgreSQL
3. Default SQLite (fallback) - Simple development

---

## ✅ Migration Checklist

Use this checklist to ensure successful PostgreSQL migration:

### Pre-Migration
- [ ] Verify `psycopg2-binary` is in `requirements.txt`
- [ ] Verify `dj-database-url` is in `requirements.txt`
- [ ] Commit all code changes
- [ ] Backup any important SQLite data (if needed)

### Heroku Migration
- [ ] Add PostgreSQL addon: `heroku addons:create heroku-postgresql:mini`
- [ ] Verify `DATABASE_URL` exists: `heroku config | grep DATABASE_URL`
- [ ] Push code to Heroku: `git push heroku master`
- [ ] Run migrations: `heroku run "cd social_media_api && python manage.py migrate"`
- [ ] Create superuser: `heroku run "cd social_media_api && python manage.py createsuperuser"`
- [ ] Test admin panel access
- [ ] Test API endpoints
- [ ] Set up automated backups (optional but recommended)

### Local Development (Optional)
- [ ] Install PostgreSQL locally
- [ ] Create database and user
- [ ] Create `.env` file with credentials
- [ ] Add `.env` to `.gitignore`
- [ ] Test local connection
- [ ] Run migrations locally

---

## 📚 Additional Resources

- **Heroku PostgreSQL Docs:** https://devcenter.heroku.com/categories/heroku-postgres
- **Django PostgreSQL Docs:** https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes
- **dj-database-url:** https://github.com/jazzband/dj-database-url
- **PostgreSQL Tutorial:** https://www.postgresql.org/docs/current/tutorial.html

---

## 🎉 Summary

### What We've Done

1. ✅ **Updated `settings.py`** - Added smart database detection
2. ✅ **Configured three modes** - SQLite, Heroku PostgreSQL, Local PostgreSQL
3. ✅ **Created migration guide** - Step-by-step instructions
4. ✅ **Documented database access** - Multiple methods with examples

### How to Access Your Database

**On Heroku:**
- `heroku pg:psql` - SQL queries
- `heroku run "cd social_media_api && python manage.py shell"` - Django ORM
- GUI tools with `DATABASE_URL` credentials

**Locally:**
- `psql -U user -d database` - SQL queries
- `python manage.py shell` - Django ORM
- `http://localhost:8000/admin/` - Admin panel

### Next Steps

1. Add PostgreSQL addon to Heroku
2. Run migrations on Heroku
3. Create superuser
4. Start using persistent data!

**Your data will now survive forever! No more 24-hour resets! 🎊**

---

**Last Updated:** January 26, 2026
