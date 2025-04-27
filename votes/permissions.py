# 📄 votes/permissions.py

from rest_framework import permissions

class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Επιτρέπει μόνο σε διαχειριστές να δημιουργούν, τροποποιούν ή διαγράφουν ψηφοφορίες.
    Οι υπόλοιποι μπορούν να βλέπουν και να ψηφίζουν.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff
