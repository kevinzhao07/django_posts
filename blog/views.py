from django.shortcuts import render, get_object_or_404, redirect
# used to pass contents of a page from one place to another, used
# here for linking between pages and deciding what to do
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Like
from .forms import CommentForm
from django.utils import timezone
import math

# what user will see when landing on blog home page, we have passed in 
# a template from the blog directory INSIDE our templates directory INSIDE
# our blog directory (seems redundant).
# NO LONGER USED!
def home(request):
  # context is full of our dummy posts that we pass into our home template.
  post_all = Post.objects.all()
  post_all = post_all[::-1]

  likes = Like.objects.filter(user=request.user)
  likes_count = likes.count()

  list_likes = []
  for liked_posts in likes:
    list_likes.extend([liked_posts.post.pk])

  if request.method == "POST":
    
    postID_pin = request.POST.get('pinned', False)
    postID_unpin = request.POST.get('unpinned', False)
    like = request.POST.get('like', False)
    unlike = request.POST.get('unlike', False)
    username = request.user.username

    if postID_unpin != False:
      obj = get_object_or_404(Post, pk=postID_unpin)
      obj.pin = False
      obj.save()
      messages.info(request, f'Unpinned your post "{obj.title}"')
      return redirect('blog-home')
    
    elif postID_pin != False:
      user = get_object_or_404(User, username=username)
      posts = Post.objects.filter(author=user, pin=True)
      pinnedCount = posts.count()
      
      if pinnedCount == 2:
        messages.error(request, f'Cannot pin more than 2 posts.')
        return redirect('blog-home')
      
      else:
        obj = get_object_or_404(Post, pk=postID_pin)
        obj.pin = True
        obj.save()
        messages.warning(request, f'Pinned your post! "{obj.title}"')
        return redirect('blog-home')

    elif like != False:
      user_like = get_object_or_404(User, username=username)
      post_like = get_object_or_404(Post, pk=like)
      like_model = Like(user=user_like, post=post_like)
      like_model.save()

      messages.success(request, f'''You liked {post_like.author.username}'s post, "{post_like.title}"''')
      return redirect('blog-home')

    elif unlike != False:
      user_unlike = get_object_or_404(User, username=username)
      post_unlike = get_object_or_404(Post, pk=unlike)
      like_to_delete = get_object_or_404(Like, user=user_unlike, post=post_unlike)
      like_to_delete.delete()
      messages.success(request, f'''You unliked {post_unlike.author.username}'s post, "{post_unlike.title}"''')
      return redirect('blog-home')

  context = {
    # our 'posts' variable will be equal to our posts data.
    'posts': post_all,
    'likes_list': list_likes,
  }

  return render(request, 'blog/home.html', context)

class UserPostListView(ListView):
  model = Post
  template_name = 'blog/user_posts.html'
  context_object_name = 'posts'
  paginate_by = 5

  def get_queryset(self):
    user = get_object_or_404(User, username=self.kwargs.get('username'))
    return Post.objects.filter(author = user).order_by('-date_posted')

@login_required
def detail(request, *args, **kwargs):

  def form_valid(form, request):
    obj = get_object_or_404(Post, pk=kwargs['pk'])
    modelForm = form.save(commit = False)
    modelForm.post = obj
    modelForm.author = request.user
    modelForm.date_posted = timezone.now()
    modelForm.save()
    return redirect('post-detail', pk=kwargs['pk'])

  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      messages.success(request, f'commented!')
      return form_valid(form, request)
  else:
    form = CommentForm()

  obj = get_object_or_404(Post, pk=kwargs['pk'])
  comments = Comment.objects.filter(post=obj)
  comments = list(comments)
  context = {
    'post': obj,
    'comments': comments,
    'form': form
  }
  return render(request, 'blog/post_detail.html', context)
 

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