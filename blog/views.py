# needed to redirect and render pages from templates
# get_object_or_404: use to get an object using a specific field inside that model
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

# needed to restrict some pages to users who are logged in 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# make sure to import all models/forms that are used
from django.contrib.auth.models import User
from .forms import CommentForm, MessageForm, TodoForm, PostForm
from .models import Post, Comment, Like, Message, Todo
from django.utils import timezone

# views, pagination, messages, others
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import math

# not using class based views for home/detail (bigger views)

def home(request):

  # separating pinned/unpinned posts to put pinned on top (still ordering by date)
  post_all_pinned = Post.objects.filter(pin=True)
  post_all_unpinned = Post.objects.filter(pin=False)
  post_all_pinned = post_all_pinned.order_by('-date_posted')
  post_all_unpinned = post_all_unpinned.order_by('-date_posted')
  post_all_pinned = list(post_all_pinned)
  post_all_unpinned = list(post_all_unpinned)

  post_all = post_all_pinned + post_all_unpinned

  # stats count
  if request.user.is_authenticated:
    posts_by_me = Post.objects.filter(author=request.user)
    comments_by_me = Comment.objects.filter(author=request.user)
    likes_by_me = Like.objects.filter(user=request.user)
  else:
    posts_by_me = Post.objects.filter(title="not in")
    comments_by_me = Comment.objects.filter(content="comment")
    likes_by_me = Like.objects.filter()

  # populate list_likes with post.pk of posts that have been liked by the user that is logged in
  list_likes = []

  if request.user.is_authenticated:
    likes = Like.objects.filter(user=request.user)
    likes_count = likes.count()

    for liked_posts in likes:
      list_likes.extend([liked_posts.post.pk])

  # pass in all likes
  likes = Like.objects.all()

  # 10, 5, 1
  post_count = posts_by_me.count()
  post_count_10 = post_count // 10
  post_count_5 = (post_count - (post_count_10 * 10)) // 5
  post_count_1 = (post_count - (post_count_10 * 10) - (post_count_5 * 5))

  comment_count = comments_by_me.count()
  comment_count_10 = comment_count // 10
  comment_count_5 = (comment_count - (comment_count_10 * 10)) // 5
  comment_count_1 = (comment_count - (comment_count_10 * 10) - (comment_count_5 * 5))

  like_count = likes_by_me.count()
  like_count_10 = like_count // 10
  like_count_5 = (like_count - (like_count_10 * 10)) // 5
  like_count_1 = (like_count - (like_count_10 * 10) - (like_count_5 * 5))

  # can write our own function inside a function to make valid form handling easier
  def form_valid(form, request):

    # since author/post/date_posted is not explicitly defined inside the form, we want to save everything we have
    # so far (commit = False), and using the same object, fill in the other entries
    modelForm = form.save(commit = False)
    modelForm.author = request.user
    modelForm.date_posted = timezone.now()
    modelForm.pin = False
    modelForm.save()
    return redirect('blog-home')

  if request.method == "POST":
    form = PostForm(request.POST)
    if form.is_valid():
      return form_valid(form, request)
  else:
    form = PostForm()

  # context includes now all posts (in pinned/unpinned order), array of all posts liked, and page #
  context = {
    'posts': post_all,
    'likes_list': list_likes,
    'likes': likes,
    'posts_by_me': post_count,
    'number_by_me_10': [0] * int(post_count_10),
    'number_by_me_5': [0] * int(post_count_5),
    'number_by_me_1': [0] * int(post_count_1),
    'comments_by_me': comment_count,
    'comment_by_me_10': [0] * int(comment_count_10),
    'comment_by_me_5': [0] * int(comment_count_5),
    'comment_by_me_1': [0] * int(comment_count_1),
    'likes_by_me': like_count,
    'like_by_me_10': [0] * int(like_count_10),
    'like_by_me_5': [0] * int(like_count_5),
    'like_by_me_1': [0] * int(like_count_1),
    'form': form,
  }

    # # if form has been submitted -- all "forms" are in the form of submit buttons with hidden input lines
    # if request.method == "POST":
      
    #   # used to process which submit button was clicked, the others will return False (best solution?)
    #   postID_pin = request.POST.get('pinned', False)
    #   postID_unpin = request.POST.get('unpinned', False)
    #   like = request.POST.get('like', False)
    #   unlike = request.POST.get('unlike', False)

    #   username = request.user.username

    #   # if unpin button is clicked, we can retrieve the affected post by postID and SAVE it (important!)
    #   if postID_unpin != False:
    #     obj = get_object_or_404(Post, pk=postID_unpin)
    #     obj.pin = False
    #     obj.save()
    #     messages.info(request, f'Unpinned your post "{obj.title}"')
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # allows redirect to the same page in pagination
      
    #   elif postID_pin != False:
    #     user = get_object_or_404(User, username=username)
    #     posts = Post.objects.filter(author=user, pin=True)
    #     pinnedCount = posts.count()
        
    #     if pinnedCount == 2:
    #       messages.error(request, f'Cannot pin more than 2 posts.')
    #       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    #     else:
    #       obj = get_object_or_404(Post, pk=postID_pin)
    #       obj.pin = True
    #       obj.save()
    #       messages.warning(request, f'Pinned your post! "{obj.title}"')
    #       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # # creates/deletes a new Like model for every like/unlike
    # elif like != False:
    #   user_like = get_object_or_404(User, username=username)
    #   post_like = get_object_or_404(Post, pk=like)
    #   like_model = Like(user=user_like, post=post_like)
    #   like_model.save()

    #   messages.success(request, f'''You liked {post_like.author.username}'s post, "{post_like.title}"''')
    #   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # elif unlike != False:
    #   user_unlike = get_object_or_404(User, username=username)
    #   post_unlike = get_object_or_404(Post, pk=unlike)
    #   like_to_delete = get_object_or_404(Like, user=user_unlike, post=post_unlike)
    #   like_to_delete.delete()
    #   messages.success(request, f'''You unliked {post_unlike.author.username}'s post, "{post_unlike.title}"''')
    #   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

  return render(request, 'blog/home2.html', context)

