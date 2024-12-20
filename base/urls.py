from django.urls import path
from . import views
urlpatterns = [

    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('create-post/', views.createPost, name="create-post"),
    path('room/<str:pk>/', views.post, name="post"),
    path('types/', views.typesPage, name="types"),
    path('activities/', views.activityPage, name="activity"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),
    path('update-room/<str:pk>/', views.updatePost, name="update-post"),
    path('delete-room/<str:pk>/', views.deletePost, name="delete-post"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

]