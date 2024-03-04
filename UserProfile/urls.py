from django.urls import path, include
from .views import *
from accounts import views
from .views import UserProfileView
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('create', UserProfileView.as_view(), name='add-post'),
    path('get/<str:userEmail>', UserProfileView.as_view(), name='grt_user_post'), # detailed view of user post
]