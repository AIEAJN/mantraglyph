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
    last_login = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    is_deleted = models.BooleanField(default=True)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True, auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = "user"


class Language(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=225, unique=True)
    abbreviation = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="added_by",
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="updated_by",
        related_name="langage_updated_by",
        blank=True,
        null=True,
    )
    metadata = models.JSONField(blank=True, null=True)
    is_deleted = models.BooleanField(default=True)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = "language"


class Mantraglyph(models.Model):
    id = models.BigAutoField(primary_key=True)
    mantra = models.URLField(blank=True, null=True, default=None)
    image = models.URLField(blank=True, null=True, default=None)
    target_langage = models.ForeignKey(
        Language,
        models.DO_NOTHING,
        db_column="target_langage",
        related_name="target_langage",
        blank=True, null=True,
    )
    detected_langage = models.ForeignKey(
        Language,
        models.DO_NOTHING,
        db_column="detected_langage",
        related_name="detected_langage",
        blank=True, null=True,
    )
    added_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="added_by",
        blank=True, null=True,
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="updated_by",
        related_name="mantraglyph_updated_by",
        blank=True, null=True,
    )
    metadata = models.JSONField(blank=True, null=True)
    is_deleted = models.BooleanField(default=True)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = "mantraglyph"
