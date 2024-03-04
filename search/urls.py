from django.urls import path, include
from .views import *
from accounts import views
from .views import UserSearchView
urlpatterns = [
    path('user/<str:searchQuery>', UserSearchView.as_view(), name='add-post'),
]