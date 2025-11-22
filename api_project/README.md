### 1. Building Your First API Endpoint with Django REST Framework


#### Objective
Develop a simple API endpoint using Django REST Framework that allows clients to retrieve information about books stored in your database.  
This will introduce you to the core components of DRF, including serializers and views.

---

#### Task Description
In this task within your newly created **`api_project`**, you will set up a basic API endpoint to list all books using Django REST Framework.  
This will involve creating serializers, views, and routing configurations.

---

#### Steps

1. **Create the Serializer**

   You need a serializer to convert your Book model instances into JSON format.

   - **Define the Serializer:**
     - In the `api` app, create a new file named **`serializers.py`**.
     - Define a **`BookSerializer`** class that extends `rest_framework.serializers.ModelSerializer` and includes all fields of the `Book` model.

2. **Create the API View**

   Set up a view that uses the serializer to retrieve and return book data.

   - **Define the View:**
     - In **`api/views.py`**, create a view named **`BookList`** that extends `rest_framework.generics.ListAPIView`.
     - Use the `BookSerializer` to serialize the data and the `Book` model as the queryset.

3. **Configure URL Patterns**

   Ensure the API endpoint is accessible via HTTP by setting up the corresponding URL.

   - **URL Setup:**
     - In **`api/urls.py`** (create this file if it doesn't exist), include a URL pattern that routes to your `BookList` view.
     - Use Django's `path()` function to map the URL to your view.

   Your URL pattern should look like this:
```python
   urlpatterns = [
       path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
   ]
```

   Also, ensure that the main **`api_project/urls.py`** file includes a route to your `api` app.  
   Something like this should work fine:
```python
   path('api/', include('api.urls'))
```

   This step connects the app's URLs to the overall project.

4. **Test the API Endpoint**

   After setting up the endpoint, test it to ensure it functions as expected.

   - **Testing Method:**
     - Use tools like `curl`, Postman, or your browser to access the endpoint and verify that it returns a JSON list of books.

---

#### Deliverables

1. **`serializers.py`**: Includes the `BookSerializer`.
2. **`views.py`**: Contains the `BookList` view definition.
3. **`urls.py`**: Configured with the URL for accessing the `BookList` API endpoint.