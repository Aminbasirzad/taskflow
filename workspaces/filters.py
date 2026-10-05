import django_filters
from .models import Workspaces


class WorkspaceFilter(django_filters.FilterSet):
  owner = django_filters.NumberFilter(field_name="owner_id")
  search = django_filters.CharFilter(
    field_name="name",
    lookup_expr="icontains"
  )

  class Meta:
    model = Workspaces
    fields = ["owner", "search"]