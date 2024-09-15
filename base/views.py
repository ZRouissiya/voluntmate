from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User,Post,Type,Message
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import PostForm

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
    type = Type.objects.all()
    if request.method == 'POST':
        type_name = request.POST.get('type')
        type, created = Type.objects.get_or_create(name=type_name)

        Post.objects.create(
            owner=request.user,
            type=type,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'types': type}
    return render(request, 'base/post_form.html', context)

def post(request, pk):
    post = Post.objects.get(id=pk)
    post_messages = post.message_set.all()
    participants = post.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        post.participants.add(request.user)
        return redirect('post', pk=post.id)

    context = {'post': post, 'post_messages': post_messages,
               'participants': participants}
    return render(request, 'base/post.html', context)