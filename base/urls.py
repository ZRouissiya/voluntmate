from django.urls import path
from . import views
urlpatterns = [

    path('', views.home, name="home"),
    path('create-post/', views.createPost, name="create-post"),
    path('room/<str:pk>/', views.post, name="post"),
    path('types/', views.typesPage, name="types"),
    path('activities/', views.activityPage, name="activity"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),

]