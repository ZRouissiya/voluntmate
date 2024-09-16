from .models import Post,User
from django.forms import ModelForm

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['owner', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'gendre', 'username', 'email', 'age']