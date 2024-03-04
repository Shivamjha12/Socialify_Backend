from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    profile_Image = serializers.SerializerMethodField()
    # serializers.CharField(source="profile_Image.url")
    user = serializers.CharField(source="user.email")
    name = serializers.CharField(source="user.name")
    class Meta:
        model = UserProfile
        fields = ('name','user', 'profile_Image', 'country', 'city', 'short_intro', 'description', 'interests', 'friends_count')
        
    def get_profile_Image(self, obj):
        if obj.profile_Image:
            return obj.profile_Image.url
        else:
            return None