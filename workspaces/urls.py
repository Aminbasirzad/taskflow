from django.urls import path
from .views import WorkspaceListCreateView, WorkspaceDetailView, ProjectListCreateView, ProjectDetailView

urlpatterns = [
  path(
    'workspaces/',
    WorkspaceListCreateView.as_view(),
    name='workspace-list-create',
  ),

  path(
    'generics/<int:pk>',
    WorkspaceDetailView.as_view(),
    name='workspace-update-create',
  ),

  path(
    'projects/',
    ProjectListCreateView.as_view(),
    name='project-list-create',
  ),

  path(
    'projects/<int:pk>/',
    ProjectDetailView.as_view(),
    name='project-detail',
  )
]