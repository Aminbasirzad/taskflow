from django.shortcuts import render
from rest_framework import generics
from .models import Workspaces
from .serializers import WorkspaceSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWorkspaceMember


class WorkspaceListCreateView(generics.ListCreateAPIView):
  queryset = Workspaces.objects.all()
  serializer_class = WorkspaceSerializer
  permission_classes = [IsAuthenticated, IsWorkspaceMember]

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class WorkspaceDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Workspaces.objects.all()
  serializer_class = WorkspaceSerializer