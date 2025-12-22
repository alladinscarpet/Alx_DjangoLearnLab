"""
in DRF, serializers do three jobs,:
Output formatting (model → JSON)
Input validation (JSON → validated data)
Object creation / update control

Think of serializers as:
Custom gates into your database
Models define what exists
Serializers define how it enters and exits
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

# ensures compatibility with custom user models
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # This field accepts a password from the client
    # write_only=True ensures the password is NEVER included in responses
    password = serializers.CharField(write_only=True)

    class Meta:
        # Tell DRF which model this serializer is based on
        model = User

        # Explicitly define allowed fields
        # This prevents exposing sensitive user fields
        fields = ['username', 'email', 'password', 'bio']

    def create(self, validated_data):
        """
        This method runs AFTER serializer validation succeeds.
        It defines HOW a User instance is created.
        """

        # Use Django's built-in create_user method
        # This automatically hashes the password correctly
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        # bio is a custom field we added to the user model
        # We set it manually because create_user doesn't know about it
        user.bio = validated_data.get('bio', '')

        # Save the user to the database
        user.save()

        # Return the created user instance
        return user