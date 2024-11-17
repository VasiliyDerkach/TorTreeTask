"""
 Модуль forms.py
 class CreateContact - форма для создания нового контакта
    last_name -фамилия (обязательное поле)
    first_name - имя
    second_name - отяество
class CreateTask - форма для создания новой задачи
    title -  текст заголовка задачи (обязательное поле)
    start - дата старта задачи
    end - дата завершения задачи
"""

from django import forms
class CreateContact(forms.Form):
    last_name = forms.CharField(max_length=75, label='Введите фамилию')
    first_name = forms.CharField(max_length=75,label='Введите имя')
    second_name = forms.CharField(max_length=75, label='Введите отяество')

class CreateTask(forms.Form):
    title = forms.CharField(max_length=250, label='Введите текст задачи')
    start = forms.DateField(label='Введите дату старта', required=False)
    end = forms.DateField(label='Введите дату завершения',  required=False)