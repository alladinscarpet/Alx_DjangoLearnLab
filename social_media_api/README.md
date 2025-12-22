# Social Media API Project Tasks

## 0. Project Setup and User Authentication for a Social Media API



### Objective
Start building a Social Media API from scratch, focusing on setting up the project environment, user authentication, and creating the initial user models.

### Task Description
Begin by establishing the foundational elements of your Social Media API. This includes setting up the Django project, integrating Django REST Framework for API functionality, and implementing a robust user authentication system.

### Step 1: Create a New Django Project

**Environment Setup:**
- Install Django and Django REST Framework using pip, if not already installed:
  ```bash
  pip install django djangorestframework
  ```
- Create a new Django project named `social_media_api`:
  ```bash
  django-admin startproject social_media_api
  ```
- Navigate into your project directory and create a new Django app called `accounts` for handling user-related functionality:
  ```bash
  cd social_media_api
  python manage.py startapp accounts
  ```
- Add `'rest_framework'` and `'accounts'` to the `INSTALLED_APPS` in `settings.py`.

### Step 2: Configure User Authentication

**User Model and Authentication:**
- Create a custom user model that extends Django's AbstractUser, adding fields such as `bio`, `profile_picture`, and `followers` (a ManyToMany field referencing itself, symmetrical=False).
- Set up Django REST Framework's token authentication by adding `'rest_framework.authtoken'` to your installed apps and running migrations to create the token model.
- Implement views and serializers in the `accounts` app for user registration, login, and token retrieval.

### Step 3: Define URL Patterns

**Routing Configuration:**
- Configure URL patterns in `accounts/urls.py` to include routes for registration (`/register`), login (`/login`), and user profile management (`/profile`).
- Ensure that registration and login endpoints return a token upon successful operations.

### Step 4: Testing and Initial Launch

**Server Testing:**
- Start the Django development server to ensure the initial setup is configured correctly:
  ```bash
  python manage.py runserver
  ```
- Use tools like Postman to test user registration and login functionalities, verifying that tokens are generated and returned correctly.

### Deliverables
1. **Project Setup Files:** Include all configuration files, initial migrations, and the Django project structure.
2. **Code Files:** Include models, views, and serializers for the user authentication system in the `accounts` app.
3. **Documentation:** Provide a README file detailing the setup process, how to register and authenticate users, and a brief overview of the user model.


---

---

## 1. Implementing Posts and Comments Functionality

**mandatory**  
**Score:** 0.0% (Checks completed: 0.0%)

### Objective
Develop core functionalities of the Social Media API by adding posts and comments features. This task will enable users to create, view, update, and delete posts and comments within the social media platform.

### Task Description
Expand your social_media_api project by creating functionality for users to manage posts and engage with them through comments. This includes setting up models, serializers, views, and routes for posts and comments.

### Step 1: Create Post and Comment Models

**Model Definitions:**
- In a new app within the project called posts, create models for Post and Comment.
- Post should have fields like author (ForeignKey to User), title, content, created_at, and updated_at.
- Comment should reference both Post (ForeignKey) and User (author), with additional fields for content, created_at, and updated_at.

**Database Setup:**
- Include these models in your migrations and update the database by running:
  ```bash
  python manage.py makemigrations posts
  python manage.py migrate
  ```

### Step 2: Implement Serializers for Posts and Comments

**Serializer Setup:**
- Create serializers for both Post and Comment in posts/serializers.py.
- Ensure that serializers handle user relationships correctly and validate data as needed.

### Step 3: Create Views for CRUD Operations

**View Implementation:**
- Using Django REST Framework's viewsets, set up CRUD operations for both posts and comments in posts/views.py.
- Implement permissions to ensure users can only edit or delete their own posts and comments.

### Step 4: Configure URL Routing

**Routing Configuration:**
- Define URL patterns in posts/urls.py that map to the viewsets using Django REST Framework's routers. This includes routes for listing, creating, editing, and deleting both posts and comments.

### Step 5: Implement Pagination and Filtering

**Enhance API Usability:**
- Add pagination to post and comment list endpoints to manage large datasets.
- Implement filtering capabilities in post views to allow users to search posts by title or content.

