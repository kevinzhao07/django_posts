# .py file is used for linking to other pages
from django.urls import path
from .views import PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
# import views.py in order to use home function (for linking)
from . import views

# second parameter is either a class based view or a view function (imported)
urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>', views.detail, name='post-detail'),
    path('post/new', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('liked/', views.liked, name="user-likes"),
    path('messages/', views.chat, name="messages"),
    path('like/', views.like, name='like'),
    path('pin/', views.pin, name='pin'),
    path('unpin/', views.unpin, name='unpin'),
    path('unlike/', views.unlike, name='unlike'),
    path('messages/<str:username>', views.messagesPerson, name="messages-person")
]