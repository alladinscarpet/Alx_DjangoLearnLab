
'''
Where you define what should happen when someone visits
a certain web page (the logic behind routes).
'''

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer

# Create your views here.



class RegisterView(APIView):
    """
    Handles user registration.
    Accepts POST requests with username, email, password, bio.
    """

    def post(self, request):
        # Pass incoming request data to the serializer
        serializer = RegisterSerializer(data=request.data)

        # Validate input data (runs serializer field validation)
        if serializer.is_valid():
            # Create and save the user
            user = serializer.save()

            # Create a token for the newly registered user
            # This token will be used for authenticated requests
            token, created = Token.objects.get_or_create(user=user)

            # Return success response with token
            return Response(
                {
                    "message": "User registered successfully",
                    "token": token.key
                },
                status=status.HTTP_201_CREATED
            )

        # If validation fails, return error messages
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    Handles user login.
    Accepts POST requests with username and password.
    """

    def post(self, request):
        # Extract credentials from request body
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate user credentials
        user = authenticate(username=username, password=password)

        # If authentication fails
        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get or create token for authenticated user
        token, created = Token.objects.get_or_create(user=user)

        # Return token to client
        return Response(
            {
                "message": "Login successful",
                "token": token.key
            },
            status=status.HTTP_200_OK
        )
