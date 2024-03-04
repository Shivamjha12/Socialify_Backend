from django.db import models
from accounts.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_Image = models.ImageField(upload_to='profile_image', blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    short_intro = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    interests = models.CharField(max_length=255, blank=True)
    friends_count = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return str(self.user.email)
    