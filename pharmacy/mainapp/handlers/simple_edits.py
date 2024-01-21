from django.db import DataError

from .commons import *

@permission_required('mainapp.change_medicine', raise_exception=True)
@login_required(login_url=login_view)
def medicine_edit(request, record):
    error = ''
    o = Medicine
    n = 'medicine'
    if request.method == 'POST':
        try:
            id_rec = save_record(record, o, request)
            return redirect(reverse(n + "_id", args=[id_rec]))
        except DataError as e:
            error = str(e)

    if record != 'new':
        ob = o.objects.get(id=record)
    else:
        ob = o.objects.create()

    title = 'Редактирование: '+str(ob) if record != 'new' else 'Новая запись'
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
            {'type': 'image', 'url': default_val(o, 'photo', ob.photo), 'name':'i-photo', 'title': 'Изображение', 'value': '', 'text_value':'',
             'select':''},
            {'type': 'text', 'url': '', 'name': 'i-article', 'title': 'Артикул', 'value': default_val(o, 'article', ob.article), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-name', 'title': 'Наименование', 'value': default_val(o, 'name', ob.name), 'text_value': '',
             'select': ''},
            {'type': 'link', 'url': '', 'name': 'i-group', 'title': 'Лекарственная группа', 'value': '', 'text_value': default_val(o, 'group', ob.group),
             'select': 's-med_group'},
            {'type': 'date', 'url': '', 'name': 'i-expiration_date', 'title': 'Годен до', 'value': default_val(o, 'expiration_date', ob.expiration_date), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-storage_conditions', 'title': 'Условия хранения', 'value': default_val(o, 'storage_conditions', ob.storage_conditions), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-interactions', 'title': 'Взаимодействие с другими лекарствами', 'value': default_val(o, 'interactions', ob.interactions), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-limitations', 'title': 'Ограничения к применению', 'value': default_val(o, 'limitations', ob.limitations), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-side_effects', 'title': 'Побочные эффекты', 'value': default_val(o, 'side_effects', ob.side_effects), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-usage_instruction', 'title': 'Инструкция к применению', 'value': default_val(o, 'usage_instruction', ob.usage_instruction), 'text_value': '',
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
    custom_context['input_fields'] = [
        {**x, 'maxlength': o._meta.get_field(x['name'][2:]).max_length} if x['type'] in (
        'text', 'number', 'textarea') else x
        for x in custom_context['input_fields']
    ]

    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/simple_view_edit.html', default_context | view_context | custom_context)


@permission_required('mainapp.change_legalentity', raise_exception=True)
@login_required(login_url=login_view)
def legal_edit(request, record):
    error = ''
    o = LegalEntity
    n = 'legal'
    if request.method == 'POST':
        try:
            id_rec = save_record(record, o, request)
            return redirect(reverse(n + "_id", args=[id_rec]))
        except DataError as e:
            error = str(e)

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
            {'type': 'text', 'url': '', 'name': 'i-name', 'title': 'Название',
             'value': default_val(o, 'name', ob.name), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-address', 'title': 'Адрес',
             'value': default_val(o, 'address', ob.address), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-phone', 'title': 'Телефон',
             'value': default_val(o, 'phone', ob.phone), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-inn', 'title': 'ИНН',
             'value': default_val(o, 'inn', ob.inn), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-kpp', 'title': 'КПП',
             'value': default_val(o, 'name', ob.kpp), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-contact_person', 'title': 'Контактное лицо',
             'value': default_val(o, 'contact_person', ob.contact_person), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-contact_person_position', 'title': 'Должность контактного лица',
             'value': default_val(o, 'contact_person_position', ob.contact_person_position), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-discounts', 'title': 'Предоставляемые скидки',
             'value': default_val(o, 'discounts', ob.discounts), 'text_value': '',
             'select': ''},
        ],

        'list_selects': []
    }
    custom_context['input_fields'] = [
        {**x, 'maxlength': o._meta.get_field(x['name'][2:]).max_length} if x['type'] in (
        'text', 'number', 'textarea') else x
        for x in custom_context['input_fields']
    ]
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/simple_view_edit.html', default_context | view_context | custom_context)


