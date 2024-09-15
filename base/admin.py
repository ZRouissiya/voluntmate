from django.contrib import admin

from .models import Post,Type,Message,User

admin.site.register(User)
admin.site.register(Type)
admin.site.register(Message)
admin.site.register(Post)
