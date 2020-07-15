from django.db import models
from taggit.managers import TaggableManager
# Create your models here.
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField 
from PIL import Image 
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(allow_unicode=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    content = RichTextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default ='default-post.jpg', upload_to= 'post_pics',null=False,blank=False)
    status = models.IntegerField(choices=STATUS, default=1)
    tags = TaggableManager()
    importance = models.BooleanField(null=False)
    # here status 0 is Draft and 1 is published and it is out.
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        # let's this image is more than 300 pixels

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("post_detail", kwargs={"slug": str(self.slug)})
    
'''
Django ships with built-in syndication feed generating framework, which is used to generate dynamic Atom and RSS feeds.

RSS is an abbreviation for Really Simple Syndication, it’s a way to have information delivered to you instead of you having to go find it. 
RSS is basically a structured XML document that includes full or summarized text along with other metadata such as published date, author name, etc.
'''
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = RichTextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)