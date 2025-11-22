'''
only allow admins to edit data, everyone else can only read:
'''

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission: read-only for everyone, write only for admin.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # GET, HEAD, OPTIONS are safe
        return request.user and request.user.is_staff  # POST, PUT, DELETE only if admin
