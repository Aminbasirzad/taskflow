from rest_framework import serializers
from .models import Task, WorksoaceMember


class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = "__all__"

    read_only_fields = [
      "id",
      "created_by",
      "created_at",
      "updated_at",
    ]

  def validate_peoject(self, project):
    is_member = WorksoaceMember.objects.filter(
      workspaces=project.workspace,
      user=self.context["request"].user,
    ).exists()

    if not is_member:
      raise serializers.ValidationError(
        "You are not a member of this workspace"
      )

    return project