from django.contrib.auth.decorators import permission_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.urls import reverse
from ..forms import CustomAuthenticationForm
from ..models import Medicine, Prescription, Order, LegalEntity, PhysicalPerson, Doctor, MedicalFacility, \
    MedicineGroup, Receipt, Certificate, Contract, Supplier, PrescComposition, OrderComposition, ReceiptItem,\
    CertificateAttachment, ContractMedicine
from ..utils import get_default_context, required_presc, get_view_context, get_user_permissions, check_user_rules, \
    get_list_context, get_FIO, get_gender, get_link
from pharmacy.settings import STATIC_URL


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
            context = get_default_context('login')
            custom_context = {'form': form, 'error': error, }
            return render(request, 'mainapp/login.html', context | custom_context)

    # Если пользователь уже авторизован, либо авторизация прошла без ошибок,
    # перенаправляем на главную страницу
    return redirect('index')


@login_required(login_url=login_view)
def index_view(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def reports_list(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


def error_access(request, exception=0):
    context = get_default_context('index', user=request.user)
    custom_context = {
        'fav': STATIC_URL + 'mainapp/other/favicon.jpg',
        'error': STATIC_URL + 'mainapp/css/error.css',
        'common': STATIC_URL + 'mainapp/css/common.css',
        'def': STATIC_URL + 'mainapp/css/default.css',
        'smile': STATIC_URL + 'mainapp/svg/smile.svg',
        'bg': STATIC_URL + 'mainapp/other/bg.jpg',
    }
    return render(request, '404.html', context | custom_context, status=404)