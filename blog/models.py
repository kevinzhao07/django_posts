from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model): 
  title = models.CharField(max_length=100)
  content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  pin = models.BooleanField(default=False)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.CharField(max_length=280)
  date_posted = models.DateTimeField(default=timezone.now)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)

  def __str__(self):
    return self.post.title

class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  date_liked = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.user.username} liked a post'

class Message(models.Model):
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
  message = models.TextField()
  date_sent = models.DateTimeField(default=timezone.now)
  def __str__(self):
    return f'{self.sender.username} sent {self.receiver.username} a message'