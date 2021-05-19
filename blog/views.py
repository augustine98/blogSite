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
from .models import Post, Community
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
    
    thisUserUpVote = post.upvotes.filter(id = request.user.id).count()
    thisUserDownVote = post.downvotes.filter(id = request.user.id).count()

    if(vote_action == 'vote'):
        if(vote_type == 'up'):
            if(thisUserUpVote == 1):
                return HttpResponse("Already Voted")
            elif(thisUserDownVote == 1):
                post.downvotes.remove(request.user)
            post.upvotes.add(request.user)
        elif(vote_type == 'down'):
            if(thisUserDownVote == 1):
                return HttpResponse("Already Voted")
            elif(thisUserUpVote == 1):
                post.upvotes.remove(request.user)
            post.downvotes.add(request.user)
    elif (vote_action == 'recall-vote'):
        if(vote_type=='up' and thisUserUpVote == 1):
            post.upvotes.remove(request.user)
        elif(vote_type == 'down' and thisUserDownVote == 1):
            post.downvotes.remove(request.user)
        else :
            return HttpResponse("Error, Unknown vote type or no  vote to recall")
    else :
        return HttpResponse("Error, Bad Action")

    return HttpResponse(post.upvotes.count() - post.downvotes.count())
            




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

class PostDetailView(LoginRequiredMixin , DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        post = get_object_or_404(Post , pk = self.kwargs.get('pk'))
        user = get_object_or_404(User , pk = self.request.user.id)
        context['thisUserUpVote'] = post.upvotes.filter(id = user.id).count()
        context['thisUserDownVote'] = post.downvotes.filter(id = user.id).count()
        context['postScore'] = post.upvotes.count() - post.downvotes.count()
        print(context['thisUserUpVote'] , context['thisUserDownVote'] , context['postScore'])  
        print(context)
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    success_url ='/'

    def test_func(self):
        return self.get_object().author == self.request.user

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title' , 'content' , 'posted_to']

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


class CommunityCreateView(LoginRequiredMixin , CreateView):
    model = Community
    fields = ['name' , 'description']

    def form_valid(self , form):
        # form.instance.members.add(self.request.user)
        return super().form_valid(form)

class CommunityListView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        comm = get_object_or_404(Community, name = self.kwargs.get('name'))
        return Post.objects.filter(posted_to = comm).order_by('-date_posted')
