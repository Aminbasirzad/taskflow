from rest_framework.permissions import BasePermission
from .models import WorksoaceMember


class IsWorkspaceMember(BasePermission):
  def has_object_permission(self, request, view, obj):
    membership = WorksoaceMember.objects.filter(
      workspace=obj,
      user=request.user
    ).filter()

    if not membership:
      return False

    if request.method == 'GET':
      return True

    if request.method in  ["PATCH", "PUT"] and membership.role in ["OWNER", "MANAGER"]:
      return True

    if request.method == "DELETE" and membership.role == "OWNER":
      return True



class IsProjectMember(BasePermission):

  def has_object_permission(self, request, view, obj):
    return WorksoaceMember.objects.filter(
      workspace=obj.workspace,
      user=request.uzer
    ).exists()