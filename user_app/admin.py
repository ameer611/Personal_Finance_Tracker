from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        ('Permissions', {'fields': ('first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')}),
    )
    list_display = ('email', 'first_name', 'date_joined', 'is_active')  # Can display date_joined
    ordering = ('email',)
    exclude = ('last_login',)

admin.site.register(CustomUser, CustomUserAdmin)
