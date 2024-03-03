from django.db import models
from accounts.models import *   
# Create your models here.
from django.db import models
from accounts.models import User
import uuid
from datetime import datetime

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postid = models.UUIDField(default=uuid.uuid4, editable=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    
    def add_like(self):
        self.likes += 1
        self.save()

    def formatted_date(self):
        return self.created_at.strftime('%d/%m/%Y')
    def __str__(self):
        return str(self.postid)+" "+str(self.user.email)
    
class Photo(models.Model):
    post = models.ForeignKey(Post, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_photos')
    caption = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.post.postid
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Convert the date field to the desired format before saving
        if isinstance(self.created_at,str):
            self.created_at = datetime.strptime(self.created_at, '%d/%m/%Y')
        super().save(*args, **kwargs)
        
    def formatted_date(self):
        return self.created_at.strftime('%d/%m/%Y')
    
    def __str__(self):
        return str(self.content[:5]) + '...' + str(self.post.postid)

    
