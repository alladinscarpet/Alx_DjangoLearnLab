### 2. Implementing CRUD Operations with ViewSets and Routers in Django REST Framework



#### Objective
Expand your API functionality by using Django REST Framework's ViewSets and Routers to implement CRUD (Create, Read, Update, Delete) operations on the `Book` model.  
This approach simplifies the management of standard database operations through RESTful APIs.

---

#### Task Description
In this task, you will replace the simple list view created previously with a full set of CRUD operations using DRF's ViewSets.  
This will allow clients to not only retrieve but also create, update, and delete books via your API.

---

#### Steps

1. **Create a ViewSet**

   ViewSets in DRF allow you to consolidate common logic for handling standard operations into a single class that handles all HTTP methods (GET, POST, PUT, DELETE).

   - **Define the ViewSet:**
     - In **`api/views.py`**, extend the existing view setup by adding a new class **`BookViewSet`** that handles all CRUD operations.
     - Use `rest_framework.viewsets.ModelViewSet`, which provides implementations for various actions like list, create, retrieve, update, and destroy.

2. **Set Up a Router**

   Routers in DRF automatically determine the URL conf based on your ViewSet.

   - **Configure the Router:**
     - In **`api/urls.py`**, import `DefaultRouter` from `rest_framework.routers` and register your `BookViewSet`.
     - Register the BookViewSet with the router as follows:
```python
       router.register(r'books_all', BookViewSet, basename='book_all')
```

     - The router will handle creating the appropriate URL patterns for all CRUD operations on the `Book` model.

   Your URL patterns in **`api/urls.py`** should now look like this:
```python
   urlpatterns = [
       # Route for the BookList view (ListAPIView)
       path('books/', BookList.as_view(), name='book-list'),

       # Include the router URLs for BookViewSet (all CRUD operations)
       path('', include(router.urls)),  # This includes all routes registered with the router
   ]
```

3. **Test CRUD Operations**

   Ensure that each of the CRUD operations works as expected. Test creating, retrieving, updating, and deleting books through your API.

   - **Testing Method:**
     - Use tools like Postman or curl to send POST, GET, PUT, and DELETE requests to your API endpoints and verify the responses.

   **Tip:** Be sure to test the following operations:
   - **GET** `/books_all/` – List all books
   - **GET** `/books_all/<id>/` – Retrieve a book by its ID
   - **POST** `/books_all/` – Create a new book
   - **PUT** `/books_all/<id>/` – Update a book
   - **DELETE** `/books_all/<id>/` – Delete a book

---

#### Deliverables

1. **`views.py`**: Updated with `BookViewSet` that handles all CRUD operations.
2. **`urls.py`**: Includes the configuration using `DefaultRouter` to route requests to the `BookViewSet`.