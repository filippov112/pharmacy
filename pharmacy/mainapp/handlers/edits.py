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
    ob = Certificate.objects.get(id=record)
    n = 'certificate'
    if request.method == 'POST':
        try:
            ob.delete()
            return redirect(n + '_list')
        except IntegrityError as e:
            error = 'Существуют связанные записи: ' + ', '.join(
                [str(x) for x in (e.protected_objects if e.protected_objects else [])])

    default_context = get_default_context(n, user=request.user, title=str(ob), error=error)
    view_context = get_edit_context(n, ob)
    custom_context = {
        'task': 'edit',
        # Фото, Артикул, Название, Группа, Срок, Условия хранения, Рецепт, Взаимодействие, Ограничения, Побочные эффекты, Инструкция
        'input_fields': [
            # image, text, textarea, number, date, file, link
            #
            # image                         - name, url
            # file                          - name, text_value
            # link                          - name, text_value, select
            # text, number, date, textarea  - name, value
            {'type': 'image', 'url': ob.photo.url, 'name': 'i-', 'title': '', 'value': '', 'text_value': '',
             'select': ''},
        ],

        'list_selects': [
            {
                'name': '',
                'title': '',
                'records': [{'pk': x.id, 'text': str(x)} for x in ...]
            },
        ]
    }
    return render(request, 'mainapp/edit.html', default_context | view_context | custom_context)


@login_required(login_url=login_view)
def contract_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


