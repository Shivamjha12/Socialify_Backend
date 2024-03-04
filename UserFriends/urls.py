from django.urls import path, include
from .views import *
from accounts import views
from .views import *

urlpatterns = [
    path('add', AddFriendApi.as_view(), name='add-friend'),
    path('get/<str:userEmail>', GetFriendApi.as_view(), name='get-friend'),
    path('is_friend/<str:user1>/<str:user2>', IsFriendApi.as_view(), name='isFriend'),
    
]