def like(request):
  if request.method == "GET":
    post_pk = request.GET['post_pk']
    like_user = request.GET['like_user']
    liked_post = Post.objects.get(pk=post_pk)
    liked_user = User.objects.get(username=like_user)
    new_like = Like(user=liked_user, post=liked_post)
    new_like.save()
    return HttpResponse('success')
  else:
    return HttpResponse('unsuccessful')

def unlike(request):
  if request.method == "GET":
    post_pk = request.GET['post_pk']
    like_user = request.GET['like_user']
    liked_post = Post.objects.get(pk=post_pk)
    liked_user = User.objects.get(username=like_user)
    old_like = get_object_or_404(Like, user=liked_user, post=liked_post)
    old_like.delete()
    return HttpResponse('success')
  else:
    return HttpResponse('unsuccessful')

def pin(request):
  if request.method == "GET":
    post_pk = request.GET['post_pk']
    post_to_pin = Post.objects.get(pk=post_pk)
    post_to_pin.pin = True
    post_to_pin.save()
    return HttpResponse('success')
  else:
    return HttpResponse('unsuccessful')

def unpin(request):
  if request.method == "GET":
    post_pk = request.GET['post_pk']
    post_to_pin = Post.objects.get(pk=post_pk)
    post_to_pin.pin = False
    post_to_pin.save()
    return HttpResponse('success')
  else:
    return HttpResponse('unsuccessful')

# same as home view with less functionality, but in a Class based view
class UserPostListView(ListView):
  model = Post
  template_name = 'blog/user_posts.html'
  context_object_name = 'posts'

  def get_queryset(self):
    user = get_object_or_404(User, username=self.kwargs.get('username'))
    return Post.objects.filter(author = user).order_by('-date_posted')

# login required to view page (will redirect to login)
@login_required
def detail(request, *args, **kwargs):

  # can write our own function inside a function to make valid form handling easier
  def form_valid(form, request):

    # since author/post/date_posted is not explicitly defined inside the form, we want to save everything we have
    # so far (commit = False), and using the same object, fill in the other entries
    obj = get_object_or_404(Post, pk=kwargs['pk'])
    modelForm = form.save(commit = False)
    modelForm.post = obj
    modelForm.author = request.user
    modelForm.date_posted = timezone.now()
    modelForm.save()
    return redirect('post-detail', pk=kwargs['pk'])

  # if not valid form, simply returns
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      messages.success(request, f'commented!')
      return form_valid(form, request)
  else:
    form = CommentForm()

  # passes in all comments/likes to display in details
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
 
# simple create view overwriting form_valid
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

# todo view?
def about(request):

  def form_valid(form, request):
    todoForm = form.save(commit = False)
    todoForm.author = request.user
    todoForm.save()
    return redirect('blog-about')

  if request.method == "POST":
    form = TodoForm(request.POST)
    if form.is_valid():
      return form_valid(form, request)
  else:
    form = TodoForm()

  todo_all = Todo.objects.all()

  context = {
    'form': form,
    'todos': todo_all,
  }

  return render(request, 'blog/about.html', context)

# filters all likes on one page, keeps pin/unpin
@login_required
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

# message page displaying all users, also takes the form functionality of the personal message page
# where users can change colors of chat bubbles
@login_required
def chat(request):
  users = User.objects.all()

  # if color was changed, update all colors accordingly between user messages
  if request.method == "POST":
    color = request.POST.get('color', False)
    username = request.POST.get('receiver', False)
    receiver = get_object_or_404(User, username=username)
    sender = request.user
    messages_sender = list(Message.objects.filter(sender=sender, receiver=receiver))
    messages_receiver = list(Message.objects.filter(sender=receiver, receiver=sender))
    for message in messages_sender:
      message.color = color
      message.save()
    
    return redirect('messages-person', username=username)

  # display last message and count sent // TODO: get You:/Them: to work?
  message_out = Message.objects.filter(sender=request.user)
  message_in = Message.objects.filter(receiver=request.user)
  message_all = message_out.union(message_in).order_by('date_sent')
  message_dictionary = {}
  message_count = {}
  
  for m in message_all:
    if m.sender == request.user:
      front = m.sender.username
      back = m.receiver.username 
    else:
      front = m.receiver.username
      back = m.sender.username
    key = front + back
    message_dictionary[key] = m.message
    if message_count.get(key) == None:
      message_count[key] = 1
    else:
      message_count[key] += 1

  context = {
    'users': users,
    'message_dictionary': message_dictionary,
    'our_username': request.user.username,
    'message_count': message_count,
  }
  return render(request, 'blog/messages.html', context)

def messagesend(request):
  if request.method == "GET":
    sender = request.user
    receiver_username = request.GET['receiver_username']
    receiver = get_object_or_404(User, username=receiver_username)
    text = request.GET['message_text']
    color = request.GET['color_message']
    new_message = Message(sender=sender, receiver=receiver, color=color, message=text, date_sent=timezone.now())
    new_message.save()
    return HttpResponse('success')
  else:
    return HttpResponse('unsuccessful')

# simple form handling of creating new messages
@login_required
def messagesPerson(request, *args, **kwargs):

  def form_valid(form, request):
    receive = get_object_or_404(User, username=kwargs['username'])
    send = request.user
    messages_all_one = Message.objects.filter(sender=send, receiver=receive)
    if len(messages_all_one) == 0:
      color = 'regular-blue'
    else:
      color = messages_all_one[0].color
    messageForm = form.save(commit = False)
    messageForm.date_posted = timezone.now()
    messageForm.sender = send
    messageForm.receiver = receive
    messageForm.color = color
    messageForm.save()
    return redirect('messages-person', username=kwargs['username'])

  if request.method == "POST":
    form = MessageForm(request.POST)
    if form.is_valid():
      return form_valid(form, request)
  else:
    form = MessageForm()
  
  # ordering messages by date sent
  receive = get_object_or_404(User, username=kwargs['username'])
  send = request.user
  messages_all_one = Message.objects.filter(sender=send, receiver=receive)
  if len(messages_all_one) == 0:
    color = 'regular-blue'
  else:
    color = messages_all_one[0].color
  messages_all_two = Message.objects.filter(sender=receive, receiver=send)
  messages_all = messages_all_one.union(messages_all_two).order_by('date_sent')
  user = request.user.username

  context = {
    'messages_all': messages_all,
    'form': form,
    'username_logged_in': user,
    'user_to_message': receive,
    'color_message': color,
    'receiver_username': kwargs['username'],
  }

  return render(request, 'blog/messages_person.html', context)
