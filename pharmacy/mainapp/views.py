from django.http import HttpResponse
from django.shortcuts import render, redirect
# from mainapp.reports import render_pdf, get_report
# from utils import *


# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, remember=request.POST.get('remember'))
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if form.remember:
                request.session.set_expiry(2592000)  # устанавливаем срок действия сессии на 30 дней (в секундах)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'mainapp/login.html', {'form': form})


# def login(request):
#     return render(request, 'mainapp/login.html')


# def error_access(request):
#     return render(request, 'mainapp/error_access.html', context=get_default_context(request))
#
#
# def reports_list(request):
#     if request.method == 'POST':
#         d = replace_null(request.POST)
#
#         req = {}
#         req['dn'] = datetime.strptime(d['dn'], "%Y-%m-%d").date() if 'dn' in d.keys() else ''
#         req['de'] = datetime.strptime(d['de'], "%Y-%m-%d").date() if 'de' in d.keys() else ''
#         req['report'] = int(d['report']) if d['report'] != '' else ''
#         req['jockey'] = Jockey.objects.filter(id=int(d['jockey'])) if 'jockey' in d.keys() else ''
#         req['horse'] = Horse.objects.filter(id=int(d['horse'])) if 'horse' in d.keys() else ''
#         req['race'] = Race.objects.filter(id=int(d['race'])) if 'race' in d.keys() else ''
#
#         template_path, context = get_report(req)
#
#         pdf = render_pdf(template_path, context)
#         response = HttpResponse(pdf, content_type="application/pdf")
#         response['Content-Disposition'] = "attachment;"
#         return response
#     else:
#         context = get_default_context(request)
#         custom_context = {
#             'title': 'Список печати',
#             'title_table': 'Список печати',
#             'item_selected': 4,
#
#             'list_v': get_list_v(
#                 ['table_horses', 'Лошади', Horse, False],
#                 ['table_jokey', 'Наездники', Jockey, False],
#                 ['table_races', 'Заезды', Race, False],
#             ),
#
#             'reports': [
#                 {
#                     'report_name': 'Рейтинг лошадей за период.pdf',
#                     'report': 0,
#                     'title': 'Рейтинг лошадей за период',
#                     'has_date_block': True,
#                 },
#                 {
#                     'report_name': 'Рейтинг жокеев за период.pdf',
#                     'report': 1,
#                     'title': 'Рейтинг жокеев за период',
#                     'has_date_block': True,
#                 },
#                 {
#                     'report_name': 'Статистика жокея за период.pdf',
#                     'report': 2,
#                     'title': 'Статистика жокея за период',
#                     'links': [
#                         {
#                             'title': 'Жокей',
#                             'name': 'jockey',
#                             'table': 'table_jokey',
#                         },
#                     ],
#                     'has_date_block': True,
#                 },
#                 {
#                     'report_name': 'Статистика лошади за период.pdf',
#                     'report': 3,
#                     'title': 'Статистика лошади за период',
#                     'links': [
#                         {
#                             'title': 'Лошадь',
#                             'name': 'horse',
#                             'table': 'table_horses',
#                         },
#                     ],
#                     'has_date_block': True,
#                 },
#                 {
#                     'report_name': 'Список заездов с результатами за период.pdf',
#                     'report': 4,
#                     'title': 'Список заездов с результатами за период',
#                     'has_date_block': True,
#                 },
#                 {
#                     'report_name': 'Распечатка заезда.pdf',
#                     'report': 5,
#                     'title': 'Распечатка заезда',
#                     'links': [
#                         {
#                             'title': 'Заезд',
#                             'name': 'race',
#                             'table': 'table_races',
#                         },
#                     ],
#                     'has_date_block': False,
#                 },
#             ]
#         }
#         return render(request, 'mainapp/reports.html', context=context | custom_context)