### Step 6: Test and Validate Functionality

**Testing Guidelines:**
- Thoroughly test all endpoints using tools like Postman or automated tests to ensure they behave as expected.
- Validate that permissions are correctly enforced and that data integrity is maintained through the API.

### Step 7: Document API Endpoints

**Documentation:**
- Update the API documentation to include detailed information on how to interact with the posts and comments endpoints.
- Provide examples of requests and responses for all operations.

### Deliverables
- **Code Files:** Include all models, serializers, views, and URL configurations related to posts and comments.
- **API Documentation:** Detailed descriptions of each endpoint, including usage examples.
- **Testing Results:** Evidence of testing and validation, including any scripts or Postman collections used.

---

---

## 2. Implementing User Follows and Feed Functionality


### Objective
Expand the Social Media API by adding features for users to follow other users and view an aggregated feed of posts from users they follow. This task enhances the social aspect of the platform, mimicking key functionalities seen in popular social media networks.

### Task Description
In this task, you will build on your existing social_media_api by incorporating user relationships and a dynamic content feed. This involves managing user follow relationships and creating a feed that displays posts from followed users.

### Step 1: Update the User Model to Handle Follows

**Model Adjustments:**
- Modify your custom user model to include a following field, which is a many-to-many relationship to itself, representing the users that a given user follows.
- Make necessary migrations to update the user model:
  ```bash
  python manage.py makemigrations accounts
  python manage.py migrate
  ```

### Step 2: Create API Endpoints for Managing Follows

**Follow Management Views:**
- Develop views in the accounts app that allow users to follow and unfollow others. This might include actions like follow_user and unfollow_user, which update the following relationship.
- Ensure proper permissions are enforced so users can only modify their own following list.

### Step 3: Implement the Feed Functionality

**Feed Generation:**
- Create a view in the posts app that generates a feed based on the posts from users that the current user follows.
- This view should return posts ordered by creation date, showing the most recent posts at the top.

### Step 4: Define URL Patterns for New Features

**Routing for Follows and Feed:**
- Set up URL patterns in accounts/urls.py for follow management (e.g., `/follow/<int:user_id>/` and `/unfollow/<int:user_id>/`).
- Add a route in posts/urls.py for the feed endpoint, such as `/feed/`.

### Step 5: Test Follow and Feed Features

**Testing and Validation:**
- Conduct thorough tests to ensure that the follow system works as intended and that the feed correctly displays posts from followed users.
- Use Postman or similar tools to simulate the user experience and verify the correctness of the output.

### Step 6: Documentation

**API Documentation:**
- Update your project documentation to include details on how to manage follows and access the feed. Provide clear instructions and examples for each new endpoint.
- Document any changes made to models, especially modifications to the user model.

### Deliverables
- **Updated Models and Migrations:** Include changes to the user model and any new migrations.
- **Code Files for Views and Serializers:** Implementations for follow management and feed generation.
- **URL Configurations:** New routes added for managing follows and retrieving the feed.
- **Documentation:** Comprehensive API documentation covering the new functionalities.

---

---

## 3. Implementing Notifications and Likes Functionality


### Objective
Enhance user engagement in your Social Media API by adding notification and likes functionalities. This task will allow users to like posts and receive notifications for various interactions within the platform.

### Task Description
Develop functionalities in your social_media_api that enable users to like posts and receive notifications for important activities such as new followers, likes on their posts, or comments. This will make the platform more interactive and social.

### Step 1: Create Like and Notification Models

**Model Definitions:**
- In the posts app, create a Like model that tracks which users have liked which posts. This model should have a ForeignKey to Post and a ForeignKey to User.
- In a new app called notifications, create a Notification model with fields like recipient (ForeignKey to User), actor (ForeignKey to User), verb (describing the action), target (GenericForeignKey to the object), and timestamp.

### Step 2: Implement Like Functionality

**Like System Views:**
- Create views to handle liking and unliking posts. These views should update the Like model and generate appropriate notifications.
- Ensure that these views check for user authentication and prevent users from liking a post multiple times.

