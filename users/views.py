from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from .decorators import unauthenticated_user, allowed_users
from django.core.exceptions import PermissionDenied 
from django.shortcuts import get_list_or_404, get_object_or_404
from itertools import chain
from .forms import CustomUserChangeForm
import os
from django.http import HttpResponseRedirect

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')
	context = {}
	return render(request, 'registration/login.html', context)

@unauthenticated_user
def signupPage(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            junocity = CustomUser.objects.get(username='junocity')
            user.neighbors.add(junocity)
            junocity.neighbors.add(user)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'signup.html', context)
	
def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def send_neighbor_request(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    neighbor_request, created = NeighborRequest.objects.get_or_create(from_user=request.user, to_user=user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def ignore_neighbor_request(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    neighbor_request = NeighborRequest.objects.filter(from_user=user, to_user=request.user).first()
    neighbor_request.delete()
    return redirect('profile', pk=request.user.pk)

@login_required(login_url='login')
def cancel_neighbor_request(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    neighbor_request = NeighborRequest.objects.filter(from_user=request.user, to_user=user).first()
    neighbor_request.delete()
    return redirect('profile', pk=request.user.pk)

@login_required(login_url='login')
def accept_neighbor_request(request, pk):
    from_user = get_object_or_404(CustomUser, pk=pk)
    neighbor_request = NeighborRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = neighbor_request.to_user
    user2 = from_user
    user1.neighbors.add(user2)
    user2.neighbors.add(user1)
    neighbor_request.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def remove_neighbor(request, pk):
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    user2 = CustomUser.objects.get(pk=pk)
    new_user_neighbors = user.neighbors.exclude(pk=user2.pk)
    new_user2_neighbors = user2.neighbors.exclude(pk=user.pk)
    user.neighbors.set(new_user_neighbors)
    user2.neighbors.set(new_user2_neighbors)
    return redirect('profile', pk=request.user.pk)

@login_required(login_url='login')
def profile(request, pk):
    current_user = CustomUser.objects.get(pk=pk)
    sent_neighbor_requests = NeighborRequest.objects.filter(from_user=current_user)
    received_neighbor_requests = NeighborRequest.objects.filter(to_user=current_user)
    neighbors = current_user.neighbors.all()
    posts = Post.objects.filter(author=current_user)
    blocks = current_user.blocks.all()
    user_profile_pic = current_user.profile_pic.url
    head, tail = os.path.split(user_profile_pic)
    tail, query = tail.split('?')

    button_status = 'none'
    if current_user not in request.user.neighbors.all():
        button_status = 'not_neighbor'
        if len(NeighborRequest.objects.filter(from_user=request.user).filter(to_user=current_user)) == 1:
            button_status = 'neighbor_request_sent'
        elif len(NeighborRequest.objects.filter(from_user=current_user).filter(to_user=request.user)) == 1:
            button_status = 'neighbor_request_received'

    context = {'current_user': current_user, 'button_status': button_status, 'neighbors': neighbors, 'blocks': blocks,
            'sent_nrequests': sent_neighbor_requests, 'received_nrequests': received_neighbor_requests, 'posts': posts, 'profile_pic': user_profile_pic}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def account_settings(request):
    user = request.user
    form = CustomUserChangeForm(instance=user)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('first_name')
            messages.success(request, 'Profile was saved for ' + name)
    context = {'form':form}
    return render(request, 'account_settings.html', context)

@login_required(login_url='login') 
def bookmarks_list(request):
    user = request.user
    bookmarks = user.bookmarks.all().order_by('-published')
    context = {'bookmarks': bookmarks}
    return render(request, 'bookmarks_list.html', context)