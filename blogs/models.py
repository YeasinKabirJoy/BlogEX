from django.db import models
import uuid
from django.urls import reverse
from django.utils.text import slugify
from users.models import Profile
# Create your models here.


class Blog(models.Model):
    owner = models.ForeignKey(Profile,blank=True,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='images/',default='images/default.jpg',blank=True)
    file = models.FileField(upload_to='files/',blank=True,null=True)
    tags = models.ManyToManyField('Tag',blank=True,null=True)
    vote_total = models.IntegerField(default=0,blank=True,null=True)
    vote_ratio = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    slug = models.SlugField(default="",blank=True,null=False,max_length=1000)

    class Meta:
        ordering = ['-vote_ratio','-vote_total','title']
        # ordering = ['created']  ascending
        # ordering = ['-created'] descending

    def get_view_url(self):
        return reverse("single-blog",args=[self.slug])

    def get_update_url(self):
        return reverse("update-blog",args=[self.slug])

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    @property
    def imgURL(self):
        try:
            url = self.image.url
        except:
            url = '/media/images/default.jpg'
        return url
    @property
    def reviewers(self):
        queryset= self.review_set.all().values_list('owner__id',flat=True)
        return queryset

    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(vote='up').count()
        total_vote = reviews.count()
        ratio = (up_votes/total_vote) * 100

        self.vote_ratio = ratio
        self.vote_total = total_vote
        self.save()

    def __str__(self):
        return self.title


##kdjfkdsjfdskj




class Review(models.Model):
    VOTE_TYPE = (
        ("up","Up Vote"),
        ("down","Down Vote")
    )
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    vote = models.CharField(max_length=100,choices=VOTE_TYPE)
    review_text = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner','blog']]

    def __str__(self):
        return self.blog.title +" --- "+ self.vote





class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

