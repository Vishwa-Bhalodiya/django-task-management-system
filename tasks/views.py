from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsAdminForCreate
from .decorators import log_task_action, send_task_email

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminForCreate]
    queryset = Task.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['assigned_to', 'status']

    @log_task_action
    def create(self, request):
        return super().create(request)
    
    def perform_create(self, serializer):
        task = serializer.save()
        #Clear cache for assigned user
        cache.delete(f"tasks_user_{task.assigned_to.id}")
        cache.delete(f"tasks_user_{self.request.user.id}") #admin
        
        send_task_email(task)
        return task

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
    
    @log_task_action
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        task = serializer.save()
        cache.delete(f"tasks_user_{task.assigned_to.id}")
        return task
    
        
    def perform_destroy(self, instance):
        cache.delete(f"tasks_user_{instance.assigned_to.id}")
        instance.delete()
