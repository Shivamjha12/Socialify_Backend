from rest_framework import serializers
from .models import Post, Photo, Comment

 
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'image', 'caption')

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.CharField(source="post.postid")
    user = serializers.CharField(source="user.name")
    class Meta:
        model = Comment
        fields = ('user','post', 'content', 'created_at')

class PostSerializer(serializers.ModelSerializer):
    # comments_obj = Comment.objects.filter(post__postid=postid)
    
    photos = PhotoSerializer(many=True, read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    user = serializers.CharField(source="user.email")
    name = serializers.CharField(source="user.name")
    class Meta:
        model = Post
        fields = ('id', 'user','name','postid', 'content', 'created_at', 'updated_at', 'likes', 'photos')
