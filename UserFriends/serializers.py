from rest_framework import serializers
from .models import Friendship

class UserFriendSerializer(serializers.ModelSerializer):
    user2 = serializers.CharField(source="user2.email")

    class Meta:
        model = Friendship
        fields = ('user2',)
