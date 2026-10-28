from django.shortcuts import render
from rest_framework import generics
from .models import Workspaces, WorksoaceMember, Project, Task
from .serializers import WorkspaceSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWorkspaceMember, IsProjectMember, IsTaskMember
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import WorkspaceFilter, ProjectFilter, TaskFilter
from .project_serializer import ProjectSerializer
from .task_serializers import TaskSerializer


class WorkspaceListCreateView(generics.ListCreateAPIView):
  queryset = Workspaces.objects.all()
  serializer_class = WorkspaceSerializer
  permission_classes = [IsAuthenticated, IsWorkspaceMember]
  frilter_backends = [OrderingFilter]
  ordering_fields = ["name", "created_at"]
  ordering = ["name"]
  filter_backends = [
    DjangoFilterBackend,OrderingFilter,
  ]

  filterset_class = WorkspaceFilter

  def get_queryset(self):
    queryset = Workspaces.objects.filter(
      members__user=self.request.user
    )

    search = self.request.query_params.get("search")
    if search:
      queryset = queryset.filter(name__icontains=search)
    return queryset

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


class ProjectListCreateView(generics.ListCreateAPIView):
  serializer_class = ProjectSerializer
  permission_classes = [IsAuthenticated]
  ordering_fields = ["name", "created_at"]
  filterset_class = ProjectFilter
  ordering = ["created_at"]
  filter_backends = [
    DjangoFilterBackend,OrderingFilter,
  ]


  def get_queryset(self):
    return Project.objects.filter(
      workspace__members__user=self.request.user
    )

  def perform_create(self, serializer):
    serializer.save(
      created_by=self.request.user
    )




class ProjectDetailView(generics.RetrieveUpdateAPIView):
  serializer_class = ProjectSerializer
  permission_classes = [IsAuthenticated, IsProjectMember]

  def get_queryset(self):
    return Project.objects.filter(
      workspace__members__user=self.request.user
    )


class TaskListCreateView(generics.ListCreateAPIView):
  serializer_class = TaskSerializer
  permission_classes = [IsAuthenticated]
  filter_backends = [DjangoFilterBackend, OrderingFilter]
  filterset_class = TaskFilter
  ordering_fields = ["title", "created_at", "priority", "status"]
  ordering = ["-created_at"]

  def get_queryset(self):
    return Task.objects.filter(
      project__workspace__members__user=self.request.user
    ).distinct()

  def perform_create(self, serializer):
    serializer.save(
      created_by=self.request.user
    )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = TaskSerializer
  permission_classes = [IsAuthenticated, IsTaskMember]

  def get_queryset(self):
    return Task.objects.filter(
      project__workspace__members__user=self.request.user
    ).distinct()