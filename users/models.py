from django.db import models
from django.contrib.postgres.fields import CICharField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from taggit.managers import TaggableManager
from posts.models import Post
import datetime

class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    bio = models.TextField(max_length=400, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="default-profile.png", null=True, blank=True)
    neighbors = models.ManyToManyField("CustomUser", blank=True)
    blocks = models.ManyToManyField("Block", blank=True)
    bookmarks = models.ManyToManyField(Post, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def age(self):
        return int((datetime.date.today() - self.birthday).days / 365.25)

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self):
        return "/users/profile/{}".format(self.pk)

class Block(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    founder = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = TaggableManager()
    
    def __str__(self):
        return str(self.name)

class NeighborRequest(models.Model):
    to_user = models.ForeignKey(CustomUser, related_name='to_user', null=True, on_delete=models.SET_NULL)
    from_user = models.ForeignKey(CustomUser, related_name='from_user', null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user, self.to_user)