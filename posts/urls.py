from django.urls import path
from . import views
from .views import (
    PostUpdateView,
    PostDeleteView,
    PostCreateView,
)

urlpatterns = [
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='post_edit'),
    path('post_detail/<str:pk>/', views.post_detail, name='post_detail'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'), 
    path('new/', PostCreateView.as_view(), name='post_new'),
    path('block/<str:block_pk>/', views.post_list, name='post_list'),
    path('trending_list/', views.trending_list, name='trending_list'), 
    path('change-bookmark/<str:pk>', views.change_bookmark, name='change_bookmark'),
    path('change-post-like/<str:pk>', views.change_post_like, name='change_post_like'),
    path('change-comment-like/<str:pk>', views.change_comment_like, name='change_comment_like'),
    path('delete_comment/<str:id>/', views.comment_delete, name='delete_comment'), 
]