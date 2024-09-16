from .models import Post,User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['owner', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'gendre', 'username', 'email', 'age']
        
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username','email','gendre', 'age']
        
