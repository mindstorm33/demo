from django.shortcuts import render, redirect
from .models import BlogPost
from account.models import Account
from .forms import CreateBlogPostForm

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
    
