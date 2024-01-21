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
            {'type': 'link', 'url': '', 'name': 'i-medicine', 'title': 'Препарат', 'value': '',
             'text_value': default_val(o, 'medicine', ob.medicine),
             'select': 's-medicine'},
            {'type': 'link', 'url': '', 'name': 'i-supplier', 'title': 'Поставщик', 'value': '',
             'text_value': default_val(o, 'supplier', ob.supplier),
             'select': 's-supplier'},
            {'type': 'file', 'url': '', 'name': 'i-document_scan', 'title': 'Скан документа',
             'value': '', 'text_value': default_val(o, 'document_scan', ob.document_scan),
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-number', 'title': 'Номер',
             'value': default_val(o, 'number', ob.number), 'text_value': '',
             'select': ''},
            {'type': 'date', 'url': '', 'name': 'i-start_date', 'title': 'Дата начала действия',
             'value': default_val(o, 'start_date', ob.start_date), 'text_value': '',
             'select': ''},
            {'type': 'date', 'url': '', 'name': 'i-end_date', 'title': 'Дата окончания действия',
             'value': default_val(o, 'end_date', ob.end_date), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-certifying_authority', 'title': 'Сертифицирующий орган',
             'value': default_val(o, 'certifying_authority', ob.certifying_authority), 'text_value': '',
             'select': ''},
        ],

        'list_selects': [
            {
                'name': 's-medicine',
                'title': 'Каталог препаратов',
                'records': [{'pk': x.id, 'text': str(x)} for x in Medicine.objects.all()]
            },
            {
                'name': 's-supplier',
                'title': 'Реестр поставщиков',
                'records': [{'pk': x.id, 'text': str(x)} for x in Supplier.objects.all()]
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


