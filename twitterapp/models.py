from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
import os
# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('documents',filename)
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='static/',default='documents/default.jpg')
    DOB=models.DateField(null=True,blank=True)
    city=models.CharField(max_length=128,null=True,blank=True)
    phone=models.CharField(max_length=128,null=True,blank=True)
    Gender=models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.DOB

    def create_profile(sender,**kwargs):
        if kwargs['created']:
            user_profile=Profile.objects.create(user=kwargs['instance'])
    post_save.connect(create_profile,sender=User)

class Followers(models.Model):
    user_id=models.IntegerField()
    following = models.IntegerField(default=0)

class Tweet(models.Model):
    title=models.CharField(max_length=128)
    image=models.ImageField(upload_to='static/',null=True,blank=True)
    #video=models.URLField(null=True,blank=True)
    date_created= models.DateTimeField(default=timezone.now().replace(microsecond=0))
    def __str__(self):
        return self.title
    posts=models.ForeignKey(User,on_delete=models.CASCADE)

class FollowRequests(models.Model):
    uid=models.IntegerField()
    fid=models.IntegerField()

class Like(models.Model):
    postId=models.IntegerField()
    UserId=models.IntegerField()

class Comment(models.Model):
    postId=models.IntegerField()
    UserId=models.IntegerField()
    comment=models.CharField(max_length=128)


