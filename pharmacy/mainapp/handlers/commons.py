from django.db import IntegrityError
from django.http import HttpResponseServerError, HttpResponse
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
from django.db.models import ProtectedError

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
                'report': 'Отчет по заказам препарата.pdf',
                'title': 'Отчет по заказам препарата',
                'period_block': True,
                'links': [
                    {'title': 'Препарат', 'table': 's-medicine', 'name': 'medicine'},
                ]
            },
            {
                'report': 'Отчет по поставкам препарата.pdf',
                'title': 'Отчет по поставкам препарата',
                'period_block': True,
                'links': [
                    {'title': 'Препарат', 'table': 's-medicine', 'name': 'medicine'},
                ]
            },
            {
                'report': 'Отчет по доходам и расходам.pdf',
                'title': 'Отчет по доходам и расходам',
                'period_block': True,
                'links': []
            },
            {
                'report': 'Отчет по сотрудникам.pdf',
                'title': 'Отчет по сотрудникам',
                'period_block': True,
                'links': [
                    {'title': 'Сотрудник', 'table': 's-user', 'name': 'user'},
                ]
            },
        ],
    }

    select_list = ['s-medicine', 's-user']
    custom_context['list_selects'] = []
    for s in select_list:
        custom_context['list_selects'].append({
            'name': s,
            'title': get_title_select(s),
            'records': [{'pk': x.id, 'text': str(x)} for x in get_obj_select(s).objects.all()]
        })

    return render(request, 'mainapp/reports.html', context | custom_context)

@login_required(login_url=login_view)
def report_print(request, report):
    if request.method == "POST":
        d = request.POST
        context = {}
        template = ''
        f = {}

        match(report):
            case 'Отчет по заказам препарата.pdf':
                template = 'reports/1.html'
                if d['dn']:
                    f['order__date__gte'] = default_val(Order, 'date', d['dn'], is_date=True)
                if d['dk']:
                    f['order__date__lte'] = default_val(Order, 'date', d['dk'], is_date=True)
                if d['medicine'] != '':
                    f['medicine'] = default_val(OrderComposition, 'medicine', int(d['medicine']))
                context = {
                    'name': str(Medicine.objects.get(id=int(d['medicine']))) if d['medicine'] != '' else '',
                    'dn': str(d['dn']),
                    'dk': str(d['dk']),
                    'records': [
                        {
                            'num': x.order.number,
                            'date': x.order.date,
                            'client': str(x.order.physical_person if x.order.physical_person else x.order.legal_entity),
                            'count': x.quantity,
                            'summ': x.price * x.quantity
                        }
                        for x in (OrderComposition.objects.filter(**f) if len(f.keys()) > 0 else OrderComposition.objects.all())
                    ]
                }

            case 'Отчет по поставкам препарата.pdf':
                template = 'reports/2.html'
                if d['dn']:
                    f['receipt__date__gte'] = default_val(Receipt, 'date', d['dn'], is_date=True)
                if d['dk']:
                    f['receipt__date__lte'] = default_val(Receipt, 'date', d['dk'], is_date=True)
                if d['medicine'] != '':
                    f['medicine'] = default_val(ReceiptItem, 'medicine', int(d['medicine']))
                context = {
                    'name': str(Medicine.objects.get(id=int(d['medicine']))) if d['medicine'] != '' else '',
                    'dn': str(d['dn']),
                    'dk': str(d['dk']),
                    'records': [
                        {
                            'supplier': str(x.receipt.contract.supplier),
                            'date': x.receipt.date,
                            'count': x.quantity,
                            'price': x.unit_price * x.quantity,
                        }
                        for x in (ReceiptItem.objects.filter(**f) if len(f.keys()) > 0 else ReceiptItem.objects.all())
                    ]
                }

            case 'Отчет по доходам и расходам.pdf':
                template = 'reports/3.html'
                if d['dn']:
                    f['date__gte'] = default_val(Receipt, 'date', d['dn'], is_date=True)
                if d['dk']:
                    f['date__lte'] = default_val(Receipt, 'date', d['dk'], is_date=True)
                R = Receipt.objects.filter(**f) if len(f.keys()) > 0 else Receipt.objects.all()

                f = {}
                if d['dn']:
                    f['date__gte'] = default_val(Order, 'date', d['dn'], is_date=True)
                if d['dk']:
                    f['date__lte'] = default_val(Order, 'date', d['dk'], is_date=True)
                O = Order.objects.filter(**f) if len(f.keys()) > 0 else Order.objects.all()

                context = {
                    'dn': str(d['dn']),
                    'dk': str(d['dk']),

                    'receipts': [
                        {
                            'date': str(x.date),
                            'number': x.number,
                            'summ': sum([y.quantity * y.unit_price for y in ReceiptItem.objects.filter(receipt=x.id)]),
                        }
                        for x in R
                    ],
                    'orders': [
                        {
                            'date': str(x.date),
                            'number': x.number,
                            'summ': sum([y.quantity * y.price for y in OrderComposition.objects.filter(order=x.id)]),
                        }
                        for x in O
                    ],
                    'summ_receipt':sum([y.quantity * y.unit_price for y in ReceiptItem.objects.filter(receipt__in=[x.id for x in R])]),
                    'summ_order':sum([y.quantity * y.price for y in OrderComposition.objects.filter(order__in=[x.id for x in O])])
                }

            case 'Отчет по сотрудникам.pdf':
                template = 'reports/4.html'
                if d['dn']:
                    f['date__gte'] = default_val(Order, 'date', d['dn'], is_date=True)
                if d['dk']:
                    f['date__lte'] = default_val(Order, 'date', d['dk'], is_date=True)
                if d['user'] != '':
                    f['seller'] = default_val(Order, 'seller', int(d['user']))
                O = Order.objects.filter(**f) if len(f.keys()) > 0 else Order.objects.all()
                context = {
                    'user': str(Profile.objects.get(id=int(d['user']))) if d['user'] != '' else '',
                    'dn': str(d['dn']),
                    'dk': str(d['dk']),
                    'records': [
                        {
                            'number': x.number,
                            'date': str(x.date),
                            'client': str(x.physical_person if x.physical_person else x.legal_entity),
                            'summ': sum([y.quantity * y.price for y in OrderComposition.objects.filter(order=x.id)])
                        }
                        for x in O
                    ],
                    'all_summ': sum([y.quantity * y.price for y in OrderComposition.objects.filter(order__in=[x.id for x in O])])
                }

        pdf = render_pdf(template, context)
        response = HttpResponse(pdf, content_type="application/pdf")
        response['Content-Disposition'] = "attachment;"
        return response
    else:
        return redirect('index')

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