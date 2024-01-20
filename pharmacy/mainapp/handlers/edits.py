from .commons import *


@login_required(login_url=login_view)
def prescription_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def order_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def receipt_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@permission_required('mainapp.change_certificate', raise_exception=True)
@login_required(login_url=login_view)
def certificate_edit(request, record):
    error = ''
    o = Certificate
    n = 'certificate'
    if request.method == 'POST':
        id_rec = save_record(record, o, request)
        return redirect(reverse(n + "_id", args=[id_rec]))
    else:
        if record != 'new':
            ob = o.objects.get(id=record)
        else:
            ob = o.objects.create()

    title = 'Редактирование: ' + str(ob) if record != 'new' else 'Новая запись'
    task = record
    default_context = get_default_context(n, user=request.user, title=title, error=error)
    view_context = get_edit_context(task, n, ob)
    custom_context = {
        'task': task,
        'input_fields': [
            # image, text, textarea, number, date, file, link
            #
            # image                         - name, url
            # file                          - name, text_value
            # link                          - name, text_value, select
            # text, number, date, textarea  - name, value
            {'type': 'image', 'url': default_val(o, 'photo', ob.photo), 'name': 'i-photo', 'title': 'Изображение',
             'value': '', 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-article', 'title': 'Артикул',
             'value': default_val(o, 'article', ob.article), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-name', 'title': 'Наименование',
             'value': default_val(o, 'name', ob.name), 'text_value': '',
             'select': ''},
            {'type': 'link', 'url': '', 'name': 'i-group', 'title': 'Лекарственная группа', 'value': '',
             'text_value': default_val(o, 'group', ob.group),
             'select': 's-med_group'},
            {'type': 'date', 'url': '', 'name': 'i-expiration_date', 'title': 'Годен до',
             'value': default_val(o, 'expiration_date', ob.expiration_date), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-storage_conditions', 'title': 'Условия хранения',
             'value': default_val(o, 'storage_conditions', ob.storage_conditions), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-interactions', 'title': 'Взаимодействие с другими лекарствами',
             'value': default_val(o, 'interactions', ob.interactions), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-limitations', 'title': 'Ограничения к применению',
             'value': default_val(o, 'limitations', ob.limitations), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-side_effects', 'title': 'Побочные эффекты',
             'value': default_val(o, 'side_effects', ob.side_effects), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-usage_instruction', 'title': 'Инструкция к применению',
             'value': default_val(o, 'usage_instruction', ob.usage_instruction), 'text_value': '',
             'select': ''},
        ],

        'list_selects': [
            {
                'name': 's-med_group',
                'title': 'Лекарственные группы',
                'records': [{'pk': x.id, 'text': str(x)} for x in MedicineGroup.objects.all()]
            },
        ]
    }
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/edit.html', default_context | view_context | custom_context)


@login_required(login_url=login_view)
def contract_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


