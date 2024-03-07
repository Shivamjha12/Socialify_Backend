from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from accounts.models import User
from accounts.views import get_user_from_token
from django.db import IntegrityError
from UserProfile.models import UserProfile
# here are all calculating function
from django.db.models import Q
from UserProfile.models import UserProfile
from UserProfile.serializers import UserProfileSerializer
def get_total_friends(user):
    friendships = Friendship.objects.filter(user1=user)
    friends=[]
    for i in friendships:
        friends.append(i)
    return len(friends)
#------------------------------------
class GetFriendApi(APIView):
    
    def get(self, request, userEmail):
        user = User.objects.filter(email=userEmail).first()
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'User Not Found'})
        
        # Query friendships where the user is either user1 or user2
        friendships = Friendship.objects.filter(user1=user)
        no_of_friends = []
        for i in friendships:
            if i.user2.id not in no_of_friends:
                no_of_friends.append(i.user2.id)
            
            
        userprofile = UserProfile.objects.filter(user=user).first()
        userprofile.friends_count = len(no_of_friends)
        userprofile.save()    
        # Serialize the friendships
        serializer = UserFriendSerializer(friendships, many=True).data
        for i in serializer:
            print(i)
            profileuser = User.objects.filter(email=i['user2']).first()
            profile=UserProfile.objects.filter(user=profileuser).first()
            profile_data = UserProfileSerializer(profile).data
            i.update({"profile_data":profile_data})
        return Response(status=status.HTTP_200_OK, data=serializer)
    
class AddFriendApi(APIView):
    def post(self, request):
        jwt = request.data['jwt']
        friendEmail = request.data['friendEmail']
        currentUser = get_user_from_token(jwt)
        friendEmailInstance = User.objects.filter(email=friendEmail).first()
        
        if friendEmailInstance is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'User Not Found'})
        try:
            friend = Friendship.objects.create(user1=currentUser, user2=friendEmailInstance)
            friend.save()
            user1profile = UserProfile.objects.filter(user=currentUser).first()
            user2profile = UserProfile.objects.filter(user=friendEmailInstance).first()
            user1friends = get_total_friends(currentUser)
            user2friends = get_total_friends(friendEmailInstance)
            if user1friends is None:
                up=UserProfile.objects.create(user=currentUser)
                up.save()
                user1profile = UserProfile.objects.filter(user=currentUser).first()
            if user2friends is None:
                up=UserProfile.objects.create(user=friendEmailInstance)
                up.save()
                user2profile = UserProfile.objects.filter(user=friendEmailInstance).first()
            user1profile.friends_count=user1friends
            user1profile.save()
            user2profile.friends_count=user2friends
            user2profile.save()
            
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Friend Already Exists'})
        return Response(status=status.HTTP_201_CREATED, data={"message": "Friend Added Successfully"})
    
class IsFriendApi(APIView):
    
    def get(self, request,user1,user2):
        userobj1 = User.objects.filter(email=user1).first()
        userobj2 = User.objects.filter(email=user2).first()
        if(userobj1 is None or userobj2 is None):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'User Not Found'})
        isFriend = Friendship.objects.filter(user1=userobj1,user2=userobj2).exists()
        return Response(status=status.HTTP_200_OK, data={'isFriend': isFriend})
            