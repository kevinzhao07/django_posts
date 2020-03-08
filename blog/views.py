from django.shortcuts import render, get_object_or_404
# used to pass contents of a page from one place to another, used
# here for linking between pages and deciding what to do
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

# what user will see when landing on blog home page, we have passed in 
# a template from the blog directory INSIDE our templates directory INSIDE
# our blog directory (seems redundant).
# NO LONGER USED!
def home(request):
  # context is full of our dummy posts that we pass into our home template.
  context = {
    # our 'posts' variable will be equal to our posts data.
    'posts': Post.objects.all()
  }
  return render(request, 'blog/home.html', context)

class PostListView(ListView):
  model = Post
  template_name = 'blog/home.html'
  context_object_name = 'posts'
  ordering = ['-date_posted']
  paginate_by = 5

class UserPostListView(ListView):
  model = Post
  template_name = 'blog/user_posts.html'
  context_object_name = 'posts'
  paginate_by = 5

  def get_queryset(self):
    user = get_object_or_404(User, username=self.kwargs.get('username'))
    return Post.objects.filter(author = user).order_by('-date_posted')

class PostDetailView(DetailView):
  model = Post
  context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['title', 'content']

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['title', 'content']

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  context_object_name = 'post'
  success_url = '/'

  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author

# what user will see when landing on about page
def about(request):
  return render(request, 'blog/about.html', {'title': 'titty'})