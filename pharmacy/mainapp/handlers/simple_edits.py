from .commons import *

@permission_required('mainapp.change_medicine', raise_exception=True)
@login_required(login_url=login_view)
def medicine_edit(request, record):
    error = ''
    o = Medicine
    n = 'medicine'
    if request.method == 'POST':
        id_rec = save_record(record, o, request.POST)
        return redirect(n+"_id", args=[id_rec])
    else:
        if record != 'new':
            ob = Medicine.objects.get(id=record)
        else:
            ob = Medicine.objects.create()

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
            {'type': 'image', 'url': ob.photo.url, 'name':'i-photo', 'title': 'Изображение', 'value': '', 'text_value':'',
             'select':''},
            {'type': 'text', 'url': '', 'name': 'i-article', 'title': 'Артикул', 'value': ob.article, 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-name', 'title': 'Наименование', 'value': ob.name, 'text_value': '',
             'select': ''},
            {'type': 'link', 'url': '', 'name': 'i-group', 'title': 'Лекарственная группа', 'value': '', 'text_value': str(ob.group),
             'select': 's-med_group'},
            {'type': 'date', 'url': '', 'name': 'i-expiration_date', 'title': 'Годен до', 'value': str(ob.expiration_date), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-storage_conditions', 'title': 'Условия хранения', 'value': ob.storage_conditions, 'text_value': '',
             'select': ''},
            {'type': 'checkbox', 'url': '', 'name': 'i-pre_required', 'title': 'Требует рецепта', 'value': ob.pre_required, 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-interactions', 'title': 'Взаимодействие с другими лекарствами', 'value': ob.interactions, 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-limitations', 'title': 'Ограничения к применению', 'value': ob.limitations, 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-side_effects', 'title': 'Побочные эффекты', 'value': ob.side_effects, 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-usage_instruction', 'title': 'Инструкция к применению', 'value': ob.usage_instruction, 'text_value': '',
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
    return render(request, 'mainapp/simple_view_edit.html', default_context | view_context | custom_context)


@login_required(login_url=login_view)
def legal_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def physic_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def doctor_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def facility_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)



@login_required(login_url=login_view)
def supplier_edit(request):
    if request.resolver_match.view_name == 'prescription_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def med_group_edit(request):
    if request.resolver_match.view_name == 'med_group_new':
        pass
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/simple_view_edit.html', context | custom_context)