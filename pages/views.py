from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from users.models import CustomUser, Block
from users.forms import CustomUserChangeForm
from posts.models import Post
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.db.models.functions import datetime
from datetime import datetime, timedelta

def about(request):
	return render(request, 'about.html')

def intro(request):
	return render(request, 'intro.html')

@login_required(login_url='login')
def home(request):
	user = request.user
	neighbors = user.neighbors.all()
	posts = Post.objects.filter(Q(author=user))
	current_time = datetime.now(tz=timezone.utc)
	trending_posts = Post.objects.filter(published__range=[current_time - timedelta(days=5), current_time])
	trending_posts = trending_posts.annotate(like_count=Count('likes')).order_by('-like_count')[:10]
	for neighbor in neighbors:
		posts = posts | Post.objects.filter(Q(author=neighbor)) 
	posts = posts.order_by('-published')
	blocks = user.blocks.all()
	root = 'Your Neighbors'
	context = {'user': user, 'posts': posts, 'blocks': blocks, 'root': root, 'trending_posts': trending_posts}
	return render(request, 'home.html', context)

@login_required(login_url='login')
def home_block(request, pk):
	posts = Post.objects.filter(block_id=pk)
	user = request.user
	blocks = user.blocks.all()
	root = Block.objects.get(id=pk).name
	current_time = datetime.now(tz=timezone.utc)
	trending_posts = Post.objects.filter(published__range=[current_time - timedelta(days=5), current_time])
	trending_posts = trending_posts.annotate(like_count=Count('likes')).order_by('-like_count')[:10]
	context = {'user': user, 'posts': posts, 'blocks': blocks, 'root': root,'pk': pk, 'trending_posts': trending_posts}
	return render(request, 'home.html', context)

@login_required(login_url='login')
def profile(request):
	user = request.user
	form = CustomUserChangeForm(instance=user)
	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save() 
	context = {'form': form}
	return render(request, 'profile.html', context)

@login_required(login_url='login')
def browse(request):
	block_list = None
	user_list = None
	post_list = None
	neighbor_list = None
	main_blocks = Block.objects.filter(pk__range=(1, 6))
	user = request.user
	query = request.GET.get("q")
	if query:
		block_list = Block.objects.filter(Q(name__icontains=query) | Q(tags__slug__icontains=query)).distinct()
		neighbor_list = user.neighbors.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query)).distinct()
		user_list = CustomUser.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query)).distinct() 
		post_list = Post.objects.filter(Q(tags__slug__icontains=query) | Q(title__icontains=query)).distinct().order_by('-published')
	if neighbor_list and user_list:
		user_list = neighbor_list | user_list
	context = {'block_list': block_list, 'user_list': user_list, 'post_list': post_list, 'main_blocks': main_blocks}
	return render(request, 'browse.html', context)

@login_required(login_url='login')
def block(request, pk):
	block = Block.objects.get(id=pk)
	posts = Post.objects.filter(block=block).order_by('-published')
	current_time = datetime.now(tz=timezone.utc)
	trending_posts = posts.filter(published__range=[current_time - timedelta(days=5), current_time])
	trending_posts = trending_posts.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
	posts = posts.exclude(id__in=trending_posts)
	population = block.customuser_set.all()
	blocks = request.user.blocks.all()
	if block in blocks:
		in_user_blocks = True
	else:
		in_user_blocks = False
	context = {'block': block, 'name': block.name, 'pk': block.pk, 'description':block.description, 'founder': block.founder, 'population': population.count,
			'date_created': block.date_created, 'tags': block.tags, 'posts': posts, 'pk': pk, 'in_user_blocks': in_user_blocks, 'trending_posts': trending_posts} 
	return render(request, 'block.html', context)   

@login_required(login_url='login')
def join_block(request, pk):
    user = request.user
    block = Block.objects.get(pk=pk)
    user.blocks.add(block)
    return redirect('block', pk=pk)

@login_required(login_url='login')
def leave_block(request, pk):
	user = request.user
	block = Block.objects.get(pk=pk)
	user.blocks.remove(block)
	return redirect('block', pk=pk)

