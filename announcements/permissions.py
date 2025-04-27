# 📄 announcements/permissions.py

from rest_framework import permissions

class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Επιτρέπει μόνο σε διαχειριστές να δημιουργούν/τροποποιούν, οι υπόλοιποι μπορούν μόνο να διαβάζουν.
    """

    def has_permission(self, request, view):
        # GET/HEAD/OPTIONS είναι πάντα επιτρεπτά
        if request.method in permissions.SAFE_METHODS:
            return True
        # Για POST/PUT/DELETE, απαιτείται is_staff
        return request.user and request.user.is_authenticated and request.user.is_staff
