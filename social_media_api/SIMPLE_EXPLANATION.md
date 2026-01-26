# Simple Explanation: What We Did & How to Access Your Database

## The Problem 

When you deployed to Heroku with SQLite, **all your data disappeared every 24 hours**. This happened because:

- Heroku "restarts" your app daily (called dyno restart)
- SQLite stores data in a file (`alx_social_media.sqlite3`)
- Heroku's file system is **temporary** - files get deleted on restart
- Result: All users, posts, likes → GONE! 😱

## The Solution: PostgreSQL

PostgreSQL is a **real database server** that stores data separately from your app, so:

- ✅ Data survives restarts
- ✅ Data survives deployments
- ✅ Data is **permanent**
- ✅ Production-ready and reliable

---

## 🔧 What We Changed

### 1. Your `settings.py` Is Now Smarter

We updated your Django settings to automatically choose the right database:

**Before:**
```python
# Always used SQLite (temporary on Heroku)
DATABASES = {'default': {...sqlite3...}}
```

**After:**
```python
# Smart detection - picks the right database automatically!

# Option A: SQLite (when no env vars set) → Local development
DATABASES = {'default': {...sqlite3...}}

# Option B: PostgreSQL via DATABASE_URL → Heroku production
if 'DATABASE_URL' in os.environ:
    use PostgreSQL from Heroku

# Option C: Local PostgreSQL → Advanced local development
elif USE_POSTGRESQL=True:
    use local PostgreSQL server
```

### 2. What This Means

- **On your computer:** Still uses SQLite (easy, no setup needed)
- **On Heroku:** Automatically switches to PostgreSQL (when you add it)
- **Zero code changes needed** - it's all automatic! 🎉

---

## 🚀 How to Activate PostgreSQL on Heroku

Currently, your Heroku app is still using SQLite (temporary). Follow these 4 steps to switch to PostgreSQL:

### Step 1: Add PostgreSQL Database (One-Time Setup)

```bash
heroku addons:create heroku-postgresql:mini --app social-media-api-deninjo
```

**What this does:** 
- Creates a PostgreSQL database for your app
- Costs $5/month (but worth it for persistent data!)
- Automatically sets `DATABASE_URL` environment variable
- Your app will now use PostgreSQL automatically!

### Step 2: Push Your Updated Code

```bash
git add .
git commit -m "Add PostgreSQL support"
git push heroku master
```

**What this does:**
- Sends your updated settings.py to Heroku
- Redeploys your app with PostgreSQL support

### Step 3: Setup the Database Tables

```bash
heroku run "cd social_media_api && python manage.py migrate" --app social-media-api-deninjo
```

**What this does:**
- Creates all your tables (users, posts, likes, notifications) in PostgreSQL
- Just like running migrations locally

### Step 4: Create Admin Account

```bash
heroku run "cd social_media_api && python manage.py createsuperuser" --app social-media-api-deninjo
```

**What this does:**
- Creates your admin user (the old SQLite one is gone)
- Follow prompts to set username/password

**🎉 DONE! Your data is now permanent!**

---

## 📊 How to Access Your Database

We created two comprehensive guides for you:

### Guide 1: `POSTGRESQL_SETUP.md`
- Complete migration instructions
- Troubleshooting tips
- Backup and restore commands
- Local PostgreSQL setup (optional)

### Guide 2: `DATABASE_ACCESS_GUIDE.md`
- Copy-paste commands to access your data
- SQL query examples
- Django ORM (Python) examples
- Quick reference cheat sheet

### Quick Access Methods:

#### Method 1: SQL Queries (PostgreSQL Shell)
```bash
heroku pg:psql --app social-media-api-deninjo
```
Then run SQL:
```sql
SELECT * FROM accounts_user;
SELECT * FROM posts_post;
\q  -- exit
```

#### Method 2: Django Python Shell
```bash
heroku run "cd social_media_api && python manage.py shell" --app social-media-api-deninjo
```
Then run Python:
```python
from accounts.models import User
users = User.objects.all()
for user in users:
    print(user.username)
exit()
```

#### Method 3: Admin Panel (Easiest!)
Just visit:
```
https://social-media-api-deninjo.herokuapp.com/admin/
```
Login with your superuser credentials.

---

## 🎯 Key Concepts Explained Simply

### Database URL
- A special connection string that looks like: `postgres://user:pass@host:5432/dbname`
- Heroku sets this automatically when you add PostgreSQL
- Your Django app reads it and connects to the database
- Think of it like a phone number to reach your database

### Three Database Modes