@permission_required('mainapp.change_physicalperson', raise_exception=True)
@login_required(login_url=login_view)
def physic_edit(request, record):
    error = ''
    o = PhysicalPerson
    n = 'physic'
    if request.method == 'POST':
        try:
            id_rec = save_record(record, o, request)
            return redirect(reverse(n + "_id", args=[id_rec]))
        except DataError as e:
            error = str(e)

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
            {'type': 'text', 'url': '', 'name': 'i-last_name', 'title': 'Фамилия',
             'value': default_val(o, 'last_name', ob.last_name), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-first_name', 'title': 'Имя',
             'value': default_val(o, 'first_name', ob.first_name), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-middle_name', 'title': 'Отчество',
             'value': default_val(o, 'middle_name', ob.middle_name), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-city', 'title': 'Город',
             'value': default_val(o, 'city', ob.city), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-address', 'title': 'Адрес',
             'value': default_val(o, 'address', ob.address), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-phone', 'title': 'Телефон',
             'value': default_val(o, 'phone', ob.phone), 'text_value': '',
             'select': ''},
            {'type': 'date', 'url': '', 'name': 'i-birth_date', 'title': 'Дата рождения',
             'value': default_val(o, 'birth_date', ob.birth_date), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-benefits', 'title': 'Предоставляемые льготы',
             'value': default_val(o, 'benefits', ob.benefits), 'text_value': '',
             'select': ''},
        ],

        'list_selects': []
    }
    custom_context['input_fields'] = [
        {**x, 'maxlength': o._meta.get_field(x['name'][2:]).max_length} if x['type'] in (
        'text', 'number', 'textarea') else x
        for x in custom_context['input_fields']
    ]
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/simple_view_edit.html', default_context | view_context | custom_context)


@permission_required('mainapp.change_doctor', raise_exception=True)
@login_required(login_url=login_view)
def doctor_edit(request, record):
    error = ''
    o = Doctor
    n = 'doctor'
    if request.method == 'POST':
        try:
            id_rec = save_record(record, o, request)
            return redirect(reverse(n + "_id", args=[id_rec]))
        except DataError as e:
            error = str(e)

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
            {'type': 'link', 'url': '', 'name': 'i-facility', 'title': 'Лечебное учреждение', 'value': '',
             'text_value': default_val(o, 'facility', ob.facility),
             'select': 's-facility'},
            {'type': 'text', 'url': '', 'name': 'i-last_name', 'title': 'Фамилия',
             'value': default_val(o, 'last_name', ob.last_name), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-first_name', 'title': 'Имя',
             'value': default_val(o, 'first_name', ob.first_name), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-middle_name', 'title': 'Отчество',
             'value': default_val(o, 'middle_name', ob.middle_name), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-phone', 'title': 'Телефон',
             'value': default_val(o, 'phone', ob.phone), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-specialization', 'title': 'Специализация',
             'value': default_val(o, 'specialization', ob.specialization), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-position', 'title': 'Должность',
             'value': default_val(o, 'position', ob.position), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-work_schedule', 'title': 'График работы',
             'value': default_val(o, 'work_schedule', ob.work_schedule), 'text_value': '',
             'select': ''},
        ],

        'list_selects': [
            {
                'name': 's-facility',
                'title': 'Лечебные учреждения',
                'records': [{'pk': x.id, 'text': str(x)} for x in MedicalFacility.objects.all()]
            },
        ]
    }
    custom_context['input_fields'] = [
        {**x, 'maxlength': o._meta.get_field(x['name'][2:]).max_length} if x['type'] in (
        'text', 'number', 'textarea') else x
        for x in custom_context['input_fields']
    ]
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/simple_view_edit.html', default_context | view_context | custom_context)


