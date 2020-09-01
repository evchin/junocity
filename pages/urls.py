from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('home/', views.home, name='home'),
    path('home/<str:pk>/', views.home_block, name='home_block'),
    path('about/', views.about, name='about'),
    path('browse/', views.browse, name='browse'),
    path('block/<str:pk>/', views.block, name='block'),
    path('join_block/<str:pk>/', views.join_block, name='join_block'),
    path('leave_block/<str:pk>/', views.leave_block, name='leave_block'), 
]