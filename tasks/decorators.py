from functools import wraps
from django.core.mail import send_mail

def log_task_action(func):
    @wraps(func)
    def wrapper(self, request):
        if request.user.is_authenticated:
            print(f"[TASK LOG] Action by user {request.user.id}")
    
        return func(self, request)
    return wrapper

def send_task_email(func):
    @wraps(func)
    def wrapper(self, serializer):
        task = func(self, serializer)
        
        send_mail(
            subject = f'New Task Assigned: {task.title}',
            message=task.description,
            from_email='vishupatel13297@gmail.com',
            recipient_list=[task.assigned_to.email],
        )
        return task
    return wrapper
