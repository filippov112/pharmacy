from django.db import IntegrityError
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import login
from django.db import DataError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.urls import reverse
from ..forms import CustomAuthenticationForm
from ..models import *
from ..functions.main import *
from pharmacy.settings import STATIC_URL


def login_view(request):
    error = ''
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, remember=request.POST.get('remember'))
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if form.remember:
                request.session.set_expiry(2592000)
            return redirect('index')
        else:
            error = 'Введенные данные некорректны!'
    else:
        form = CustomAuthenticationForm()

    context = get_default_context('login', title='Авторизация')
    custom_context = {'form': form, 'error': error, }
    return render(request, 'mainapp/login.html', context | custom_context)


@login_required(login_url=login_view)
def index_view(request):
    error = ''
    context = get_default_context('index', request.user, 'Заглавная', error)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def reports_list(request):
    error = ''
    context = get_default_context('reports', request.user, 'Отчетные формы', error)
    custom_context = {
        'title_view': 'Отчетные формы',
        'reports': [
            {
                'report': 0,
                'title': 'Отчет по продажам за период',
                'date_block': False,
                'period_block': True,
                'links': []
            },
            {
                'report': 1,
                'title': 'Отчет по доступным запасам лекарства',
                'date_block': False,
                'period_block': False,
                'links': [
                    {'title': 'Препарат', 'table': 's-medicine', 'name': 'medicine'},
                ]
            },
            {
                'report': 2,
                'title': 'Отчет по списанию просроченных препаратов',
                'date_block': True,
                'period_block': False,
                'links': []
            },
            {
                'report': 3,
                'title': 'Отчет по доходам и расходам',
                'date_block': False,
                'period_block': True,
                'links': []
            },
            {
                'report': 4,
                'title': 'Отчет по заказам на препарат',
                'date_block': False,
                'period_block': True,
                'links': [
                    {'title': 'Препарат', 'table': 's-medicine', 'name': 'medicine'},
                ]
            },
            {
                'report': 5,
                'title': 'Отчет по динамике средней цены на препарат',
                'date_block': False,
                'period_block': True,
                'links': [
                    {'title': 'Препарат', 'table': 's-medicine', 'name': 'medicine'},
                ]
            },
            {
                'report': 6,
                'title': 'Отчет по датам последних поставок',
                'date_block': True,
                'period_block': False,
                'links': []
            },
        ],
    }

    select_list = ['s-medicine',]
    custom_context['list_selects'] = []
    for s in select_list:
        custom_context['list_selects'].append({
            'name': s,
            'title': get_title_select(s),
            'records': [{'pk': x.id, 'text': str(x)} for x in get_obj_select(s).objects.all()]
        })

    return render(request, 'mainapp/reports.html', context | custom_context)

def report_print(request, report):
    pass

def error_access(request, exception=0):
    custom_context = {
        'fav': STATIC_URL + 'mainapp/other/favicon.jpg',
        'error': STATIC_URL + 'mainapp/css/error.css',
        'common': STATIC_URL + 'mainapp/css/common.css',
        'def': STATIC_URL + 'mainapp/css/default.css',
        'smile': STATIC_URL + 'mainapp/svg/smile.svg',
        'bg': STATIC_URL + 'mainapp/other/bg.jpg',
    }
    return render(request, '404.html', custom_context, status=404)