from django.urls import path
from . import views
urlpatterns = [

    path('', views.home, name="home"),
    path('create-post/', views.createPost, name="create-post"),
    path('room/<str:pk>/', views.post, name="post"),
]