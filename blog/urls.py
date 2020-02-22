# .py file is used for linking to other pages
from django.urls import path
# import views.py in order to use home function (for linking)
from . import views

# views.home returns HttpResponse that we are on "blog-home" page
# always have trailing / when adding paths
urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about')
]