import django_filters
from .models import Workspaces, Project


class WorkspaceFilter(django_filters.FilterSet):
  owner = django_filters.NumberFilter(field_name="owner_id")
  search = django_filters.CharFilter(
    field_name="name",
    lookup_expr="icontains"
  )

  class Meta:
    model = Workspaces
    fields = ["owner", "search"]


class ProjectFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(
    lookup_expr="icontains"
  )
  created_by = django_filters.NumberFilter(
    field_name="created_by_id"
  )

  class Meta:
    model = Project
    fields = ["name", "created_by"]