from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.core.cache import cache
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
        
        #Clear cache for assigned user
        cache.delete(f"tasks_user_{task.assigned_to.id}")
        cache.delete(f"tasks_user_{user.id}") #admin

        send_mail(
            subject=f'New Task Assigned: {task.title}',
            message=task.description,
            from_email='vishupatel13297@gmail.com',
            recipient_list=[task.assigned_to.email],
        )

    def get_queryset(self):
        user = self.request.user
        cache_key = f"tasks_user_{user.id}"
        tasks = cache.get(cache_key)

        if tasks is None:
            if user.is_superuser:
                tasks = Task.objects.all()
            else:
                tasks = Task.objects.filter(assigned_to=user)
                
            cache.set(cache_key, tasks, timeout=300)

        return tasks
    
    def perform_update(self, serializer):
        task = serializer.save()
        cache.delete(f"tasks_user_{task.assigned_to.id}")
        
    def perform_destroy(self, instance):
        cache.delete(f"tasks_user_{instance.assigned_to.id}")
        instance.delete()
