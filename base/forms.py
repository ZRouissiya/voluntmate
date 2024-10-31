from .models import Post,User,Images
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['owner', 'participants', 'lat', 'lng']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'gendre', 'username', 'email', 'age']
        
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username','email','gendre', 'age']

class ImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['image'] 

        