### Step 3: Develop Notification System

**Notification Handling:**
- Set up views and methods to create notifications whenever relevant actions occur, such as a user getting a new follower, someone liking their post, or commenting on their post.
- Provide an endpoint for users to fetch their notifications, showcasing unread notifications prominently.

### Step 4: Define URL Patterns for Likes and Notifications

**Routing Configuration:**
- Add URL patterns in posts/urls.py for liking and unliking posts, such as `/posts/<int:pk>/like/` and `/posts/<int:pk>/unlike/`.
- In notifications/urls.py, set up a route for users to view their notifications, like `/notifications/`.

### Step 5: Test Likes and Notifications Features

**Testing and Validation:**
- Thoroughly test the likes and notifications system to ensure functionality is reliable. Test scenarios include liking a post, unliking a post, receiving notifications for various interactions, and viewing notifications.
- Use automated tests and tools like Postman to simulate interactions and verify system responses.

### Step 6: Documentation

**API Documentation:**
- Document the functionality and endpoints for the likes and notifications systems. Provide detailed examples of requests and the expected responses.
- Explain how users can interact with these features and the benefits they bring to user engagement.

### Deliverables
- **Code Files:** Models, views, and serializers for likes and notifications.
- **API Endpoint Documentation:** Detailed descriptions and usage instructions for new endpoints.
- **Testing Results:** Documentation of testing procedures, cases, and outcomes.

---

---

## 4. Deploying the Django REST API to Production


### Objective
Prepare and deploy your Django REST API to a production environment. This task involves configuring the project for deployment, selecting a hosting service, and using tools to manage static files and databases in a production setting.

### Task Description
Finalize your social_media_api project for public availability by deploying it to a production server. This will allow real-world testing and interaction, making the project a significant addition to your portfolio.

### Step 1: Prepare the Project for Deployment

**Production Settings:**
- Review and adjust the settings.py for production use. This includes setting DEBUG to False, configuring the ALLOWED_HOSTS, and setting up proper database configurations for production.
- Configure security settings like SECURE_BROWSER_XSS_FILTER, X_FRAME_OPTIONS, SECURE_CONTENT_TYPE_NOSNIFF, and SECURE_SSL_REDIRECT.

### Step 2: Choose a Hosting Service

**Hosting Selection:**
- Select a cloud hosting service suitable for deploying Django applications, such as Heroku, AWS Elastic Beanstalk, or DigitalOcean.
- Set up an account and prepare the environment according to the provider's guidelines for hosting a Django app.

### Step 3: Set Up a Web Server and WSGI

**Web Server Configuration:**
- Configure a web server, such as Gunicorn or uWSGI, to serve your Django app.
- Set up Nginx as a reverse proxy to serve static files and handle HTTPS redirection if not automatically managed by your hosting provider.

### Step 4: Manage Static Files and Databases

**Static and Media Files:**
- Configure Django to handle static files and media files properly in production using collectstatic and setting up a storage solution like AWS S3 for file hosting.
- Ensure your database is properly set up, whether using a managed database service like Amazon RDS or a PostgreSQL instance on your server.

### Step 5: Deploy the Application

**Deployment Process:**
- Push your code to a repository (e.g., GitHub) if not already done.
- Use the hosting service's deployment methods (e.g., Heroku Git, AWS CodeDeploy) to deploy your application.
- Configure environment variables in your hosting service (like secret keys and database URLs).

### Step 6: Monitor and Maintain the Application

**Maintenance and Monitoring:**
- Set up logging and monitoring to keep track of the application's health and any errors that might occur.
- Plan for regular updates and maintenance to keep the software and dependencies up to date.

### Step 7: Documentation and Final Testing

**Documentation and Testing:**
- Document the deployment process and any configurations specific to your production environment.
- Perform final testing to ensure everything is running as expected in the live environment.

### Deliverables
- **Deployment Configuration Files:** Include any scripts or configuration files used for deployment.
- **Live URL:** Provide the URL to the deployed application.
- **Deployment Documentation:** Detailed instructions and notes on the deployment process, environment setup, and maintenance plans.