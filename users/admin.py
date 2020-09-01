from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Block, NeighborRequest

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    filter_horizontal = ('neighbors',)
    list_display = ['username', 'first_name', 'last_name', 'email', 'birthday', 'phone', 'is_staff', 'date_created', 'bio', 'profile_pic']
    list_editable = ['first_name', 'last_name', 'email', 'birthday', 'phone', 'is_staff', 'bio', 'profile_pic']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Block)
admin.site.register(NeighborRequest)