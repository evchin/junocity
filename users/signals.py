from django.db.models.signals import post_save, m2m_changed, post_delete
from .models import CustomUser, Block, NeighborRequest
from posts.models import Post, Comment
from notifications.signals import notify
from django.core.signals import request_finished
from django.dispatch import receiver
    
# notify.send(actor, recipient, verb, action_object, target, level, description, public, timestamp, **kwargs)

@receiver(post_save, sender=NeighborRequest)
def neighbor_request(sender, instance, created, **kwargs):
    notify.send(instance.from_user, recipient=instance.to_user, verb='sent you a', timestamp=instance.timestamp)

@receiver(m2m_changed, sender=CustomUser.neighbors.through)
def new_neighbor(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            new_neighbor = model.objects.get(pk=pk)
            notify.send(instance, recipient=new_neighbor, verb='has become your')

@receiver(post_save, sender=Comment)
def comment_on_post(sender, instance, created, **kwargs):
    if created:
        notify.send(instance.author, recipient=instance.post.author, verb='commented', timestamp=instance.published, action_object=instance, target=instance.post)