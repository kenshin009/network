from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from datetime import datetime
class User(AbstractUser):
    pass
 
class Post(models.Model):

    user = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return self.user

class LikePost(models.Model):

    post_id = models.IntegerField()
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class Profile(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField()
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username