@permission_required('mainapp.change_medicalfacility', raise_exception=True)
@login_required(login_url=login_view)
def facility_edit(request, record):
    error = ''
    o = MedicalFacility
    n = 'facility'
    if request.method == 'POST':
        try:
            id_rec = save_record(record, o, request)
            return redirect(reverse(n + "_id", args=[id_rec]))
        except DataError as e:
            error = str(e)

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
            {'type': 'text', 'url': '', 'name': 'i-name', 'title': 'Название',
             'value': default_val(o, 'name', ob.name), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-city', 'title': 'Город',
             'value': default_val(o, 'city', ob.city), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-address', 'title': 'Адрес',
             'value': default_val(o, 'address', ob.address), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-phone', 'title': 'Телефон',
             'value': default_val(o, 'phone', ob.phone), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-email', 'title': 'Электронная почта',
             'value': default_val(o, 'email', ob.email), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-work_schedule', 'title': 'График работы',
             'value': default_val(o, 'work_schedule', ob.work_schedule), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-profiles', 'title': 'Профили услуг',
             'value': default_val(o, 'profiles', ob.profiles), 'text_value': '',
             'select': ''},
        ],

        'list_selects': []
    }

    custom_context['input_fields'] = [
        {**x, 'maxlength': o._meta.get_field(x['name'][2:]).max_length } if x['type'] in ('text', 'number', 'textarea') else x
        for x in custom_context['input_fields']
    ]

    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/simple_view_edit.html', default_context | view_context | custom_context)


@permission_required('mainapp.change_supplier', raise_exception=True)
@login_required(login_url=login_view)
def supplier_edit(request, record):
    error = ''
    o = Supplier
    n = 'supplier'
    if request.method == 'POST':
        try:
            id_rec = save_record(record, o, request)
            return redirect(reverse(n + "_id", args=[id_rec]))
        except DataError as e:
            error = str(e)

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
            {'type': 'text', 'url': '', 'name': 'i-name', 'title': 'Наименование',
             'value': default_val(o, 'name', ob.name), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-city', 'title': 'Город',
             'value': default_val(o, 'city', ob.city), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-address', 'title': 'Адрес',
             'value': default_val(o, 'address', ob.address), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-phone', 'title': 'Телефон',
             'value': default_val(o, 'phone', ob.phone), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-email', 'title': 'Электронная почта',
             'value': default_val(o, 'email', ob.email), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-inn', 'title': 'ИНН',
             'value': default_val(o, 'inn', ob.inn), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-kpp', 'title': 'КПП',
             'value': default_val(o, 'kpp', ob.kpp), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-ogrn', 'title': 'ОГРН',
             'value': default_val(o, 'ogrn', ob.ogrn), 'text_value': '',
             'select': ''},
        ],

        'list_selects': []
    }
    custom_context['input_fields'] = [
        {**x, 'maxlength': o._meta.get_field(x['name'][2:]).max_length} if x['type'] in (
        'text', 'number', 'textarea') else x
        for x in custom_context['input_fields']
    ]
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/simple_view_edit.html', default_context | view_context | custom_context)


@permission_required('mainapp.change_medicinegroup', raise_exception=True)
@login_required(login_url=login_view)
def med_group_edit(request, record):
    error = ''
    o = MedicineGroup
    n = 'med_group'
    if request.method == 'POST':
        try:
            id_rec = save_record(record, o, request)
            return redirect(reverse(n + "_id", args=[id_rec]))
        except DataError as e:
            error = str(e)

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
            {'type': 'text', 'url': '', 'name': 'i-group_name', 'title': 'Название группы',
             'value': default_val(o, 'group_name', ob.group_name), 'text_value': '',
             'select': ''},
        ],

        'list_selects': []
    }
    custom_context['input_fields'] = [
        {**x, 'maxlength': o._meta.get_field(x['name'][2:]).max_length} if x['type'] in (
        'text', 'number', 'textarea') else x
        for x in custom_context['input_fields']
    ]
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/simple_view_edit.html', default_context | view_context | custom_context)