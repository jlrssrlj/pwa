from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from blogs.models import Blog, Categorias
from dashboards.forms import BlogPostForm, CategoryForm
from django.template.defaultfilters import slugify

# Create your views here.

@login_required
def categories(request):
    return render(request, 'dashboard/categories.html')

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_category.html',context)

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Categorias, pk=pk)
    if request.method=='POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'dashboard/edit_Category.html', context)

@login_required
def delete_category(request,pk):
    category = get_object_or_404(Categorias, pk=pk)
    category.delete()
    return redirect('categories')

#Vista de Blogs

def posts(request):
    posts = Blog.objects.all()
    context =  {
        'posts': posts,
    }
    return render(request,'dashboard/posts.html', context)


@login_required
def add_posts(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' +str(post.id)
            post.save()
            return redirect('posts')
    else:
        form = BlogPostForm()  # Agregar esta línea para definir form en una solicitud GET

    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_posts.html', context)


@login_required
def edit_posts(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method=='POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title)+ '-'+str(post.id)
            return redirect('posts')
    form = BlogPostForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'dashboard/edit_posts.html', context)

@login_required
def delet_posts(request,pk):
    posts = get_object_or_404(Blog, pk=pk)
    posts.delete()
    return redirect('posts')