from django.db import models

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

# helper method for uploading images
def upload_location(instance, filename):
    """ unique location of where the image will be uploaded. """
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title),
        filename=filename
    )
    return file_path

# blog post model
class BlogPost(models.Model):
    """ Model of a blogpost """
    title                   = models.CharField(max_length=50, null=False, blank=False)
    body                    = models.TextField(max_length=5000, null=False, blank=False)
    image                   = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published          = models.DateTimeField(auto_now_add=True, verbose_name='date published')
    date_updated            = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug                    = models.SlugField(blank=True, unique=True)

    def __str__(self):
        """ return a string reprentation of the model"""
        return self.title

#  when the blog post is deleted, delete the image associated with it(?)
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

# add a slug to the blog post if it doesn't have one already
def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)


