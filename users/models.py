from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="user"
    )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = "admin"
        else:
            self.role = "user"
            
        super().save(*args, **kwargs)
