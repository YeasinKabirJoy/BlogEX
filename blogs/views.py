from django.http import Http404
from django.shortcuts import render,redirect
from .models import Blog,Tag
from .forms import BlogForm,ReviewForm
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import search_blog,paginate_blogs
# Create your views here.


def blogs(request):
    all_blogs,search_text = search_blog(request)

    all_blogs,custom_range = paginate_blogs(request,all_blogs,6)

    context ={
        'blogs':all_blogs,
        'search_text':search_text,
        'custom_range':custom_range
    }

    return render(request, 'blogs/blogs.html',context)


def single_blog(request,slug):
    blog = get_object_or_404(Blog,slug=slug)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.blog = blog
            review.owner = request.user.profile
            review.save()
            blog.get_vote_count
            messages.success(request, 'Your review was added successfully')
            return redirect('single-blog',slug=blog.slug)
    context={
        'blog':blog,
        'form':form
    }
    return render(request, 'blogs/single-blog.html',context)


@login_required(login_url='login')
def add_blog(request):
    profile = request.user.profile
    blog_form = BlogForm()

    if request.method == 'POST':
        newtags = request.POST.get("newtags").replace(',', ' ').split()
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = profile
            blog.save()
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)
                blog.tags.add(tag)

            messages.success(request,'Blog Added')
            return redirect('account')

    context={
        'form':blog_form,
    }
    return render(request, 'blogs/blog-form.html', context)


@login_required(login_url='login')
def update_blog(request,slug):
    profile = request.user.profile
    try:
        blog = profile.blog_set.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404
    blog_form = BlogForm(instance=blog)

    if request.method == 'POST':
        newtags = request.POST.get("newtags").replace(',',' ').split()
        form = BlogForm(request.POST,request.FILES,instance=blog)
        if form.is_valid():
            blog=form.save()
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)
                blog.tags.add(tag)
            messages.success(request, 'Blog Updated')
            return redirect('account')

    context={
        'form':blog_form,
        "blog":blog
    }
    return render(request, 'blogs/blog-form.html', context)


@login_required(login_url='login')
def delete_blog(request, id):
    profile = request.user.profile
    try:
        blog = profile.blog_set.get(id=id)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == "POST":
        blog.delete()
        return redirect('account')
    context={
        'object':blog
    }
    return render(request,"delete-object.html",context)