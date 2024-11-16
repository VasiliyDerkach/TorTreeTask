from django import forms
class CreateContact(forms.Form):
    last_name = forms.CharField(max_length=75, label='Введите фамилию')
    first_name = forms.CharField(max_length=75,label='Введите имя')
    second_name = forms.CharField(max_length=75, label='Введите отяество')

class CreateTask(forms.Form):
    title = forms.CharField(max_length=250, label='Введите текст задачи')
    start = forms.DateField(label='Введите дату старта', required=False)
    end = forms.DateField(label='Введите дату завершения',  required=False)