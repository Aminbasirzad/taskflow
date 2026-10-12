from django.db import models
from django.conf import settings


class Workspaces(models.Model):
  name = models.CharField(max_length=200)
  owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name


class WorksoaceMember(models.Model):
  class Role(models.TextChoices):
    OWNER = 'OWNER', 'Owner'
    MANAGER = 'MANAGER', 'Manager'
    MEMBER = 'MEMBER', 'Member'
  workspace = models.ForeignKey(
    Workspaces,
    on_delete=models.CASCADE,
    related_name='members'
)
  
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
) 
  
  role = models.CharField(
    max_length=20,
    choices=Role.choices,
     default=Role.MEMBER
)
  
  joined_at = models.DateTimeField(auto_now_add=True)
  

class Project(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=250)

  workspace = models.ForeignKey(
    Workspaces,
    on_delete=models.CASCADE
)

  created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
  class Status(models.TextChoices):
    TODO = "TODO", "To Do"
    INPROGRESS = "IN_PROGRESS", "In Progress"
    DONE = "DONE", "Done"
  class Priority(models.TextChoices):
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGT = "HIGT", "Higt"

  title = models.CharField(max_length=100)
  description = models.TextField()

  status = models.CharField(
    max_length=20,
    choices=Status.choices,
    default=Status.TODO,
  )

  Priority = models.CharField(
    max_length=20,
    choices=Priority.choices,
    default=Priority.MEDIUM,
  )

  project = models.ForeignKey(
    Project,
    on_delete=models.CASCADE,
    related_name="tasks"
  )
  assignee = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="assigned_tasks"
  )

  created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="created_tasks",
  )

  created_at = models.DateTimeField(auto_now_add=True)

  update_at = models.DateTimeField(auto_now=True)