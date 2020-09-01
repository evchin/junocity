from django import forms
from .models import Post, Comment
from users.models import CustomUser

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ('content',) 