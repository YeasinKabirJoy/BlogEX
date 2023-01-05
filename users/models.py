import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    user_name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True,null=True,default="profiles/user-default.png")
    short_intro = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    location = models.CharField(max_length=200,blank=True,null=True)
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    slug = models.SlugField(default="", blank=True, null=False, max_length=1000)

    @property
    def imgURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = '/media/profiles/user-default.png'
        return url

    class Meta:
        ordering = ['created']

    def save(self,*args,**kwargs):
        self.slug = slugify(self.user_name)
        super().save(*args,**kwargs)

    def __str__(self):
        if self.name:
            return "name: "+str(self.name)
        else:
            return "username: "+str(self.user_name)


class Skill(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f'{self.owner.name} ----- {self.name}'


class Message(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,blank=True,null=True,related_name='send_messages')
    recipient = models.ForeignKey(Profile,on_delete=models.SET_NULL,blank=True,null=True,related_name='messages')
    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=200,blank=True,null=True)
    subject= models.CharField(max_length=200,blank=True,null=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read','-created']
