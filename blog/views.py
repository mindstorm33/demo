from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost
from account.models import Account
from .forms import CreateBlogPostForm, UpdateBlogPostForm

# Create your views here.

def create_blog_view(request):
    """ view for creating a blog """

    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form  = CreateBlogPostForm()

        context['form'] = form

    return render(request, 'blog/create_blog.html', context)


def detail_blog_view(request, slug):
    """ render the page to display the datailed blog post. """

    context = {}
    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):

    context = {}

    user =  request.user 
    if not user.is_authenticated:
        return render('must_authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)
    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            context['success_message'] = 'Updated'
    form = UpdateBlogPostForm(
        initial={
            "title": blog_post.title,
            "body": blog_post.body,
            "image": blog_post.image,
        }
    )
    
    context['form'] = form
    return render(request, 'blog/edit_blog.html', context )
    
