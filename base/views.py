from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import PostForm,UserForm,MyUserCreationForm,ImageForm
import googlemaps
from django.conf import settings

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(
        Q(type__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    type = Type.objects.all()[0:5]
    post_count = posts.count()
    post_messages = Message.objects.filter(
        Q(post__type__name__icontains=q))[0:3]

    context = {'posts': posts, 'types': type,
               'post_count': post_count, 'post_messages': post_messages}
    return render(request, 'base/index.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    image_form=ImageForm()
    type = Type.objects.all()
    key = settings.GOOGLE_API_KEY

    if request.method == 'POST':
        type_name = request.POST.get('type')
        type, created = Type.objects.get_or_create(name=type_name)

        post = Post.objects.create(
            owner=request.user,
            type=type,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            lat=request.POST.get('lat'),
            lng=request.POST.get('lng')   ,
            place_name=request.POST.get('place_name')     
        )
        if request.FILES.getlist('images'):
                for image in request.FILES.getlist('images'):
                    Images.objects.create(
                        post=post,
                        user=request.user, 
                        image=image
                    )
        return redirect('home')

    context = {'form': form, 'types': type,'image_form':image_form, 'key':key}
    return render(request, 'base/post_form.html', context)

def post(request, pk):
    post = Post.objects.get(id=pk)
    post_messages = post.message_set.all()
    participants = post.participants.all()
    images=post.images.all()
    key = settings.GOOGLE_API_KEY

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        post.participants.add(request.user)
        return redirect('post', pk=post.id)
     
    context = {
                'post': post,
                'post_messages': post_messages,
                'participants': participants,
                'images':images,
                'key':key,
                'lat': float(post.lat),
                'lng' : float(post.lng),
                'place_name':post.place_name
                 }
    
    return render(request, 'base/post.html', context)

def typesPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    types = Type.objects.filter(name__icontains=q)
    return render(request, 'base/types.html', {'types': types})

def activityPage(request):
    post_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'post_messages': post_messages})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    post_messages = user.message_set.all()
    types = Type.objects.all()
    context = {'user': user, 'posts': posts,
               'post_messages': post_messages, 'types': types}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    images=post.images.all()
    types = Type.objects.all()
    if request.user != post.owner:
        return redirect('home')

    if request.method == 'POST':
        type_name = request.POST.get('type')
        type, created = Type.objects.get_or_create(name=type_name)
        post.name = request.POST.get('name')
        post.type = type
        post.description = request.POST.get('description')
        post.save()
        for image in request.FILES.getlist('images'):
                Images.objects.create(
                    post=post,
                    user=request.user,  
                    image=image
                )
        return redirect('home')

    context = {'form': form, 'types': types, 'post': post,'images':images}
    return render(request, 'base/post_form.html', context)

@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.owner:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': post})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return redirect('home')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

