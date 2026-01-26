# Database Access Quick Reference Guide

## Quick Start: Accessing Your Database

This guide provides **copy-paste commands** to quickly access and query your PostgreSQL database.



## Heroku (Production Database)

### Access Method 1: PostgreSQL Shell (SQL Queries)

```bash
# Connect to database
heroku pg:psql --app social-media-api-deninjo
```

**Common SQL Queries:**

```sql
-- 1. List all tables
\dt

-- 2. View table structure
\d accounts_user
\d posts_post
\d posts_like
\d notifications_notification

-- 3. Count records
SELECT COUNT(*) FROM accounts_user;
SELECT COUNT(*) FROM posts_post;
SELECT COUNT(*) FROM posts_like;

-- 4. View all users
SELECT id, username, email, bio, created_at FROM accounts_user;

-- 5. View all posts with author names
SELECT p.id, p.title, p.content, u.username AS author, p.created_at 
FROM posts_post p 
JOIN accounts_user u ON p.author_id = u.id 
ORDER BY p.created_at DESC;

-- 6. View posts with like counts
SELECT p.id, p.title, u.username AS author, COUNT(l.id) AS likes
FROM posts_post p
LEFT JOIN accounts_user u ON p.author_id = u.id
LEFT JOIN posts_like l ON p.id = l.post_id
GROUP BY p.id, p.title, u.username
ORDER BY likes DESC;

-- 7. Find users with most posts
SELECT u.username, COUNT(p.id) AS post_count
FROM accounts_user u
LEFT JOIN posts_post p ON u.id = p.author_id
GROUP BY u.username
ORDER BY post_count DESC;

-- 8. View recent notifications
SELECT n.id, n.message, u.username AS recipient, n.created_at, n.is_read
FROM notifications_notification n
JOIN accounts_user u ON n.recipient_id = u.id
ORDER BY n.created_at DESC
LIMIT 20;

-- 9. Find posts by specific user
SELECT title, content, created_at 
FROM posts_post 
WHERE author_id = (SELECT id FROM accounts_user WHERE username = 'your_username');

-- 10. View user's followers
SELECT u.username, u.email
FROM accounts_user u
JOIN accounts_user_following uf ON u.id = uf.from_user_id
WHERE uf.to_user_id = (SELECT id FROM accounts_user WHERE username = 'your_username');

-- Exit
\q
```

---

### Access Method 2: Django Shell (Python/ORM)

```bash
# Open Django shell on Heroku
heroku run "cd social_media_api && python manage.py shell" --app social-media-api-deninjo
```

**Common Django ORM Commands:**

