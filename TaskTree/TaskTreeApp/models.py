import uuid
from django.db import models

# Create your models here.
class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    start = models.DateField(null=True)
    end = models.DateField(null=True)
class Univers_list(models.Model):
    id_out = models.CharField(max_length=36, blank=False)
    id_in = models.CharField(max_length=36, blank=False)
    num_in_link = models.IntegerField()
    role = models.CharField(max_length=75)

class Contacts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)