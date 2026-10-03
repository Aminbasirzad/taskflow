from django.urls import path
from .views import WorkspaceListCreateView, WorkspaceDetailView

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
]