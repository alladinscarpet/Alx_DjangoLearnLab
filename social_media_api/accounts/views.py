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

from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404




# Create your views here.
# Import the custom user model
from django.contrib.auth import get_user_model

User = get_user_model()


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


#----------------------------------------followers view--------------------------------------------#

# Follow a user
class FollowUserView(generics.GenericAPIView):
    """
    Endpoint to follow another user.
    Authenticated users can follow any other user.
    """
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can follow

    def post(self, request, user_id):
        # Get the user to follow by ID, or return 404 if not found
        target_user = get_object_or_404(User.objects.all(), id=user_id)
        current_user = request.user  # The logged-in user making the request

        # Prevent following yourself
        if target_user == current_user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the target user to the current user's following list
        current_user.following.add(target_user)
        current_user.save()

        return Response({"detail": f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)


# Unfollow a user
class UnfollowUserView(generics.GenericAPIView):
    """
    Endpoint to unfollow another user.
    Authenticated users can remove users from their following list.
    """
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can unfollow

    def post(self, request, user_id):
        target_user = get_object_or_404(User.objects.all(), id=user_id)
        current_user = request.user

        # Prevent unfollowing yourself
        if target_user == current_user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the target user from the current user's following list
        current_user.following.remove(target_user)
        current_user.save()

        return Response({"detail": f"You have unfollowed {target_user.username}."}, status=status.HTTP_200_OK)


