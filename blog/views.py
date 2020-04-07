from django.shortcuts import render, get_object_or_404, redirect
# used to pass contents of a page from one place to another, used
# here for linking between pages and deciding what to do
from django.http import HttpResponse, HttpResponseRedirect
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
  post_all_pinned = Post.objects.filter(pin=True)
  post_all_unpinned = Post.objects.filter(pin=False)
  post_all_pinned = post_all_pinned[::-1]
  post_all_unpinned = post_all_unpinned[::-1]
  post_all_pinned = list(post_all_pinned)
  post_all_unpinned = list(post_all_unpinned)

  post_all = post_all_pinned + post_all_unpinned

  list_likes = []

  if request.user.is_authenticated:
    likes = Like.objects.filter(user=request.user)
    likes_count = likes.count()

    for liked_posts in likes:
      list_likes.extend([liked_posts.post.pk])

  paginator = Paginator(post_all, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    # our 'posts' variable will be equal to our posts data.
    'posts': post_all,
    'likes_list': list_likes,
    'page_obj': page_obj,
  }


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
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    elif postID_pin != False:
      user = get_object_or_404(User, username=username)
      posts = Post.objects.filter(author=user, pin=True)
      pinnedCount = posts.count()
      
      if pinnedCount == 2:
        messages.error(request, f'Cannot pin more than 2 posts.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      
      else:
        obj = get_object_or_404(Post, pk=postID_pin)
        obj.pin = True
        obj.save()
        messages.warning(request, f'Pinned your post! "{obj.title}"')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif like != False:
      user_like = get_object_or_404(User, username=username)
      post_like = get_object_or_404(Post, pk=like)
      like_model = Like(user=user_like, post=post_like)
      like_model.save()

      messages.success(request, f'''You liked {post_like.author.username}'s post, "{post_like.title}"''')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif unlike != False:
      user_unlike = get_object_or_404(User, username=username)
      post_unlike = get_object_or_404(Post, pk=unlike)
      like_to_delete = get_object_or_404(Like, user=user_unlike, post=post_unlike)
      like_to_delete.delete()
      messages.success(request, f'''You unliked {post_unlike.author.username}'s post, "{post_unlike.title}"''')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
  likes = Like.objects.filter(post=obj)
  likes = list(likes)
  context = {
    'post': obj,
    'comments': comments,
    'form': form,
    'likes': likes,
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


def liked(request):
  user = request.user
  likes = Like.objects.filter(user=user)
  likes = likes[::-1]

  paginator = Paginator(likes, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  title = f"{user.username}'s likes!"
  context = {
    'likes': likes,
    'page_obj': page_obj,
    'title': title
  }

  return render(request, 'blog/likes.html', context)

def chat(request):
  users = User.objects.all()
  context = {
    'users': users,
  }
  return render(request, 'blog/messages.html', context)
