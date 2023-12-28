from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CustomAuthenticationForm
from .models import Medicine
from .utils import get_default_context, required_presc


def login_view(request):
    # Обрабатываем представление только для неавторизованных пользователей
    if not request.user.is_authenticated:
        load_view = False
        error = ''
        # Отправка данных авторизации
        if request.method == 'POST':
            form = CustomAuthenticationForm(data=request.POST, remember=request.POST.get('remember'))
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                if form.remember:
                    request.session.set_expiry(
                        2592000)  # устанавливаем срок действия сессии на 30 дней (в секундах)
            # Отправленные данные некорректны
            else:
                load_view = True
                error = 'Введенные данные некорректны!'
        # Переход на страницу авторизации
        else:
            load_view = True
            form = CustomAuthenticationForm()
        if load_view:
            context = get_default_context(punkt_selected='login')
            custom_context = {'form': form, 'error': error, }
            return render(request, 'mainapp/login.html', context | custom_context)

    # Если пользователь уже авторизован, либо авторизация прошла без ошибок,
    # перенаправляем на главную страницу
    return redirect('index')


@login_required(login_url=login_view)
def index_view(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def prescription_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def order_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def legal_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def physic_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def doctor_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def facility_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def receipt_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def certificate_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def contract_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def supplier_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def medicine_id(request, record):
    context = get_default_context(bread_crumbs=True, punkt_selected='medicine', user=request.user)
    custom_context = {
        'edit_link': reverse('medicine_edit', args=[record])
    }
    return render(request, 'mainapp/view.html', context | custom_context)


@login_required
def med_group_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/view.html', context | custom_context)


@login_required
def prescription_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def order_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def legal_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def physic_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def doctor_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def facility_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def receipt_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def certificate_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def contract_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def supplier_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def medicine_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def med_group_edit(request):

    if request.resolver_match.view_name == 'med_group_new':
        pass
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/simple_view_edit.html', context | custom_context)


@login_required
def prescription_list(request):
    # Номер, Клиент, Лекарство, Врач, Статус
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'prescription_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def order_list(request):
    # Номер, Дата, Клиент физ., Клиент юр., Продавец
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'order_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def legal_list(request):
    # Название, Адрес, ИНН, КПП
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'legal_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def physic_list(request):
    # ФИО, Город, Адрес, Дата рождения
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'physic_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def doctor_list(request):
    # ФИО, Учреждение, Специализация, Должность
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'doctor_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def facility_list(request):
    # Название, Город, Адрес
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'facility_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def med_group_list(request):
    # Наименование
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'med_group_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def receipt_list(request):
    # Договор, дата
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'receipt_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def certificate_list(request):
    # Номер, Лекарство, Поставщик, Дата начала
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'certificate_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def contract_list(request):
    # Номер, Поставщик, Дата начала
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'contract_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def supplier_list(request):
    # Наименование, Город, Адрес
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {
        'add_record': 'supplier_new',
        'link_table': reverse('prescription_id'),
        'desc_table': ['', '', ''],
    }
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def medicine_list(request):
    # Артикул, Наименование, Фарм.группа, Требует рецепта
    records = []
    if request.method == "POST":
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            records = Medicine.objects.all()
            # ...
            records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = Medicine.objects.all()
    context = get_default_context(punkt_selected='medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [{'link': reverse('medicine_id', args=[x.id]), 'id': x.id, 'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]} for x in records],
        'filters': [
            [{'title': "Поиск по названию", 'name': 'f-name', 'type': 'text'}, ],
            [{'title': "Поиск по артиклу", 'name': 'f-article', 'type': 'text'}, ],
            [{'title': "Группы", 'name': 'f-group', 'type': 'number'}, ],
            [{'title': "Обязательность рецепта", 'name': 'f-pre_required', 'type': 'checkbox'}, ],
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)


@login_required
def reports_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def error_access(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)
