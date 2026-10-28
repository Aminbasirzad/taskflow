from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Workspaces, WorksoaceMember, Project, Task


User = get_user_model()


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )

        self.workspace = Workspaces.objects.create(
            name="Test Workspace",
            owner=self.user,
        )

        WorksoaceMember.objects.create(
            workspace=self.workspace,
            user=self.user,
            role=WorksoaceMember.Role.OWNER,
        )

        self.project = Project.objects.create(
            name="Test Project",
            description="Project for API tests",
            workspace=self.workspace,
            created_by=self.user,
        )

        self.client.force_authenticate(user=self.user)


    def test_member_cannot_update_task(self):
        member = User.objects.create_user(
            username="member",
            password="TestPassword123!",
        )
        WorksoaceMember.objects.create(
            workspace=self.workspace,
            user=member,
            role=WorksoaceMember.Role.MEMBER,
        )

        self.client.force_authenticate(user=member)
        task = Task.objects.create(
            title="Original Task",
            description="Test",
            project=self.project,
            created_by=self.user,
        )

        response = self.client.patch(
            f"/api/tasks/{task.id}/",
            {"title": "Changed Task"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        task.refresh_from_db()
        self.assertEqual(task.title, "Original Task")

    def test_member_cannot_delete_task(self):
        member = User.objects.create_user(
            username="member2",
            password="TestPassword123!",
        )
        WorksoaceMember.objects.create(
            workspace=self.workspace,
            user=member,
            role=WorksoaceMember.Role.MEMBER,
        )

        self.client.force_authenticate(user=member)
        task = Task.objects.create(
            title="Task to Keep",
            description="Test",
            project=self.project,
            created_by=self.user,
        )

        response = self.client.delete(f"/api/tasks/{task.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_outsider_cannot_view_task(self):
        outsider = User.objects.create_user(
            username="outsider",
            password="TestPassword123!",
        )
        task = Task.objects.create(
            title="Private Task",
            description="Test",
            project=self.project,
            created_by=self.user,
        )

        self.client.force_authenticate(user=outsider)
        response = self.client.get(f"/api/tasks/{task.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task(self):
        response = self.client.post(
            "/api/tasks/",
            {
                "title": "Test Task",
                "description": "Testing task creation",
                "status": "TODO",
                "priority": "HIGH",
                "project": self.project.id,
            },
            format="json",
            
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().created_by, self.user)



    def test_manager_can_update_task(self):
        manager = User.objects.create_user(
            username="manager",
            password="TestPassword123!",
        )
        WorksoaceMember.objects.create(
            workspace=self.workspace,
            user=manager,
            role=WorksoaceMember.Role.MANAGER,
        )

        task = Task.objects.create(
            title="Original Task",
            description="Test",
            project=self.project,
            created_by=self.user,
        )

        self.client.force_authenticate(user=manager)
        response = self.client.patch(
            f"/api/tasks/{task.id}/",
            {"title": "Updated by Manager"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated by Manager")

    def test_manager_cannot_delete_task(self):
        manager = User.objects.create_user(
            username="manager2",
            password="TestPassword123!",
        )
        WorksoaceMember.objects.create(
            workspace=self.workspace,
            user=manager,
            role=WorksoaceMember.Role.MANAGER,
        )

        task = Task.objects.create(
            title="Task to Keep",
            description="Test",
            project=self.project,
            created_by=self.user,
        )

        self.client.force_authenticate(user=manager)
        response = self.client.delete(f"/api/tasks/{task.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Task.objects.filter(id=task.id).exists())


    def test_owner_can_update_task(self):
        task = Task.objects.create(
            title="Original Task",
            description="Test",
            project=self.project,
            created_by=self.user,
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/tasks/{task.id}/",
            {"title": "Updated by Owner"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated by Owner")

    def test_owner_can_delete_task(self):
        task = Task.objects.create(
            title="Task to Delete",
            description="Test",
            project=self.project,
            created_by=self.user,
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/tasks/{task.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_create_task_with_invalid_priority(self):
        response = self.client.post(
            "/api/tasks/",
            {
                "title": "Invalid Priority Task",
                "description": "Testing invalid priority",
                "status": "TODO",
                "priority": "URGENT",
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)


    def test_create_task_without_title(self):
        response = self.client.post(
            "/api/tasks/",
            {
                "description": "Task without title",
                "status": "TODO",
                "priority": "HIGH",
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)