```python
# Import models
from accounts.models import User
from posts.models import Post, Like
from notifications.models import Notification

# ==================== USER OPERATIONS ====================

# 1. Get all users
users = User.objects.all()
for user in users:
    print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

# 2. Count total users
print(f"Total users: {User.objects.count()}")

# 3. Get specific user
user = User.objects.get(username='admin')
print(f"User: {user.username}, Bio: {user.bio}")

# 4. Get user by ID
user = User.objects.get(id=1)

# 5. Get user's followers
followers = user.followers.all()
for follower in followers:
    print(f"Follower: {follower.username}")

# 6. Get users that this user is following
following = user.following.all()
for followed_user in following:
    print(f"Following: {followed_user.username}")

# 7. Create new user
new_user = User.objects.create_user(
    username='newuser',
    email='newuser@example.com',
    password='securepass123',
    bio='Hello from Django shell!'
)

# 8. Update user
user = User.objects.get(username='admin')
user.bio = 'Updated bio text'
user.save()

# ==================== POST OPERATIONS ====================

# 9. Get all posts
posts = Post.objects.all()
for post in posts:
    print(f"Post: {post.title} by {post.author.username}")

# 10. Count total posts
print(f"Total posts: {Post.objects.count()}")

# 11. Get posts by specific user
user = User.objects.get(username='admin')
user_posts = Post.objects.filter(author=user)
print(f"{user.username} has {user_posts.count()} posts")

# 12. Get recent posts
recent_posts = Post.objects.all().order_by('-created_at')[:10]
for post in recent_posts:
    print(f"{post.title} - {post.created_at}")

# 13. Create new post
user = User.objects.get(username='admin')
new_post = Post.objects.create(
    author=user,
    title='My New Post',
    content='This is the content of my post!'
)

# 14. Update post
post = Post.objects.get(id=1)
post.title = 'Updated Title'
post.content = 'Updated content'
post.save()

# 15. Delete post
post = Post.objects.get(id=999)
post.delete()

# 16. Get post with like count
from django.db.models import Count
posts_with_likes = Post.objects.annotate(like_count=Count('likes'))
for post in posts_with_likes:
    print(f"{post.title}: {post.like_count} likes")

# ==================== LIKE OPERATIONS ====================

# 17. Get all likes
likes = Like.objects.all()
for like in likes:
    print(f"{like.user.username} liked {like.post.title}")

# 18. Count total likes
print(f"Total likes: {Like.objects.count()}")

# 19. Get likes for specific post
post = Post.objects.get(id=1)
post_likes = Like.objects.filter(post=post)
print(f"Post '{post.title}' has {post_likes.count()} likes")

# 20. Create a like
user = User.objects.get(username='admin')
post = Post.objects.get(id=1)
like = Like.objects.create(user=user, post=post)

# 21. Check if user liked a post
user = User.objects.get(username='admin')
post = Post.objects.get(id=1)
has_liked = Like.objects.filter(user=user, post=post).exists()
print(f"User liked post: {has_liked}")

# ==================== NOTIFICATION OPERATIONS ====================

# 22. Get all notifications
notifications = Notification.objects.all()
for notif in notifications:
    print(f"{notif.recipient.username}: {notif.message} (Read: {notif.is_read})")

# 23. Get unread notifications for user
user = User.objects.get(username='admin')
unread = Notification.objects.filter(recipient=user, is_read=False)
print(f"Unread notifications: {unread.count()}")

# 24. Mark notification as read
notification = Notification.objects.get(id=1)
notification.is_read = True
notification.save()

# 25. Create notification
user = User.objects.get(username='admin')
notification = Notification.objects.create(
    recipient=user,
    message='You have a new follower!'
)

# ==================== ADVANCED QUERIES ====================

# 26. Get users with most posts
from django.db.models import Count
top_posters = User.objects.annotate(
    post_count=Count('posts')
).order_by('-post_count')[:5]
for user in top_posters:
    print(f"{user.username}: {user.post_count} posts")

# 27. Get posts with most likes
top_liked_posts = Post.objects.annotate(
    like_count=Count('likes')
).order_by('-like_count')[:5]
for post in top_liked_posts:
    print(f"{post.title}: {post.like_count} likes")

# 28. Get user's feed (posts from users they follow)
user = User.objects.get(username='admin')
following_users = user.following.all()
feed = Post.objects.filter(author__in=following_users).order_by('-created_at')
for post in feed:
    print(f"{post.author.username}: {post.title}")

# 29. Bulk create posts
user = User.objects.get(username='admin')
posts = [
    Post(author=user, title=f'Post {i}', content=f'Content {i}')
    for i in range(1, 6)
]
Post.objects.bulk_create(posts)

# 30. Search posts by keyword
keyword = 'python'
results = Post.objects.filter(content__icontains=keyword)
print(f"Found {results.count()} posts containing '{keyword}'")

# Exit shell
exit()
```

---

### Access Method 3: Django Admin Panel

```bash
# Open admin panel in browser
heroku open --app social-media-api-deninjo
# Then navigate to /admin/
```

**Or visit directly:**
```
https://social-media-api-deninjo.herokuapp.com/admin/
```

**What you can do:**
- View all users, posts, likes, notifications
- Create, edit, delete records
- Search and filter data
- View relationships between records
- Export data

---

### Access Method 4: Get Database URL for GUI Tools

```bash
# Get full database URL
heroku config:get DATABASE_URL --app social-media-api-deninjo
```

This returns something like:
```
postgres://username:password@hostname:5432/database_name
```

**Use with GUI tools:**
- **pgAdmin** - https://www.pgadmin.org/
- **TablePlus** - https://tableplus.com/
- **DBeaver** - https://dbeaver.io/
- **DataGrip** - https://www.jetbrains.com/datagrip/

---

## 💻 Local Development (SQLite)

### Access Method 1: Django Shell

```bash
# Open Django shell locally
python manage.py shell
```

Use the same Django ORM commands as above.

---

### Access Method 2: SQLite Command Line

```bash
# Open SQLite database
sqlite3 alx_social_media.sqlite3
```

**Common SQLite commands:**

```sql
-- List tables
.tables

-- View table schema
.schema accounts_user

-- View all users
SELECT * FROM accounts_user;

-- Enable column headers
.headers on
.mode column

-- Run queries (same as PostgreSQL)
SELECT username, email FROM accounts_user;

-- Exit
.quit
```

---

### Access Method 3: Django Admin Panel

```bash
# Run development server
python manage.py runserver

# Open browser to:
# http://localhost:8000/admin/
```

---

## 🔍 Useful Management Commands

### View Current Database Settings

```bash
# On Heroku
heroku run "cd social_media_api && python manage.py shell" --app social-media-api-deninjo
```

```python
from django.conf import settings
print(settings.DATABASES['default'])
```

### Database Statistics

```bash
# On Heroku (PostgreSQL)
heroku pg:info --app social-media-api-deninjo

# Shows:
# - Database size
# - Number of tables
# - Connection count
# - Plan details
```

### Export Data

```bash
# Export as JSON (all data)
heroku run "cd social_media_api && python manage.py dumpdata" --app social-media-api-deninjo > backup.json

# Export specific app
heroku run "cd social_media_api && python manage.py dumpdata posts" --app social-media-api-deninjo > posts_backup.json

# Export specific model
heroku run "cd social_media_api && python manage.py dumpdata posts.Post" --app social-media-api-deninjo > posts_only.json
```

