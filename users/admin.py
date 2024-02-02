from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models.users import User


admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        ('Идентификаторы пользователя', {'fields': ('email', 'username',)}),
        ('Личная информация', {'fields': ('first_name', 'last_name',)}),
        ('Параметры доступа', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        # ('Параметры доступа', {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        # }),
        ('Важные даты', {'fields': ('date_joined', 'last_login',)}),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'phone_number', 'password1', 'password2',),
    #     }),
    # )
    list_display = ('id', 'username', 'full_name', 'email', )

    list_display_links = ('id', 'username', 'full_name',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',)
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login', 'date_joined')