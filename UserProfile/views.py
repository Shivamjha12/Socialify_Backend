from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from accounts.models import User
from accounts.views import get_user_from_token
from .serializers import UserProfileSerializer
# Create your views here.
class UserProfileView(APIView):
    def get(self, request,userEmail):
        UserProfileobj = UserProfile.objects.filter(user__email=userEmail).first()
        if UserProfileobj is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'Profile Not Found'})
        profile_data = UserProfileSerializer(UserProfileobj).data
        return Response(status=status.HTTP_200_OK,data=profile_data)
    
    def post(self, request):
        jwt = request.data['jwt']
        profile_image = request.data.get('profile_image', None)
        country = request.data['country']
        city = request.data['city']
        short_intro = request.data['short_intro']
        description = request.data['description']
        interests = request.data['interests']
        userEmail = get_user_from_token(jwt)
        if userEmail is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'User Not Found'})
    
        userProfileInstance = UserProfile.objects.filter(user__email=userEmail.email).first()
        if userProfileInstance is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Profile Already Exists'})
        
        UserProfileobj = UserProfile.objects.create(user=userEmail, profile_Image=profile_image, country=country, city=city, short_intro=short_intro, description=description, interests=interests)
        UserProfileobj.save()
        
        return Response(status=status.HTTP_201_CREATED, data={"message": "Profile Created Successfully"})