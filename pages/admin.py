from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from pages.models import AuthorModel, PostModel


class AuthorInline(admin.StackedInline):
    model = AuthorModel
    can_delete = False
    verbose_name_plural = 'Author'
    extra = 0


class CustomUserAdmin(BaseUserAdmin):
    inlines = [AuthorInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ('message', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = (
        'message',
        'author__user__username',
        'author__user__first_name',
        'author__user__last_name',
    )


@admin.register(AuthorModel)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


# Avval eski UserAdmin'ni olib tashlaymiz
admin.site.unregister(User)
# Keyin o‘zimiz yozganini qayta ro‘yxatdan o‘tkazamiz
admin.site.register(User, CustomUserAdmin)