### Import Data

```bash
# Import JSON data
heroku run "cd social_media_api && python manage.py loaddata backup.json" --app social-media-api-deninjo
```

---

## 📊 Database Monitoring Commands

### Check Database Size

```bash
heroku pg:psql --app social-media-api-deninjo -c "
SELECT 
    pg_size_pretty(pg_database_size(current_database())) AS database_size;
"
```

### Check Table Sizes

```bash
heroku pg:psql --app social-media-api-deninjo -c "
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

### Check Row Counts

```bash
heroku pg:psql --app social-media-api-deninjo -c "
SELECT 
    schemaname,
    tablename,
    n_live_tup AS row_count
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
"
```

### Check Active Connections

```bash
heroku pg:psql --app social-media-api-deninjo -c "
SELECT 
    count(*) AS active_connections
FROM pg_stat_activity
WHERE state = 'active';
"
```

---

## 🛠️ Database Maintenance

### Create Backup

```bash
# Manual backup
heroku pg:backups:capture --app social-media-api-deninjo

# Download backup
heroku pg:backups:download --app social-media-api-deninjo
```

### View Backups

```bash
# List all backups
heroku pg:backups --app social-media-api-deninjo
```

### Restore Backup

```bash
# Restore from specific backup
heroku pg:backups:restore b001 DATABASE_URL --app social-media-api-deninjo --confirm social-media-api-deninjo
```

### Schedule Auto Backups

```bash
# Daily backup at 2 AM
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/Los_Angeles' --app social-media-api-deninjo
```

---

## 🔐 Security Best Practices

### Never Share These:

❌ Database URL  
❌ Database password  
❌ `DATABASE_URL` environment variable  
❌ Backup files with production data

### Safe to Share:

✅ Database host (hostname only)  
✅ Database name  
✅ Port number (5432)

### Rotate Credentials

```bash
# Rotate database credentials
heroku pg:credentials:rotate --app social-media-api-deninjo --confirm social-media-api-deninjo
```

---

## 📋 Cheat Sheet

### Most Common Commands

```bash
# === HEROKU DATABASE ACCESS ===
heroku pg:psql --app social-media-api-deninjo
heroku run "cd social_media_api && python manage.py shell" --app social-media-api-deninjo

# === DATABASE INFO ===
heroku pg:info --app social-media-api-deninjo
heroku config:get DATABASE_URL --app social-media-api-deninjo

# === BACKUPS ===
heroku pg:backups:capture --app social-media-api-deninjo
heroku pg:backups --app social-media-api-deninjo
heroku pg:backups:download --app social-media-api-deninjo

# === MIGRATIONS ===
heroku run "cd social_media_api && python manage.py migrate" --app social-media-api-deninjo
heroku run "cd social_media_api && python manage.py showmigrations" --app social-media-api-deninjo

# === ADMIN ===
heroku run "cd social_media_api && python manage.py createsuperuser" --app social-media-api-deninjo
heroku open --app social-media-api-deninjo
```

---

## 🎯 Quick Examples

### Example 1: Check User Count

```bash
heroku pg:psql --app social-media-api-deninjo -c "SELECT COUNT(*) FROM accounts_user;"
```

### Example 2: Find User by Username

```bash
heroku run "cd social_media_api && python manage.py shell" --app social-media-api-deninjo
```

```python
from accounts.models import User
user = User.objects.get(username='admin')
print(f"User ID: {user.id}, Email: {user.email}")
exit()
```

### Example 3: List All Posts

```bash
heroku pg:psql --app social-media-api-deninjo -c "SELECT id, title, author_id FROM posts_post LIMIT 10;"
```

### Example 4: Delete Old Notifications

```bash
heroku run "cd social_media_api && python manage.py shell" --app social-media-api-deninjo
```

```python
from notifications.models import Notification
from datetime import timedelta
from django.utils import timezone

old_date = timezone.now() - timedelta(days=30)
old_notifs = Notification.objects.filter(created_at__lt=old_date, is_read=True)
count = old_notifs.count()
old_notifs.delete()
print(f"Deleted {count} old notifications")
exit()
```

---

## 📞 Getting Help

### View Django Models

```bash
heroku run "cd social_media_api && python manage.py inspectdb" --app social-media-api-deninjo
```

### Check for Database Issues

```bash
heroku run "cd social_media_api && python manage.py check --database default" --app social-media-api-deninjo
```

### View Logs

```bash
heroku logs --tail --app social-media-api-deninjo
```

---

## 🎉 You're All Set!

You now have complete access to your PostgreSQL database with multiple methods:

1. ✅ **SQL queries** via `heroku pg:psql`
2. ✅ **Python/Django ORM** via `heroku run python manage.py shell`
3. ✅ **Admin panel** via browser
4. ✅ **GUI tools** via DATABASE_URL

Choose the method that works best for your task!

---

**Last Updated:** January 26, 2026
