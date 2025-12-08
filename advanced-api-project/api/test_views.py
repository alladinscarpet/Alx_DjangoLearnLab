'''
No database setup needed
Django automatically:
Creates a test database
Runs all tests inside it
Deletes it after
'''

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Book, Author
from django.contrib.auth.models import User


class BookAPITests(APITestCase):
    # method to create author, books, and a user.
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass123')
        # to enable user to be an admin
        self.user.is_staff = True
        self.user.save()  # Persist is_staff to DB

        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(
            title="Harry Potter 1",
            publication_year=1997,
            author=self.author
        )
        # Log in the test client so all requests are authenticated
        self.client.login(username='test', password='pass123')


    # Ensures the API returns a list of all books with a 200 OK response.
    def test_list_books(self):
        url = reverse('book-list')  # GET api/books/
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # Verifies that a new book can be created successfully and stored in the database.
    def test_create_book(self):
        url = reverse('book-create')  # POST api/books/create/
        data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)


    # Checks that a single book can be retrieved correctly using its ID.
    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book.id]) # GET api/books/<pk>/
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # Confirms that updating a book modifies its data and returns a 200 response.
    def test_update_book(self):
        url = reverse('book-update', args=[self.book.id]) # PUT api/books/update/<pk>/
        data = {'title': 'Updated Title', 'author': self.author.id, 'publication_year': 1997}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    # Ensures that a book can be deleted and is removed from the database.
    def test_delete_book(self):
        url = reverse('book-delete', args=[self.book.id]) # PUT api/books/update/<pk>/
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # Validates that filtering books by title (case-insensitive) returns correct matches.
    def test_filter_by_title(self):
        url = reverse('book-list') + "?title__icontains=harry"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Tests that the search feature returns books matching the search query.
    def test_search(self):
        url = reverse('book-list') + "?search=harry"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

    # Checks that books are returned in the correct order when ordering is applied.
    def test_ordering(self):
        Book.objects.create(title="A Book", publication_year=1990, author=self.author)
        url = reverse('book-list') + "?ordering=publication_year"
        response = self.client.get(url)
        years = [b['publication_year'] for b in response.data]
        self.assertEqual(years, sorted(years))
