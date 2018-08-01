from django.urls import path
from django.contrib.auth import views
from twitterapp.Views import user
# app_name="fb"
urlpatterns = [
    path(r'',views.login,{'template_name':'twitter/login.html'},name='login'),
    path(r'login/', views.login, {'template_name': 'twitter/login_page.html'}, name="login"),
    path(r'logout/', views.logout, {'template_name': 'twitter/login.html'}, name="logout"),
    path(r'register',user.register,name="register"),
    path(r'home/',user.home,name="home"),
    path(r'addtweet/',user.addtweet,name="addtweet"),
    path(r'api/search/', user.SearchUser, name="search"),
    path(r'profile/<int:pk>',user.Updateprofile.as_view(),name="profile"),
    path(r'likepost/', user.likePost, name='likepost'),
    path(r'addcomment', user.AddComment, name='addcomment'),
    path(r'viewprofile/<int:userid>',user.viewprofile,name='viewprofile'),
    path(r'follow',user.AcceptFriend,name="follow"),
    path(r'following/',user.following,name="following"),
    path(r'followers/',user.followers,name="followers"),
    #path(r'signup/',user.register,name="signup"),
    ]