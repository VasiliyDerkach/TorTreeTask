from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from .models import *
from django.shortcuts import render
from tortoise import Tortoise, fields, models, run_async
from .db import db_init

import asyncio

asyncio.run(db_init())


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
# Create your views here.
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
async def MainPage(request):
    FindTitle = ''
    if request.method == 'POST':
        if request.POST.get('btn_find')=='new_find':
            FindTitle = request.POST.get('FindTitle')
        id_del = request.POST.get('btn_del')
        # print(id_del)
        if id_del:
            await Tasks.get(id=id_del).delete()

    tasks_lst = await Tasks.filter(title__icontains=FindTitle)
    print('tasks_lst=',tasks_lst)
    count_tasks = tasks_lst.count('id')
    print(tasks_lst,count_tasks)

    if count_tasks == 0:
        PageStr = 'Нет задач соответствующих условиям'
    elif count_tasks > 0:
        PageStr = f'Количество задач = {count_tasks}'
    info_main = {'PageTitle': PageStr, 'tasks_list': tasks_lst,
                 'count_tasks': count_tasks, 'FindTitle': FindTitle}
    await Tortoise.close_connections()
    return render(request, 'main.html', context=info_main)
async def PageContacts(request):
    FindTitle = ''
    if request.method == 'POST':
        if request.POST.get('btn_find'):
            FindTitle = request.POST.get('FindTitle')
        id_del = request.POST.get('btn_del')
        # print(id_del)
        if id_del:
            await Contacts.get(id=id_del).delete()

    contacts_lst = await Contacts.filter(last_name__icontains=FindTitle)
    count_contacts = contacts_lst.count('id')
    if count_contacts == 0:
        PageStr = 'Нет контактов, соответствующих поиску'
    elif count_contacts > 0:
        PageStr = f'Количество контактов = {count_contacts}'
    info_main = {'PageTitle': PageStr, 'contacts_lst': contacts_lst,
                 'count_contacts': count_contacts, 'FindTitle': FindTitle}
    await Tortoise.close_connections()
    return render(request, 'contacts.html', context=info_main)
async def VCardContact(request, contact_id):

    VContact = await Contacts.get(id=contact_id)
    # print(VContact)
    if request.method == 'POST':
        VContact.last_name = request.POST.get('last_name')
        VContact.first_name = request.POST.get('first_name')
        VContact.second_name = request.POST.get('second_name')
        await VContact.save()
    await Tortoise.close_connections()
    return render(request, 'card_contact.html', context={'contact': VContact})

async def VEditTask(request, task_id):

    GTask = await Tasks.filter(id=task_id))
    # print(FTask)
    if request.method == 'POST':
        await GTask.update(title = request.POST.get('task_title'),
        start = request.POST.get('start'),
        end = request.POST.get('date_end'))
        # print(request.POST.get('task_title'),request.POST.get('start'),request.POST.get('date_end'))
    FTask = GTask[0]
    FTask['start'] = FTask['start'].strftime('%Y-%m-%d')
    FTask['end'] = FTask['end'].strftime('%Y-%m-%d')
    await Tortoise.close_connections()
    return render(request, 'edit_task.html', context={'task': FTask})

