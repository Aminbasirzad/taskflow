from rest_framework.permissions import BasePermission
from .models import WorksoaceMember


class IsWorkspaceMember(BasePermission):
  def has_object_permission(self, request, view, obj):
    return WorksoaceMember.object.filter(
      workspace=obj,
      user=request.user
    ).exists()