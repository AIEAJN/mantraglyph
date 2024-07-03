from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True)
    username = models.CharField(unique=True, max_length=32)
    password = models.CharField(max_length=128, null=True)
    email = models.CharField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_admin = models.BooleanField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = "user"