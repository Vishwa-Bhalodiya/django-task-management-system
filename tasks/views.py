from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail


from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['assigned_to', 'status']

    def perform_create(self, serializer):
        user = self.request.user

        # Only admin can create tasks
        if not user.is_superuser:
            raise PermissionDenied("Only admin can create tasks")

        task = serializer.save()

        send_mail(
            subject=f'New Task Assigned: {task.title}',
            message=task.description,
            from_email='vishupatel13297@gmail.com',
            recipient_list=[task.assigned_to.email],
        )

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Task.objects.all()

        return Task.objects.filter(assigned_to=user)
