from django.shortcuts import render
from rest_framework import generics
from .models import Workspaces, WorksoaceMember
from .serializers import WorkspaceSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWorkspaceMember


class WorkspaceListCreateView(generics.ListCreateAPIView):
  queryset = Workspaces.objects.all()
  serializer_class = WorkspaceSerializer
  permission_classes = [IsAuthenticated, IsWorkspaceMember]


  def get_queryset(self):
    return Workspaces.objects.filter(
      members__user=self.request.user
    )

  def perform_create(self, serializer):
    workspace = serializer.save(owner=self.request.user)

    WorksoaceMember.objects.create(
      workspace=workspace,
      user=self.request.user,
      role=WorksoaceMember.Role.OWNER
    )


class WorkspaceDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Workspaces.objects.all()
  serializer_class = WorkspaceSerializer