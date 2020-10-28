from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post
from django.views.decorators.csrf import csrf_exempt




def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request , 'blog/home.html', context = context)

@csrf_exempt
def vote(request, pk):
    vote_type = request.POST.get('type')
    vote_action = request.POST.get('action')

    post = get_object_or_404(Post , pk = pk) 
    
    thisUserUpvote = post.upvotes.filter(id = request.user.id).count()
    thisUserDownvote = post.downvotes.filter(id = request.user.id).count()

    if(vote_action == 'vote'):
        if(thisUserUpvote==0 and thisUserDownvote == 0):
            if(vote_type == 'up'):
                post.upvotes.add(request.user)
            elif(vote_type == 'down'):
                post.downvotes.add(request.user)
            else:
                return HttpResponse("Error, Unknown vote type")
        else:
            return HttpResponse("Already Voted")
    elif (vote_action == 'recall'):
        if(vote_type=='up' and thisUserUpvote == 1):
            post.upvotes.remove(request.user)
        elif(vote_type == 'down' and thisUserDownvote == 1):
            post.downvotes.remove(request.user)
        else :
            return HttpResponse("Error, Unknown vote type or no  vote to recall")
    else :
        return HttpResponse("Error, Bad Action")

    thisUserUpvote = post.upvotes.filter(id = request.user.id).count()
    thisUserDownvote = post.downvotes.filter(id = request.user.id).count()
    post.score = thisUserUpvote - thisUserDownvote
    return HttpResponse(post.score)
            




class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name ='posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User , username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    success_url ='/blog/'

    def test_func(self):
        return self.get_object().author == self.request.user

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title' , 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title' , 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author;