async def VCardTask(request, task_id):
    find_task = await Tasks.filter(id=task_id)
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
        link_task = await Univers_list.filter(id_out=vtask_id)
        count_fulllink_task = link_task.count('id')
        if request.method == 'POST':
            btn_find_unlink = request.POST.get('btn_find_unlink')
            if btn_find_unlink:
                FindTitleUnLink = request.POST.get('FindTitleUnlink')
            btn_find_tlink = request.POST.get('btn_find_tsklink')
            if btn_find_tlink:
                FindTitle = request.POST.get('FindTitle')
                # print('FindTitle=',FindTitle)

        if count_fulllink_task>0:
            list_link_task = await Univers_list.filter(id_out=vtask_id)
            lst_link_idin = [str(lst.id_in) for lst in list_link_task]
            # print('lst_link_idin=',lst_link_idin)
            flist_link_task = await Tasks.filter(title__icontains=FindTitle, id__in=lst_link_idin)
            # print(flist_link_task)
            notlist_link_task = await Tasks.exclude(id__in=lst_link_idin).exclude(id=vtask_id).filter(title__icontains=FindTitleUnLink)
            count_link_tasks = flist_link_task.count()
        else:
            flist_link_task = None
            notlist_link_task = await Tasks.exclude(id=vtask_id).filter(title__icontains=FindTitleUnLink)
        count_unlink_tasks = notlist_link_task.count('id')
        if request.method == 'POST':
            btn_unlink = request.POST.get('btn_unlink')
            if btn_unlink:
                await Univers_list.filter(id_in=btn_unlink,id_out=vtask_id).delete()
            btn_link = request.POST.get('btn_link')
            if btn_link:
                # print(btn_link,vtask_id)
                lu = await Univers_list.filter(id_in=btn_link, id_out=vtask_id, role='arrow')
                if lu:
                    return HttpResponse("Задачи уже связаны")
                else:
                    max_indx = await Univers_list.filter(id_out=vtask_id, role='arrow').aggregate(Max('num_in_link'))
                    max_indx_int = max_indx['num_in_link__max']
                    if not max_indx_int:
                        max_indx_int = 0
                    max_indx_int += 1
                    # print(max_indx)
                    await Univers_list.create(id_in=btn_link, id_out=vtask_id, num_in_link=max_indx_int, role='arrow')
    else:
        return HttpResponse("Задача не найдена")

    info_task = {'task_id': vtask_id, 'task_title': vtask_title, 'task_start':vtask_start,
                'task_end': vtask_end,'list_link_task': flist_link_task,
                 'notlist_link_task': notlist_link_task, 'FindTitleUnLink': FindTitleUnLink,
                 'FindTitle': FindTitle,
                 'count_link_tasks': count_link_tasks,'count_unlink_tasks': count_unlink_tasks}
    await Tortoise.close_connections()
    return render(request,'card_task.html',context=info_task)
async def VContactsTask(request, task_id):
    find_task = await Tasks.filter(id=task_id)
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
        link_task = await Univers_list.filter(id_out=vtask_id)
        count_fulllink_task = link_task.count('id')
        if request.method == 'POST':
            btn_find_unlink = request.POST.get('btn_find_unlink')
            if btn_find_unlink:
                FindTitleUnLink = request.POST.get('FindTitleUnlink')
            btn_find_tlink = request.POST.get('btn_find_tsklink')
            if btn_find_tlink:
                FindTitle = request.POST.get('FindTitle')
                # print('FindTitle=',FindTitle)

        if count_fulllink_task>0:
            list_link_task = await Univers_list.filter(id_out=vtask_id)
            lst_link_idin = [str(lst.id_in) for lst in list_link_task]
            # print('lst_link_idin=',lst_link_idin)
            flist_link_task = await Contacts.filter(last_name__icontains=FindTitle, id__in=lst_link_idin)
            # print(flist_link_task)
            count_link_tasks = flist_link_task.count('id')

            for idin in list_link_task:
                cnt = await Contacts.filter(id=idin['id_in'])
                if cnt:
                    elem = idin
                    elem['list_id'] = idin['id']
                    fio = cnt[0]
                    elem = {**elem, **fio}
                    lst_contacts_rol.append(elem)

        else:
            flist_link_task = None
        notlist_link_task = await Contacts.filter(last_name__icontains=FindTitleUnLink)
        count_unlink_tasks = notlist_link_task.count('id')
        if request.method == 'POST':
            btn_unlink = request.POST.get('btn_unlink')
            if btn_unlink:
                await Univers_list.filter(id=btn_unlink).delete()
            btn_link = request.POST.get('btn_link')
            btn_role = request.POST.get('btn_role')
            if btn_role:
                # print(vrole)
                vrole = request.POST.get(f"contact_role>{btn_role}")
                await Univers_list.filter(id=btn_role).update(role=vrole)
            else:
                vrole = ''

            if btn_link:
                    await Univers_list.create(id_in=btn_link, id_out=vtask_id, num_in_link=0, role=vrole)
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
