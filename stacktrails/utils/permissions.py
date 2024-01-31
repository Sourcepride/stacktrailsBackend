from rest_framework.permissions import BasePermission


class LockOut(BasePermission):
    """
    Block Out All Users
    """

    message = "Permission Denied"

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False
