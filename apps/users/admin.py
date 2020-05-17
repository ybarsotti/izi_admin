from django.contrib import admin

from django.utils.translation import ugettext_lazy as _

from .models import User


@admin.register(User)
class UserAmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações pessoais'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissões'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (_('Datas importantes'), {'fields': ('last_login',)}),
    )

    readonly_fields = ('last_login', )