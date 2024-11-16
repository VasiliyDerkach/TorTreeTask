import uuid
# from django.db import models
from tortoise import Tortoise, fields, models, run_async
from .db import db_init
# Create your models here.
class Tasks(models.Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = fields.CharField(max_length=250)
    start = fields.DateField(null=True)
    end = fields.DateField(null=True)
    class Meta:
        table = "tasks"
class Univers_list(models.Model):
    id = fields.IntField(primary_key=True)
    id_out = fields.CharField(max_length=36, blank=False)
    id_in = fields.CharField(max_length=36, blank=False)
    num_in_link = fields.IntField()
    role = fields.CharField(max_length=75)
    class Meta:
        table = "Univers_list"
class Contacts(models.Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name = fields.CharField(max_length=100)
    first_name = fields.CharField(max_length=100)
    second_name = fields.CharField(max_length=100)
    class Meta:
        table = "Contacts"