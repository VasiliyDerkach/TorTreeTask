"""
    модуль views.py
    Содержит представления для реализаии проекта TorTaskTree

    VCreateTask(request) - функция представления, вызывающая форму Django (class CreateTask),
    для создания новой записи задачи (Tasks).
    Передает в таблицу Tasks поля Текст задачи (title), Дата начала выполнения задачи Start,
    Дата завершения задачи End.

    VCreateContact(request) - функция, вызывающая форму Django (class CreateContact), для создания новой
    записи в таблице Контакты (Contacts).
    Передает в таблицу Contacts поля Фамилия - last_name, Имя - first_name, Отчество - second_name.

    MainPage(request) - функция, вызывающая html шаблон, для главной страницы проекта.
    Страница вызывает список задач, рядом с заголовком задачи реализованы кнопки для удаления и редактирования задачи.
    Также реализованы кнопки связывания задачи с другими задачами и кнопка связывания задачи с контактами.
    Заголовки задач реализованы в виде ссылок на карточку для редактирования конкретной задачи.
    Страница содержит поиск задачи по введенному пользователем контексту.

    PageContacts(request) - функция, вызывающая html шаблон, для страницы со списком контактов (Contacts).
    Страница содержит поиск контакта по введенной пользователем фамилии, кнопку для создания новгго контакта.
    Реализованы кнопка удаления выбранного контакта. ФИО контакта реализованы, как ссылки на страницу
    редактирования данных выборанного контакта.

    VCardContact(request, contact_id) - функция, вызывающая html шаблон, для страницы редактирования данных конаткта.
    Атрибут contact_id - значение ключевого поля id таблицы контактов.

    VEditTask(request, task_id)  - функция, вызывающая html шаблон, для страницы редактирования данных задачи.
    Редактирование связей задач между собой и с контактами осуществляется в других функциях.
    Атрибут task_id - значение ключевого поля id таблицы задач.

    VCardTask(request, task_id) - функция, вызывающая html шаблон, для страницы редактирования
    данных о взаимсвязях задач между собой.
    Атрибут task_id - значение ключевого поля id таблицы задач.
    Страница содержит список связанных с данной задачей других задач той же таблицы.
    Это аналог исходящих стрелок связи задач, от выбранной к указанным в списке.
    Рядом с заголовком связанной задачи реализована кнопка удаления связи задач из таблицы связей Univers_list.
    Страница содержит список задач, несвязанных с выбранной задачей. При этом исключается повторное связывание
    двух задач однонаправленной связью. В списке отсутствует выбранная задача, т.к. исключено связывание задачи
    самой с собой.
    Напротив заголовка каждой несвязанной задачи реализована кнопка добавления связи задач, через добавление
    соответствующей записи в таблицу Univers_list.
    Реализованы поиски связанной задачи по контексту в ее загаловке и аналогично по списку несвязанных задач.

    VContactsTask(request, task_id) - функция, вызывающая html шаблон, для страницы редактирования
    данных о взаимсвязях задачи с контактами, а также ролевым значение этой взаимосвязи.
    Атрибут task_id - значение ключевого поля id таблицы задач.
    Страница содержит список связанных с данной задачей контактов и ролей взаимосвязи.
    Это аналог исходящих стрелок связи задач, от выбранной к указанным в списке конатктам.
    Рядом с заголовком связанного контакта  реализована кнопка удаления связи задачи и контакта
    из таблицы связей Univers_list.
    Там же реализован выпадающий список ролей взаимосвязи задачи и контакта (исполнитель, руководитель и т.п.) для
    выбора роли для данной взаимосвязи. Рядом с данным выпадающим списком реализована кнопка сохранения данных о роли
    в поле Role таблицы Univers_list.
    Страница содержит список всех контактов. При этом не исключается повторное связывание
    задач и контакта.

    Напротив заголовка каждого несвязанного с задачей контакта  реализована кнопка добавления связи задачи и контакта,
    через добавление соответствующей записи в таблицу Univers_list.
    Реализованы поиски связанных контактов задачи по контексту фамилии в ее загаловке
    и аналогично по списку несвязанных контактов.

"""

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datetime_safe import datetime

