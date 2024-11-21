"""
    Модуль models.py
    Задает модель таблицы Tasks
    поля Текст задачи (title),
    Дата начала выполнения задачи Start,
    Дата завершения задачи End.
    ключевое поле id - 36 значная строка формата uuid

    Модель таблицы Контакты (Contacts).
    поля Фамилия - last_name, Имя - first_name, Отчество - second_name.
    ключевое поле id - 36 значная строка формата uuid

    Модель таблицы Univers_list
    для связывание задач между собой и контактами.
    созаваемое автоматически целочисленное поле id - ключевое поле для определения уникального указателя на запись таблицы,
    используемое для удаления и редактирования данных талицы.
    id_out - текстовое поле для хранения указателя на id задачи (в формате uuid), от которой исходит взаимсвязь
     с другой задачей или с констактом (исходящая стрелка).
    id_in - текстовое поле для хранения указателя на id задачи или контакта (в формате uuid), в которую входит взаимсвязь
     с другой задачей (входящая стрелка).
     Role - текстовое поле для хранения данных о характере взаимосвязи задачи и контакта (исполнитель, контролер и т.п.).
     Для взаимосвязи задач значение по умолчанию 'arrow'.
     num_in_link - целочисленное поле для автоматической нумерации записей таблицы взаимсвязей для задачи с id=id_out
     (нумерация исходящих стрелок для одной задачи).
     Для взаимсвязи задач и конктактов   num_in_link=0
     Поле предназначено для расшрения функционала приложения в будущем. Например, сложный алгоритм определния актуальности
     задачи по входящим в нее нумерованным стрелкам по типу Arrow[1] and (Arrow[2] or Arrow[3])
"""
import uuid
# from django.db import models
from tortoise import fields
from tortoise.models import Model
from .db import db_init
# Create your models here.
class Tasks(Model):
    """
    class Tasks(Model):
        Задает модель таблицы Tasks
        поля Текст задачи (title),
        Дата начала выполнения задачи Start,
        Дата завершения задачи End.
        ключевое поле id - 36 значная строка формата uuid
    """
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = fields.CharField(max_length=250)
    start = fields.DateField(null=True)
    end = fields.DateField(null=True)
    class Meta:
        table = "tasks"

class Univers_list(Model):
    """
    class Univers_list(Model):
        Модель таблицы Univers_list
        для связывание задач между собой и контактами.
        созаваемое автоматически целочисленное поле id - ключевое поле для определения уникального указателя на запись таблицы,
        используемое для удаления и редактирования данных талицы.
        id_out - текстовое поле для хранения указателя на id задачи (в формате uuid), от которой исходит взаимсвязь
         с другой задачей или с констактом (исходящая стрелка).
        id_in - текстовое поле для хранения указателя на id задачи или контакта (в формате uuid), в которую входит взаимсвязь
         с другой задачей (входящая стрелка).
         Role - текстовое поле для хранения данных о характере взаимосвязи задачи и контакта (исполнитель, контролер и т.п.).
         Для взаимосвязи задач значение по умолчанию 'arrow'.
         num_in_link - целочисленное поле для автоматической нумерации записей таблицы взаимсвязей для задачи с id=id_out
         (нумерация исходящих стрелок для одной задачи).
         Для взаимсвязи задач и конктактов   num_in_link=0
         Поле предназначено для расшрения функционала приложения в будущем. Например, сложный алгоритм определния актуальности
         задачи по входящим в нее нумерованным стрелкам по типу Arrow[1] and (Arrow[2] or Arrow[3])
    """
    id = fields.IntField(primary_key=True)
    id_out = fields.CharField(max_length=36, blank=False)
    id_in = fields.CharField(max_length=36, blank=False)
    num_in_link = fields.IntField()
    role = fields.CharField(max_length=75)
    class Meta:
        table = "Univers_list"
class Contacts(Model):
    """
    class Contacts(Model):
        Модель таблицы Контакты (Contacts).
        поля Фамилия - last_name, Имя - first_name, Отчество - second_name.
        ключевое поле id - 36 значная строка формата uuid
    """
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name = fields.CharField(max_length=100)
    first_name = fields.CharField(max_length=100)
    second_name = fields.CharField(max_length=100)
    class Meta:
        table = "Contacts"