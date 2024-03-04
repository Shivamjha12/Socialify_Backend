from rest_framework import serializers
from .models import *
from accounts.models import User
from UserProfile.models import UserProfile

class UserFriendSerializer(serializers.ModelSerializer):
    # user = User.objects.filter(email=email).first()
    class Meta:
        model = User
        fields = ('name','email','date_joined','is_paid_user')