from .forms import *
from .models import *
from django.shortcuts import render
from tortoise import Tortoise
from tortoise.functions import Max
from .db import db_init
import asyncio

asyncio.run(db_init())
"""
    VCreateTask(request) - функция представления, вызывающая форму Django (class CreateTask),
    для создания новой записи задачи (Tasks).
    Передает в таблицу Tasks поля Текст задачи (title), Дата начала выполнения задачи Start,
    Дата завершения задачи End.
"""
async def VCreateTask(request):

    if request.method == 'POST':
        form = CreateTask(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            task_start = form.cleaned_data['start']
            task_end = form.cleaned_data['end']
            await Tasks.create(title=title, start=task_start, end=task_end)
    else:
        form = CreateTask()
    await Tortoise.close_connections()
    cont_form={'form': form}
    return render(request, 'create_contact.html',context=cont_form)

"""
    VCreateContact(request) - функция, вызывающая форму Django (class CreateContact), для создания новой
    записи в таблице Контакты (Contacts).
    Передает в таблицу Contacts поля Фамилия - last_name, Имя - first_name, Отчество - second_name.
"""
async def VCreateContact(request):

    if request.method == 'POST':
        form = CreateContact(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            second_name = form.cleaned_data['second_name']
            await Contacts.create(last_name=last_name,first_name=first_name,second_name=second_name)
    else:
        form = CreateContact()
    cont_form={'form': form}
    await Tortoise.close_connections()
    return render(request, 'create_contact.html',context=cont_form)

"""    
    MainPage(request) - функция, вызывающая html шаблон, для главной страницы проекта.
    Страница вызывает список задач, рядом с заголовком задачи реализованы кнопки для удаления и редактирования задачи.
    Также реализованы кнопки связывания задачи с другими задачами и кнопка связывания задачи с контактами.
    Заголовки задач реализованы в виде ссылок на карточку для редактирования конкретной задачи.
    Страница содержит поиск задачи по введенному пользователем контексту.
"""
async def MainPage(request):
    FindTitle = ''
    if request.method == 'POST':
        if request.POST.get('btn_find')=='new_find':
            FindTitle = request.POST.get('FindTitle')
        id_del = request.POST.get('btn_del')
        # print(id_del)
        if id_del:
            DTsk = await Tasks.get_or_none(id=id_del)
            await DTsk.delete()
            DUlst = await Univers_list.filter(id_in=id_del).all()
            for d in DUlst:
                await d.delete()
            DUlst = await Univers_list.filter(id_out=id_del).all()
            for d in DUlst:
                await d.delete()

    tasks_lst = await Tasks.filter(title__icontains=FindTitle).values()
    tasks_lst1 = await Tasks.all()
    count_tasks = len(tasks_lst)
    if count_tasks == 0:
        PageStr = 'Нет задач соответствующих условиям'
    elif count_tasks > 0:
        PageStr = f'Количество задач = {count_tasks}'
    info_main = {'PageTitle': PageStr, 'tasks_list': tasks_lst,
                 'count_tasks': count_tasks, 'FindTitle': FindTitle}
    await Tortoise.close_connections()
    return render(request, 'main.html', context=info_main)

"""
    PageContacts(request) - функция, вызывающая html шаблон, для страницы со списком контактов (Contacts).
    Страница содержит поиск контакта по введенной пользователем фамилии, кнопку для создания новгго контакта.
    Реализованы кнопка удаления выбранного контакта. ФИО контакта реализованы, как ссылки на страницу
    редактирования данных выборанного контакта.
"""
async def PageContacts(request):
    FindTitle = ''
    if request.method == 'POST':
        if request.POST.get('btn_find'):
            FindTitle = request.POST.get('FindTitle')
        id_del = request.POST.get('btn_del')
        # print(id_del)
        if id_del:
            DCnt = await Contacts.get_or_none(id=id_del)
            await DCnt.delete()
            DUlst = await Univers_list.filter(id_in=id_del).all()
            for d in DUlst:
                await d.delete()
            DUlst = await Univers_list.filter(id_out=id_del).all()
            for d in DUlst:
                await d.delete()


    contacts_lst = await Contacts.filter(last_name__icontains=FindTitle).values()
    count_contacts = len(contacts_lst)
    if count_contacts == 0:
        PageStr = 'Нет контактов, соответствующих поиску'
    elif count_contacts > 0:
        PageStr = f'Количество контактов = {count_contacts}'
    info_main = {'PageTitle': PageStr, 'contacts_lst': contacts_lst,
                 'count_contacts': count_contacts, 'FindTitle': FindTitle}
    await Tortoise.close_connections()
    return render(request, 'contacts.html', context=info_main)

"""
    VCardContact(request, contact_id) - функция, вызывающая html шаблон, для страницы редактирования данных конаткта.
    Атрибут contact_id - значение ключевого поля id таблицы контактов.
"""
async def VCardContact(request, contact_id):

    VContact = await Contacts.get_or_none(id=contact_id)
    # print(VContact)
    if request.method == 'POST':
        VContact.last_name = request.POST.get('last_name')
        VContact.first_name = request.POST.get('first_name')
        VContact.second_name = request.POST.get('second_name')
        await VContact.save()
    await Tortoise.close_connections()
    return render(request, 'card_contact.html', context={'contact': VContact})

"""
    VEditTask(request, task_id)  - функция, вызывающая html шаблон, для страницы редактирования данных задачи.
    Редактирование связей задач между собой и с контактами осуществляется в других функциях.
    Атрибут task_id - значение ключевого поля id таблицы задач.
"""
async def VEditTask(request, task_id):

    GTask0 = await Tasks.get(id=task_id)
    print('GTask0=',GTask0)
    GTask = await Tasks.filter(id=task_id).values()
    print('GTask=', GTask)
    # print(FTask)
    if request.method == 'POST':
        # await GTask0.update(title = request.POST.get('task_title'),
        # start = request.POST.get('start'),
        # end = request.POST.get('date_end'))

        GTask0.title = request.POST.get('task_title')
        dates = request.POST.get('start')
        # print('dates=',dates)
        try:
            GTask0.start = dates
        except:
            GTask0.start = None
        if GTask0.start=='':
            GTask0.start = None
        datee = request.POST.get('date_end')
        try:
            GTask0.end = datee
        except:
            GTask0.end = None
        if GTask0.end=='':
            GTask0.end = None
        print('date',GTask0.start,GTask0.end)
        await GTask0.save()
        # print(request.POST.get('task_title'),request.POST.get('start'),request.POST.get('date_end'))
    FTask = GTask[0]
    try:
        FTask['start'] = datetime.date(FTask['start']).strftime('%Y-%m-%d')
    except:
        FTask['start'] = None
        # print('type(FTask["start"])=',type(FTask['start']))
    try:
        FTask['end'] = datetime.date(FTask['end']).strftime('%Y-%m-%d')
    except:
        FTask['end'] = None
    await Tortoise.close_connections()
    return render(request, 'edit_task.html', context={'task': FTask})

"""
    VCardTask(request, task_id) - функция, вызывающая html шаблон, для страницы редактирования
    данных о взаимсвязях задач между собой.
    Атрибут task_id - значение ключевого поля id таблицы задач.
    Страница содержит список связанных с данной задачей других задач той же таблицы.
    Это аналог исходящих стрелок связи задач, от выбранной к указанным в списке.
    Рядом с заголовком связанной задачи реализована кнопка удаления связи задач из таблицы связей Univers_list.
    Страница содержит список задач, несвязанных с выбранной задачей. При этом исключается повторное связывание
    двух задач однонаправленной связью. В списке отсутствует выбранная задача, т.к. исключено связывание задачи
    самой с собой.
    Напротив заголовка каждой несвязанной задачи реализована кнопка добавления связи задач, через добавление
    соответствующей записи в таблицу Univers_list.
    Реализованы поиски связанной задачи по контексту в ее загаловке и аналогично по списку несвязанных задач.
"""
async def VCardTask(request, task_id):
    find_task = await Tasks.filter(id=task_id).values()
    count_link_tasks = 0
    count_unlink_tasks = 0
    FindTitleUnLink = ''
    FindTitle = ''

    if find_task:
        lst_field_task = find_task[0]
        vtask_title = lst_field_task['title']
        vtask_start = lst_field_task['start']
        vtask_end = lst_field_task['end']
        vtask_id = str(lst_field_task['id'])
        link_task = await Univers_list.filter(id_out=vtask_id).values()
        count_fulllink_task = len(link_task)
        if request.method == 'POST':
            btn_find_unlink = request.POST.get('btn_find_unlink')
            if btn_find_unlink:
                FindTitleUnLink = request.POST.get('FindTitleUnlink')
                btn_find_unlink = None
            btn_find_tlink = request.POST.get('btn_find_tsklink')
            if btn_find_tlink:
                FindTitle = request.POST.get('FindTitle')
                btn_find_tlink = None
                # print('FindTitle=',FindTitle)

        if count_fulllink_task>0:
            list_link_task = await Univers_list.filter(id_out=vtask_id).values()
            print('list_link_task=',list_link_task)
            lst_link_idin = [str(lst['id_in']) for lst in list_link_task]
            # print('lst_link_idin=',lst_link_idin)
            flist_link_task = await Tasks.filter(title__icontains=FindTitle, id__in=lst_link_idin).values()
            # print(flist_link_task)
            notlist_link_task = await Tasks.exclude(id__in=lst_link_idin).exclude(id=vtask_id).filter(title__icontains=FindTitleUnLink).values()
            count_link_tasks = len(flist_link_task)
        else:
            flist_link_task = None
            notlist_link_task = await Tasks.exclude(id=vtask_id).filter(title__icontains=FindTitleUnLink).values()
        count_unlink_tasks = len(notlist_link_task)
        if request.method == 'POST':
            btn_unlink = request.POST.get('btn_unlink')
            if btn_unlink:
                DULst = await Univers_list.get_or_none(id_in=btn_unlink, id_out=vtask_id)
                await DULst.delete()
                btn_unlink = None
            btn_link = request.POST.get('btn_link')
            if btn_link:
                # print(btn_link,vtask_id)
                lu = await Univers_list.filter(id_in=btn_link, id_out=vtask_id, role='arrow').values()
                if lu:
                    return HttpResponse("Задачи уже связаны")
                else:
                    max_indx = await Univers_list.filter(id_out=vtask_id, role='arrow').annotate(max_s=max("num_in_link")).values('max_s')
                    max_indx_int = max_indx[0]['max_s']

                    # print(max_indx)
                    if not max_indx_int:
                        max_indx_int = 0
                    max_indx_int += 1
                    # print(max_indx)
                    await Univers_list.create(id_in=btn_link, id_out=vtask_id, num_in_link=max_indx_int, role='arrow')
                btn_link =None
    else:
        return HttpResponse("Задача не найдена")

    info_task = {'task_id': vtask_id, 'task_title': vtask_title, 'task_start':vtask_start,
                'task_end': vtask_end,'list_link_task': flist_link_task,
                 'notlist_link_task': notlist_link_task, 'FindTitleUnLink': FindTitleUnLink,
                 'FindTitle': FindTitle,
                 'count_link_tasks': count_link_tasks,'count_unlink_tasks': count_unlink_tasks}
    await Tortoise.close_connections()
    return render(request,'card_task.html',context=info_task)

"""
    VContactsTask(request, task_id) - функция, вызывающая html шаблон, для страницы редактирования
    данных о взаимсвязях задачи с контактами, а также ролевым значение этой взаимосвязи.
    Атрибут task_id - значение ключевого поля id таблицы задач.
    Страница содержит список связанных с данной задачей контактов и ролей взаимосвязи.
    Это аналог исходящих стрелок связи задач, от выбранной к указанным в списке конатктам.
    Рядом с заголовком связанного контакта  реализована кнопка удаления связи задачи и контакта
    из таблицы связей Univers_list.
    Там же реализован выпадающий список ролей взаимосвязи задачи и контакта (исполнитель, руководитель и т.п.) для
    выбора роли для данной взаимосвязи. Рядом с данным выпадающим списком реализована кнопка сохранения данных о роли
    в поле Role таблицы Univers_list.
    Страница содержит список всех контактов. При этом не исключается повторное связывание
    задач и контакта.

    Напротив заголовка каждого несвязанного с задачей контакта  реализована кнопка добавления связи задачи и контакта,
    через добавление соответствующей записи в таблицу Univers_list.
    Реализованы поиски связанных контактов задачи по контексту фамилии в ее загаловке
    и аналогично по списку несвязанных контактов.

"""
async def VContactsTask(request, task_id):
    find_task = await Tasks.filter(id=task_id).values()
    count_link_tasks = 0
    count_unlink_tasks = 0
    FindTitleUnLink = ''
    FindTitle = ''
    lst_contacts_rol = []
    if find_task:
        lst_field_task = find_task[0]
        vtask_title = lst_field_task['title']
        vtask_start = lst_field_task['start']
        vtask_end = lst_field_task['end']
        vtask_id = str(lst_field_task['id'])
        link_task = await Univers_list.filter(id_out=vtask_id).values()
        count_fulllink_task = len(link_task)
        if request.method == 'POST':
            btn_find_unlink = request.POST.get('btn_find_unlink')
            if btn_find_unlink:
                FindTitleUnLink = request.POST.get('FindTitleUnlink')
                btn_find_unlink = None
            btn_find_tlink = request.POST.get('btn_find_tsklink')
            if btn_find_tlink:
                FindTitle = request.POST.get('FindTitle')
                btn_find_tlink = None
                # print('FindTitle=',FindTitle)

        if count_fulllink_task>0:
            list_link_task = await Univers_list.filter(id_out=vtask_id).values()
            lst_link_idin = [lst['id_in'] for lst in list_link_task]
            # print('lst_link_idin=',lst_link_idin)
            flist_link_task = await Contacts.filter(last_name__icontains=FindTitle, id__in=lst_link_idin).values()
            # print(flist_link_task)
            count_link_tasks = len(flist_link_task)

            for idin in list_link_task:
                cnt = await Contacts.filter(id=idin['id_in']).values()
                if cnt:
                    elem = idin
                    elem['list_id'] = idin['id']
                    fio = cnt[0]
                    elem = {**elem, **fio}
                    lst_contacts_rol.append(elem)

        else:
            flist_link_task = None
        notlist_link_task = await Contacts.filter(last_name__icontains=FindTitleUnLink).values()
        count_unlink_tasks = len(notlist_link_task)
        if request.method == 'POST':
            btn_unlink = request.POST.get('btn_unlink')
            if btn_unlink:
                DULst = await Univers_list.get_or_none(id=btn_unlink)
                await DULst.delete()
                btn_unlink = None
            btn_link = request.POST.get('btn_link')
            btn_role = request.POST.get('btn_role')
            if btn_role:
                vrole = request.POST.get(f"contact_role>{btn_role}")
                # print(vrole)
                UUlst = await Univers_list.get_or_none(id=btn_role)
                # print(UUlst.id)
                UUlst.role=vrole
                await UUlst.save()
                btn_role = None
                # await UUlst.update(role=vrole)
            else:
                vrole = ''

            if btn_link:
                    await Univers_list.create(id_in=btn_link, id_out=vtask_id, num_in_link=0, role=vrole)
                    btn_link = None
    else:
        await Tortoise.close_connections()
        return HttpResponse("Задача не найдена")

    info_task = {'task_id': vtask_id, 'task_title': vtask_title, 'task_start':vtask_start,
                'task_end': vtask_end,'list_link_task': lst_contacts_rol,
                 'notlist_link_task': notlist_link_task, 'FindTitleUnLink': FindTitleUnLink,
                 'FindTitle': FindTitle,
                 'count_link_tasks': count_link_tasks,'count_unlink_tasks': count_unlink_tasks}
    await Tortoise.close_connections()
    return render(request,'task_contacts.html',context=info_task)

# if __name__=='__main__':
#     asyncio.run(db_init())
