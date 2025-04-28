from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админ-панель для управления CustomUser."""
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('is_active', 'is_staff',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
