from django.db import models
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType

class Post(models.Model):
    title = models.CharField(max_length=2000)
    body = models.TextField()
    published = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey('users.CustomUser', null=True, on_delete=models.SET_NULL)
    block = models.ForeignKey('users.Block', null=True, on_delete=models.SET_NULL)
    tags = TaggableManager()
    likes = models.ManyToManyField('users.CustomUser', related_name='post_likes', blank=True)

    def __str__(self):
        return str(self.title)
        
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey('users.CustomUser',on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField('users.CustomUser', related_name='comment_likes', blank=True)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        if self.is_parent:
            return reverse('post_detail', args=[str(self.post.id)])
        return reverse('post_detail', args=[str(self.parent.post.id)])

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        if model_instance.is_parent:
            model_instance.post = self.post
        model_instance.post = self.post
        model_instance.author = self.request.user
        model_instance.author_id = self.request.user.id
        model_instance.published = datetime.now()
        model_instance.publish = True
        model_instance.save()
        return HttpResponseRedirect(self.get_success_url())

    def children(self):
        return Comment.objects.filter(parent=self).order_by('published')

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True