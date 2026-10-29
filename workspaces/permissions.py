from rest_framework.permissions import BasePermission
from .models import WorksoaceMember


from rest_framework.permissions import BasePermission
from .models import WorksoaceMember


class IsWorkspaceMember(BasePermission):
  def has_object_permission(self, request, view, obj):
      membership = WorksoaceMember.objects.filter(
          workspace=obj,
          user=request.user,
      ).first()

      if not membership:
          return False

      if request.method in ("GET", "HEAD", "OPTIONS"):
          return True

      if request.method in ("PUT", "PATCH"):
          return membership.role in ("OWNER", "MANAGER")

      if request.method == "DELETE":
          return membership.role == "OWNER"

      return False


class IsProjectMember(BasePermission):
   def has_object_permission(self, request, view, obj):
      membership = WorksoaceMember.objects.filter(
        workspace=obj.workspace,
        user=request.user,
      ).first()

      if not membership:
          return False

      if request.method in ("GET", "HEAD", "OPTIONS"):
          return True

      if request.method in ("PUT", "PATCH"):
          return membership.role in ("OWNER", "MANAGER")

      if request.method == "DELETE":
          return membership.role == "OWNER"

      return False


class IsTaskMember(BasePermission):
  def has_object_permission(self, request, view, obj):
      membership = WorksoaceMember.objects.filter(
          workspace=obj.project.workspace,
          user=request.user,
      ).first()

      if not membership:
          return False

      if request.method in ("GET", "HEAD", "OPTIONS"):
          return True

      if request.method in ("PUT", "PATCH"):
          return membership.role in ("OWNER", "MANAGER")

      if request.method == "DELETE":
          return membership.role == "OWNER"

      return False