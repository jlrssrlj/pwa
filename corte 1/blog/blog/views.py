from django.shortcuts import redirect, render
from blogs.models import Blog, Categorias
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib import auth
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

@require_http_methods(["GET", "POST"])
def home(request):
    
    posts = Blog.objects.filter(is_featured = True).order_by('update_at')
    context = {        
        'featured_posts': posts
    }
    return render(request, 'home.html', context)

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name = 'blog_group')
            group.user_set.add(user)
            
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
            return redirect('home')

    form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'login.html',context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')