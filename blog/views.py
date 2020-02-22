from django.shortcuts import render
# used to pass contents of a page from one place to another, used
# here for linking between pages and deciding what to do
from django.http import HttpResponse

# what user will see when landing on blog home page
def home(request):
  return HttpResponse('<h1>Blog Home</h1>')

# what user will see when landing on about page
def about(request):
  return HttpResponse('<h1>About Page</h1>')