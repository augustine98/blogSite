from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Community(models.Model):
    name = models.CharField(max_length = 15)
    description = models.TextField(max_length=100)
    date_created = models.DateTimeField(default = timezone.now)
    # members = models.ManyToManyField(User , blank = True , related_name='comm_members')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('comm-list',kwargs={'pk' : self.pk})

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User , on_delete= models.CASCADE)
    upvotes = models.ManyToManyField(User, blank = True, related_name='post_upvotes')
    downvotes = models.ManyToManyField(User,blank = True, related_name='post_downvotes')
    posted_to = models.ManyToManyField(Community , blank = True , related_name='posted_to_community')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk' : self.pk})
    


