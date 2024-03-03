from django.urls import path, include
from .views import *
from accounts import views
from .views import PostCreationAPIView 
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('create', PostCreationAPIView.as_view(), name='add-post'),
    path('get/<uuid:uuid>', PostCreationAPIView.as_view(), name='grt_user_post'), # detailed view of user post
    path('get_user_post/<str:user>', UserPostAPIView.as_view(), name='add-post'),# all post of particular user
    path('get_user_feed', PostUserFeedAPIView.as_view(), name='add-post'), # we get post of user and users friends 
    path('modification/<uuid:uuid>/<str:jwtToken>', PostUpdateDeleteAPIView.as_view(), name='add-post'), # update post details or delete
    path('create_comment_post', CreatePostCommentAPIView.as_view(), name='add-post'),# all post of particular user
    path('like_post', likePostView.as_view(), name='like-post'),# all post of particular user
]