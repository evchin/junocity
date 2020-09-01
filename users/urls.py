from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signupPage, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('neighbor-request/send/<str:pk>/', views.send_neighbor_request, name='send_neighbor_request'), 
    path('neighbor-request/ignore/<str:pk>/', views.ignore_neighbor_request, name='ignore_neighbor_request'),
    path('neighbor-request/cancel/<str:pk>/', views.cancel_neighbor_request, name='cancel_neighbor_request'),
    path('neighbor-request/accept/<str:pk>/', views.accept_neighbor_request, name='accept_neighbor_request'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('bookmarks-list/', views.bookmarks_list, name='bookmarks_list'),
    path('remove-neighbor/<str:pk>/', views.remove_neighbor, name='remove_neighbor'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_form.html'), name='password_reset_form'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_complete'),
]