from django import forms
from . models import BlogPost


class CreateBlogPostForm(forms.ModelForm):
    """ form for creating blogposts """


    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']