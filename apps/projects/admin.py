from django.contrib import admin

from apps.projects.models import Sprint, Project, Column

admin.site.register(Column)
admin.site.register(Project)
admin.site.register(Sprint)