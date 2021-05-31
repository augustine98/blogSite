from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Community(models.Model):
    name = models.CharField(primary_key=True, max_length = 15)
    description = models.TextField(max_length=100)
    date_created = models.DateTimeField(default = timezone.now)
    # members = models.ManyToManyField(User , blank = True , related_name='comm_members')

    class Meta:
        verbose_name_plural = "Communities"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('comm-list',kwargs={'name' : self.name })

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User , on_delete= models.CASCADE)
    upvotes = models.ManyToManyField(User, blank = True, related_name='post_upvotes')
    downvotes = models.ManyToManyField(User,blank = True, related_name='post_downvotes')
    posted_to = models.ForeignKey(Community , on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk' : self.pk})
    
class Comment(models.Model):
    body = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    post = models.ForeignKey(Post , related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User , on_delete= models.CASCADE)

    def __str__(self):
        return self.body 
    
