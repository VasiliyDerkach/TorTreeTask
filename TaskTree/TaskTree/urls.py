"""
Модуль urls.py для обработки URL приложения TaskTreeApp
Назначение URL для представлений:
- addtask/ - добавление новой задачи в таблицу Tasks,
- addcontact/ -добавление нового контакта в таблицу Contacts,
- card_task/ - страница редактирования связей задачи с Tasks.id=task_id с другими задачами,
- edit_task/ - редактирование полей задачи с Tasks.id=task_id,
- '' - главная страница со списком задач из таблицы Tasks и операций с задачами,
- contacts/ - страница со списком контактов из таблицы Contacts и операций с контактами,
- task_contacts/ - страница редактирования связей задачи с Tasks.id=task_id с контактами,
- contacts/card_contact/ - страница редактирования полей контакта с Contacts.id=contact_id.
"""
from django.contrib import admin
from django.urls import path
from TaskTreeApp.views import *
from TaskTreeApp.forms import *
urlpatterns = [
    path('admin/', admin.site.urls),
#- '' - главная страница со списком задач из таблицы Tasks и операций с задачами,
    path('',MainPage),
#- addtask/ - добавление новой задачи в таблицу Tasks,
    path('addtask/',VCreateTask, name='addtask'),
#- addcontact/ -добавление нового контакта в таблицу Contacts,
    path('addcontact/',VCreateContact, name='addcontact'),
#- card_task/ - страница редактирования связей задачи с Tasks.id=task_id с другими задачами,
    path('card_task/<slug:task_id>/',VCardTask, name='card_task'),
#- edit_task/ - редактирование полей задачи с Tasks.id=task_id,
    path('edit_task/<slug:task_id>/',VEditTask, name='edit_task'),
#- contacts/ - страница со списком контактов из таблицы Contacts и операций с контактами,
    path('contacts/',PageContacts, name='contacts'),
#- task_contacts/ - страница редактирования связей задачи с Tasks.id=task_id с контактами,
    path('task_contacts/<slug:task_id>/',VContactsTask,name='task_contacts'),
#- contacts/card_contact/ - страница редактирования полей контакта с Contacts.id=contact_id.
    path('contacts/card_contact/<slug:contact_id>/',VCardContact, name='card_contact'),

]
