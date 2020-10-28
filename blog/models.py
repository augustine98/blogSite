from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User , on_delete= models.CASCADE)
    upvotes = models.ManyToManyField(User,blank = True, related_name='post_upvotes')
    downvotes = models.ManyToManyField(User,blank = True, related_name='post_downvotes')
    score = models.IntegerField(default= 0)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk' : self.pk})
    
class Community(models.Model):
    title = models.CharField(max_length = 15)
    description = models.TextField(max_length=100)
    date_created = models.DateTimeField(default = timezone.now)
    members = models.ManyToManyField(User , blank = True , related_name='comm_members')

    def __str__(self):
        return self.title

