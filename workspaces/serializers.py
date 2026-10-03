from rest_framework import serializers
from .models import Workspaces

class WorkspaceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Workspaces
    fields = "__all__"
    reas_only_fields = ["id", "created_at", "owner"]

  def validate_name(self, value):
    if len(value) < 3:
      raise serializers.ValidationError(
        "Workspace name must be at leats 3 charcters."
      )
    return value