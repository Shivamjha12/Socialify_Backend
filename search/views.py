from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from accounts.models import User
from accounts.views import get_user_from_token
from .serializers import UserFriendSerializer
from rest_framework import generics
from UserProfile.serializers import UserProfileSerializer
from UserProfile.models import UserProfile

class UserSearchView(APIView):
    def get(self,request,searchQuery):
        query =searchQuery
        if query:
            # Perform search using the query on relevant model fields
            # try:
            results = User.objects.filter(name__icontains=query) | User.objects.filter(email__icontains=query)
            serializer= UserFriendSerializer(results, many=True).data
            for i in serializer:
                print(i['email'])
                profileuser = User.objects.filter(email=i['email']).first()
                profile=UserProfile.objects.filter(user=profileuser).first()
                profile_data = UserProfileSerializer(profile).data
                i.update({"profile_data":profile_data})
            
            # print(type(serializer),"||||||||||||||||||||||||||||||||||||||")
            return Response(serializer,status=status.HTTP_200_OK)
            # except Exception as e:
            #     return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': f'Error in searching becaus of {Exception} '})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'No query provided'})
        