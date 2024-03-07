from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Photo, Comment
from .serializers import PostSerializer,CommentSerializer
from accounts.models import User
from UserFriends.models import Friendship


class PostCreationAPIView(APIView):
    
    def post(self, request):
        content = request.data['content']
        user = request.data['email']
        photos = request.FILES.getlist('photos')
        userInstance = User.objects.filter(email=user).first()
        if userInstance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,messages="User not found")
        post = Post.objects.create(user= userInstance,content=content)
        post.save()
        for i in photos:
            photo_instance = Photo.objects.create(image=i,post=post,caption=user)
            photo_instance.save()   
        return Response(status=status.HTTP_201_CREATED)
    
    def get(self, request,uuid):
        post = Post.objects.filter(postid=uuid).first()
        comments = Comment.objects.filter(post__postid=uuid)
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'Post Not Found'})
        post_data = PostSerializer(post).data
        post_comment_data = CommentSerializer(comments,many=True).data
        post_data.update({"comments":post_comment_data})
        return Response(status=status.HTTP_200_OK,data=post_data)

class UserPostAPIView(APIView):
    
    def get(self, request,user):
        user = User.objects.filter(email=user).first()
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'User Not Found'})
        posts = Post.objects.filter(user=user)
        post_data = PostSerializer(posts,many=True).data
        for i in post_data:
            uuid = i['postid']
            print(uuid," ----------------------------- ")
            comments = Comment.objects.filter(post__postid=uuid)
            post_comment_data = CommentSerializer(comments,many=True).data
            i.update({"comments":post_comment_data})
            # print(i," ----------------------------- ")
        return Response(status=status.HTTP_200_OK,data=post_data)


from accounts.views import get_user_from_token
class PostUpdateDeleteAPIView(APIView):
    
    def put(self, request,uuid,jwtToken):
        post = Post.objects.filter(postid=uuid).first()
        userEmail = get_user_from_token(jwtToken)
        if userEmail.email != post.user.email:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'You can not Edit others post'})
        if userEmail is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'User Not Found'})
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'Post Not Found'})
        post.content = request.data['content']
        post.save()
        return Response(status=status.HTTP_200_OK,data={'message': 'Post Updated'})
    
    def delete(self, request,uuid,jwtToken):
        post = Post.objects.filter(postid=uuid).first()
        userEmail = get_user_from_token(jwtToken)
        if userEmail.email != post.user.email:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'You can not Delete others post'})
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'Post Not Found'})
        post.delete()
        return Response(status=status.HTTP_200_OK,data={'message': 'Post Deleted'})
    
class PostUserFeedAPIView(APIView):
    
    def get(self, request,email):
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'User Not Found'})
        
        friend_of_user = Friendship.objects.filter(user1=user)
        user_friend = [i.user2.id for i in friend_of_user]
        
        # for i in friend_of_user:
        #     user_friend.append(i.user2)
        user_friend.append(user.id)
        print(user_friend,"List of friends")
        print(friend_of_user,"Here we got ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        posts = Post.objects.filter(user__id__in=user_friend) 
        print(posts,"does i am getting the posts that i want")
        post_data = PostSerializer(posts,many=True).data
        for i in post_data:
            uuid = i['postid']
            comments = Comment.objects.filter(post__postid=uuid)
            post_comment_data = CommentSerializer(comments,many=True).data
            i.update({"comments":post_comment_data})
        return Response(status=status.HTTP_200_OK,data=post_data)
    
class CreatePostCommentAPIView(APIView):
    def post(self, request):
        postid = request.data['postid']
        content = request.data['content']
        user_jwt = request.data['user_jwt']
        userInstance = get_user_from_token(user_jwt)
        if userInstance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,messages="User not found")
        post = Post.objects.filter(postid=postid).first()
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,messages="Post not found")
        comment = Comment.objects.create(user=userInstance,post=post,content=content)
        comment.save()
        return Response(status=status.HTTP_201_CREATED)
    
class likePostView(APIView):
    def post(self,request):
        postid = request.data['postid']
        user_jwt = request.data['user_jwt']
        post = Post.objects.filter(postid=postid).first()
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,messages="Post not found")
        userInstance = get_user_from_token(user_jwt)
        if userInstance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,messages="User not found")
        post.add_like()
        return Response(status=status.HTTP_200_OK,data={'message': 'Post Liked'})
        