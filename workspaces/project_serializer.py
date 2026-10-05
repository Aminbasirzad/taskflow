from rest_framework import serializers
from .models import Project, WorksoaceMember

class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    fields = "__all__"
    read_only_fields = [
      "id",
      "created_by",
      "created_at",
      "updated_at"
    ]
  def validate_workspace(self, workspace):
    is_member = WorksoaceMember.objects.filter(
      workspace=workspace,
      user=self.context["request"].user,
    ).exists()

    if not is_member:
      raise serializers.ValidationError(
        "You are not a member of this workspace"
      )
    return workspace