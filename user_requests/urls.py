from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RequestViewSet

router = DefaultRouter()
router.register('', RequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
# This code defines the URL routing for the user requests API. It uses Django REST Framework's router to automatically generate the URL patterns for the RequestViewSet, which handles CRUD operations for user requests. The base URL for this API will be determined by the path where this module is included in the project's main URL configuration.
# The router registers the RequestViewSet, which means that all the standard actions (list, create, retrieve, update, destroy) will be available at the base URL defined here. The urlpatterns list is then included in the main URL configuration of the Django project.