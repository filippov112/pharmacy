from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm
from ..mainapp.utils import get_default_context


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
            context = get_default_context(punkt_selected='login', sidebar=False)
            custom_context = {'form': form, 'error': error, }
            return render(request, 'mainapp/login.html', context | custom_context)

    # Если пользователь уже авторизован, либо авторизация прошла без ошибок,
    # перенаправляем на главную страницу
    return redirect('index')


@login_required
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


@login_required
def medicine_id(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def prescription_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def order_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def legal_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def physic_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def doctor_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def facility_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def receipt_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def certificate_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def contract_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def supplier_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def medicine_edit(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def prescription_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def order_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def legal_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def physic_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def doctor_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def facility_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def med_group_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def receipt_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def certificate_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def contract_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def supplier_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required
def medicine_list(request):
    context = get_default_context(punkt_selected='index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


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
