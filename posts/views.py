from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied 
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from .models import Post, Comment
from .forms import *
from users.models import CustomUser, Block
import json
from django.db.models.functions import datetime
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Count

@login_required(login_url='login')
def change_bookmark(request, pk):
    if request.method=='POST' and request.is_ajax():
        post = Post.objects.get(pk=pk)
        user = request.user 
        if post in user.bookmarks.all():
            user.bookmarks.remove(post)    
        else:
            user.bookmarks.add(post)
        return JsonResponse({'result': 'ok'}) 
    else:
        return JsonResponse({'result': 'nok'})

@login_required(login_url='login')
def trending_list(request):
    current_time = datetime.now(tz=timezone.utc)
    trending_posts = Post.objects.filter(published__range=[current_time - timedelta(days=7), current_time])
    trending_posts = trending_posts.annotate(like_count=Count('likes')).order_by('-like_count')[:20]
    context = {'trending_posts': trending_posts}
    return render(request, 'trending_list.html', context)

@login_required(login_url='login')
def change_post_like(request, pk):
    if request.method=='POST' and request.is_ajax():
        post = Post.objects.get(pk=pk)
        user = request.user 
        if user in post.likes.all():
            post.likes.remove(user)  
        else:
            post.likes.add(user)  
        post.save()
        return JsonResponse({'result': 'ok'}) 
    else:
        return JsonResponse({'result': 'nok'})

@login_required(login_url='login')
def change_comment_like(request, pk):
    if request.method=='POST' and request.is_ajax():
        comment = Comment.objects.get(pk=pk)
        user = request.user 
        if user in comment.likes.all():
            comment.likes.remove(user)  
        else:
            comment.likes.add(user)
        comment.save()
        return JsonResponse({'result': 'ok'}) 
    else:
        return JsonResponse({'result': 'nok'})

@login_required(login_url='login')
def post_list(request, block_pk):
    posts = Post.objects.filter(block_id=block_pk)
    comments = []
    for p in posts:
        comments += Comment.objects.filter(post_id=p.pk)
    context = {'posts': posts, 'comments': comments}
    return render(request, 'post_list.html', context)

@login_required(login_url='login')
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.comments.filter(parent=None)
    comment_form = AddCommentForm(request.POST) 
    if request.method == 'POST':
        comment_form = AddCommentForm(request.POST) 
        if comment_form.is_valid(): 
            comment = comment_form.save(commit=False)
            comment.content = request.POST.get('content')
            comment.post = post
            comment.author = request.user
            parent_obj = None
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj = parent_qs.first()
            comment.parent = parent_obj
            comment.save()
            return redirect(request.META.get('HTTP_REFERER'))
    context = {'post': post, 'comments': comments, 'comment_form': comment_form} 
    return render(request, 'post_detail.html', context)

@login_required(login_url='login')
def comment_delete(request, id):
    obj = get_object_or_404(Comment, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect(obj.get_absolute_url())
    context = {'object': obj}
    return render(request, 'confirm_delete.html', context)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'body', 'block', 'tags')
    template_name = 'post_edit.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ('title', 'body', 'block', 'tags')
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.author = self.request.user        
        return super().form_valid(form)