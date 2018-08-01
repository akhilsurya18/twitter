from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.shortcuts import redirect,render
from django import forms
from rest_framework import generics
from django.views import View
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from django.forms import ModelForm
from django import forms
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.db.models import Q
from datetime import datetime as dt
from rest_framework.views import APIView
import json
from rest_framework.response import Response
from rest_framework import serializers
from PIL import Image
from twitterapp.models import *

class Registrationform(UserCreationForm):
    class Meta:
        model=User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
    def save(self,commit=True):
        user=super(Registrationform,self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user

def register(request):
    if request.method=='POST':
        form=Registrationform(request.POST)
        # import ipdb
        # ipdb.set_trace()
        if form.is_valid():
            form.save()
            userid=User.objects.values('id').latest('id')
            f=Followers(user_id=userid['id'],id=userid['id'])
            f.save()
            return redirect('login')
        else:
            return redirect('register')
    else:
        form=Registrationform()
        args={'form':form}
        return render(request,'twitter/register.html',args)

def home(request):
    user = request.user
    following = Followers.objects.filter(id=request.user.id)
    # followers=Followers.objects.filter(fid=request.user.id)
    tweets = Tweet.objects.filter(Q(posts_id__in=[f.id for f in following]) | Q(posts_id=user.id)).order_by(
        '-date_created')
    t = []
    for p in tweets:
        c = Comment.objects.filter(postId=p.id)
        likecnt = Like.objects.filter(postId=p.id).count()
        tweet_user_id = Tweet.objects.values('posts_id').get(id=p.id)
        tweet_username = User.objects.values('username').get(id=tweet_user_id['posts_id'])
        tweet_user_profilephoto = Profile.objects.values('profile_picture').get(user_id=tweet_user_id['posts_id'])
        date = Tweet.objects.values('date_created').get(id=p.id)
        t.append({'p': p, 'c': c, 'likecnt': likecnt, 'tweetusername': tweet_username,
                  'tweetuserprofile': tweet_user_profilephoto, 'tweetdate': date})

    like = Like.objects.values('postId').filter(UserId=request.user.id)
    likelis = []
    for likeobj in like:
        likelis.append(likeobj['postId'])

    args = {'user': user, 'tweets': t, 'like': likelis,  'following': following}
    return render(request, 'twitter/home.html', args)

def addtweet(request):
    text=request.GET['text']
    tweet=Tweet(title=text,date_created=dt.now(),posts_id=request.user.id)
    # import ipdb
    # ipdb.set_trace()
    tweet.save()
    return HttpResponse("Success")

class UserdataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username=serializers.CharField()
    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.username = validated_data.get('name', instance.name)
        instance.save()
        return instance

def SearchUser(request):
    if request.method == "GET":
        # import ipdb
        # ipdb.set_trace()
        users = User.objects.all().filter(username__icontains=request.GET['query'])
        serializers = UserdataSerializer(users, many=True)
        return JsonResponse(serializers.data, safe=False)

def followers(request):
    foll=Followers.objects.values('user_id').filter(following=request.user.id)
    followers=User.objects.values().filter(id__in=[f['user_id'] for f in foll])
    args={'followers':followers}
    return render(request,'twitter/profilefolder/followers.html',args)

def following(request):
    foll = Followers.objects.values('following').filter(user_id=request.user.id)
    following = User.objects.values().filter(id__in=[f['following'] for f in foll])
    args = {'following': following}
    return render(request,'twitter/profilefolder/following.html',args)

class Addprofile(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['id','user']


class Updateprofile(UpdateView):
    model=Profile
    template_name = 'twitter/profile.html'
    form_class = Addprofile
    success_url = reverse_lazy('home')

def likePost(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        # import ipdb
        # ipdb.set_trace()
        if not Like.objects.filter(postId=post_id,UserId=request.user.id).exists():
            like=Like(postId=post_id,UserId=request.user.id)
            like.save()
        else:
            Like.objects.filter(postId=post_id,UserId=request.user.id).delete()
        likecnt=Like.objects.filter(postId=post_id).count()
        return HttpResponse(likecnt)
    else:
        return HttpResponse("0")

def AddComment(request):
    if request.method=="GET":
        post_id = request.GET['post_id']
        comment=request.GET['comment']
        cmt=Comment(postId=post_id,UserId=request.user.id,comment=comment)
        cmt.save()
        return HttpResponse('Success!!')
    else:
        return HttpResponse("Failed!!")

def viewprofile(request,userid):
    user=request.user
    foll = Followers.objects.values('following').filter(user_id=request.user.id)
    users=User.objects.all().exclude(id=user.id).exclude(id__in=[f['following'] for f in foll])
    tweets = Tweet.objects.filter(posts_id=user.id).order_by('-date_created')
    t = []
    for p in tweets:
        c = Comment.objects.filter(postId=p.id)
        likecnt = Like.objects.filter(postId=p.id).count()
        tweet_user_id = Tweet.objects.values('posts_id').get(id=p.id)
        tweet_username = User.objects.values('username').get(id=tweet_user_id['posts_id'])
        tweet_user_profilephoto = Profile.objects.values('profile_picture').get(user_id=tweet_user_id['posts_id'])
        date = Tweet.objects.values('date_created').get(id=p.id)
        t.append({'p': p, 'c': c, 'likecnt': likecnt, 'tweetusername': tweet_username,
                  'tweetuserprofile': tweet_user_profilephoto, 'tweetdate': date})

    like = Like.objects.values('postId').filter(UserId=request.user.id)
    likelis = []
    for likeobj in like:
        likelis.append(likeobj['postId'])
    args = {'u':userid, 'tweets': t, 'like': likelis,'people':users}
    return render(request,'twitter/view_profile.html',args)

def AcceptFriend(request):
    if request.method=="GET":
        fid = request.GET['friend_id']
        f2 = Followers.objects.create(user_id=request.user.id,following=fid)
        f2.save()
        return HttpResponse("Success!")
    else:
        return HttpResponse("Failed!")