**Mode 1: SQLite (Default)**
- Used when developing on your computer
- No setup needed
- Data is local to your machine
- Fast and easy for testing

**Mode 2: Heroku PostgreSQL (Production)**
- Used when deployed to Heroku
- Activated when `DATABASE_URL` exists
- Data is permanent and shared
- This is what you want for your live app!

**Mode 3: Local PostgreSQL (Optional)**
- For advanced users who want to test with PostgreSQL locally
- Requires installing PostgreSQL on your computer
- More realistic testing environment

### Migrations
- Django's way of creating/updating database tables
- When you add a new field to a model → create migration → run migrate
- Migrations work the same on SQLite and PostgreSQL
- You've already run them, so your tables exist!

### Persistent vs Ephemeral
- **Ephemeral** = temporary, gets deleted (SQLite on Heroku)
- **Persistent** = permanent, stays forever (PostgreSQL)

---

## 📋 Quick Reference

### Check Current Database Status

**Locally:**
```bash
python manage.py shell
```
```python
from django.conf import settings
print(settings.DATABASES['default']['ENGINE'])
# Shows: django.db.backends.sqlite3
exit()
```

**On Heroku:**
```bash
heroku config --app social-media-api-deninjo | grep DATABASE_URL
```
If you see a URL → PostgreSQL is active ✅  
If nothing → Still using SQLite (temporary) ⚠️

### Common Tasks

**View users:**
```bash
heroku pg:psql --app social-media-api-deninjo -c "SELECT username, email FROM accounts_user;"
```

**Count posts:**
```bash
heroku pg:psql --app social-media-api-deninjo -c "SELECT COUNT(*) FROM posts_post;"
```

**Backup database:**
```bash
heroku pg:backups:capture --app social-media-api-deninjo
```

**View logs:**
```bash
heroku logs --tail --app social-media-api-deninjo
```

---

## 🤔 Frequently Asked Questions

### Q: Will I lose my current data?
**A:** Your current SQLite data is already being lost every 24 hours on Heroku. Once you switch to PostgreSQL, you'll start with a fresh database, but it will be permanent.

### Q: Do I need to change my Django models?
**A:** No! Your models work exactly the same with PostgreSQL. No code changes needed.

### Q: What about local development?
**A:** Keep using SQLite locally (default). It's perfect for development. Only Heroku needs PostgreSQL.

### Q: How much does PostgreSQL cost?
**A:** The `mini` plan is $5/month. Worth it for persistent data! Free tier may exist but has limits.

### Q: Can I test PostgreSQL locally?
**A:** Yes! Follow the "Optional: Using PostgreSQL Locally" section in `POSTGRESQL_SETUP.md`.

### Q: What if something breaks?
**A:** Check `POSTGRESQL_SETUP.md` → Troubleshooting section. Common issues are covered.

### Q: How do I backup my data?
**A:** Run: `heroku pg:backups:capture --app social-media-api-deninjo`

### Q: Can I switch back to SQLite?
**A:** Technically yes, but why would you? You'd lose data every 24 hours again. PostgreSQL is better!

---

## 🎉 Summary

### What We Did:
1. ✅ Updated `settings.py` to support PostgreSQL
2. ✅ Kept SQLite for local development (easy!)
3. ✅ Made database choice automatic (smart!)
4. ✅ Created comprehensive documentation

### What You Need to Do:
1. Add PostgreSQL addon to Heroku (one command)
2. Push your code (git push)
3. Run migrations (one command)
4. Create superuser (one command)
5. **Enjoy permanent data! 🎊**

### Files to Reference:
- `POSTGRESQL_SETUP.md` - Complete setup guide
- `DATABASE_ACCESS_GUIDE.md` - How to access data
- `SIMPLE_EXPLANATION.md` - This file (simple overview)

### The Big Picture:
```
LOCAL DEVELOPMENT          HEROKU PRODUCTION
┌──────────────┐          ┌──────────────┐
│   SQLite     │          │  PostgreSQL  │
│  (temporary) │          │ (PERMANENT!) │
│              │          │              │
│  Easy setup  │  ─────>  │ Survives     │
│  Fast        │  Deploy  │ restarts     │
│  Good enough │          │ Production   │
│  for dev     │          │ ready        │
└──────────────┘          └──────────────┘
```

---

**You're all set! Your data will now persist forever on Heroku! 🚀**

**Questions?** Check `POSTGRESQL_SETUP.md` or `DATABASE_ACCESS_GUIDE.md`

---

**Last Updated:** January 26, 2026
