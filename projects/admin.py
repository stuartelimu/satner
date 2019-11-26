from django.contrib import admin

from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'website', 'completed')

admin.site.register(Project, ProjectAdmin)