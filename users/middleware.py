# users/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    """
    Αν ο χρήστης έχει must_change_password = True,
    τον αναγκάζει να αλλάξει τον κωδικό του.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if getattr(request.user, 'must_change_password', False):
                change_password_url = reverse('password_change')
                if request.path != change_password_url and not request.path.startswith('/admin/'):
                    return redirect(change_password_url)
        return self.get_response(request)
