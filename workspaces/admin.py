from django.contrib import admin
from .models import Workspaces, WorksoaceMember, Project

@admin.register(Workspaces)
class workspacesAdmin(admin.ModelAdmin):
  list_display = ('name', 'owner', 'created_at')

@admin.register(WorksoaceMember)
class WorksoaceMemberAdmin(admin.ModelAdmin):
  list_display = ('workspace', 'user', 'role', 'joined_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
  list_display = ('name', 'description', 'workspace', 'created_by', 'created_at', 'updated_at')