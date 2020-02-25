from django.shortcuts import render
# used to pass contents of a page from one place to another, used
# here for linking between pages and deciding what to do
from django.http import HttpResponse

posts = [
  {
    'author': 'leborn jaems',
    'title': 'winnin da chip',
    'content': 'neva again deadass',
    'date_posted': 'June 19 2017'
  },
  {
    'author': 'steven carry',
    'title': 'loosin da chip',
    'content': 'neva again deadass',
    'date_posted': 'June 19 2017'
  }
]

# what user will see when landing on blog home page, we have passed in 
# a template from the blog directory INSIDE our templates directory INSIDE
# our blog directory (seems redundant).
def home(request):
  # context is full of our dummy posts that we pass into our home template.
  context = {
    # our 'posts' variable will be equal to our posts data.
    'posts': posts,
  }
  return render(request, 'blog/home.html', context)

# what user will see when landing on about page
def about(request):
  return render(request, 'blog/about.html')