from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user", "User"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def is_admin(self):
        return self.role == "admin"

    def __str__(self):
        return self.email
