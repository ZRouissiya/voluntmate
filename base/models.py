from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    SEXE_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    age = models.IntegerField(null=True)
    gendre=models.CharField(max_length=1,choices=SEXE_CHOICES,default='M',null=True)
    avatar = models.ImageField(upload_to='avatars/',null=True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
