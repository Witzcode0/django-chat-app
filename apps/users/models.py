from django.db import models
from apps.master.models import BaseModel

# Create your models here.
class chatUser(BaseModel):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=255, blank=False, null=False, unique=True)
    bio = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255,blank=False, null=False)
    is_active = models.BooleanField(default=True)
