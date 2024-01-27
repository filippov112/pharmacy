from .commons import *


@permission_required('mainapp.view_medicine', raise_exception=True)
@login_required(login_url=login_view)
def medicine_list(request):
    error = ''
    o = Medicine
    n = 'medicine'
    fn = 'medicine'
    elements = [
        {'field': 'article'             , 'title': 'Артикул'                , 'type': 'text'},
        {'field': 'name'                , 'title': 'Наименование'           , 'type': 'text'},
        {'field': 'group'               , 'title': 'Группа препаратов'      , 'type': 'link'    , 'select': 's-med-group'},
    ]
    # Артикул, Наименование, Фарм.группа
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_'+fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Каталог препаратов', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn, no_elem_table=True)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
        'desc_table': [x['title'] for x in elements],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, str(x.group)]
            }
            for x in records
        ],
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)


@permission_required('mainapp.view_prescription', raise_exception=True)
@login_required(login_url=login_view)
def prescription_list(request):
    error = ''
    o = Prescription
    n = 'prescription'
    fn = n
    elements = [
        {'field': 'number'              , 'title': 'Номер'          , 'type': 'number'},
        {'field': 'physical_person'     , 'title': 'Клиент'         , 'type': 'link'    , 'select': 's-physic'},
        {'field': 'prescription_date'   , 'title': 'Дата рецепта'   , 'type': 'date'},
        {'field': 'doctor'              , 'title': 'Врач'           , 'type': 'link'    , 'select': 's-doctor'},
        {'field': 'status'              , 'title': 'Статус'         , 'type': 'text'},
    ]
    # Номер, Клиент, Лекарство, Врач, Статус
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Список рецептов', error=error)
    list_context    = get_list_context(n, elements, records, request.user, fn)
    custom_context  = {
        'add_record': reverse(n+'_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)



@permission_required('mainapp.view_order', raise_exception=True)
@login_required(login_url=login_view)
def order_list(request):
    error = ''
    o = Order
    n = 'order'
    fn = n
    elements = [
        {'field': 'number'          , 'title': 'Номер заказа'   , 'type': 'number'  },
        {'field': 'date'            , 'title': 'Дата заказа'    , 'type': 'date'    },
        {'field': 'physical_person' , 'title': 'Клиент физ.'    , 'type': 'link', 'select': 's-physic'},
        {'field': 'legal_entity'    , 'title': 'Клиент юр.'     , 'type': 'link', 'select': 's-legal'},
        {'field': 'seller'          , 'title': 'Продавец'       , 'type': 'link', 'select': 's-user'},
    ]
    # Номер, Дата, Клиент физ., Клиент юр., Продавец
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Список заказов', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn, no_elem_table=True)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
        'desc_table': ['Номер заказа', 'Дата заказа', 'Клиент', 'Продавец'],
        'elem_table': [
            {
                'link': reverse(n + '_id', args=[x.id]),
                'id': x.id,
                'fields': [
                    x.number,
                    x.date,
                    str(x.physical_person) if x.physical_person else str(x.legal_entity),
                    str(x.seller),
                ]
            }
            for x in records
        ],
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)


@permission_required('mainapp.view_legalentity', raise_exception=True)
@login_required(login_url=login_view)
def legal_list(request):
    error = ''
    o = LegalEntity
    n = 'legal'
    fn = 'legalentity'
    elements = [
        {'field': 'name'        , 'title': 'Название'   , 'type': 'text', },
        {'field': 'address'     , 'title': 'Адрес'      , 'type': 'text', },
        {'field': 'inn'         , 'title': 'ИНН'        , 'type': 'text', },
        {'field': 'kpp'         , 'title': 'КПП'        , 'type': 'text', },
    ]
    # Название, Адрес, ИНН, КПП
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Клиенты - Юридические лица', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)




@permission_required('mainapp.view_physicalperson', raise_exception=True)
@login_required(login_url=login_view)
def physic_list(request):
    error = ''
    o = PhysicalPerson
    n = 'physic'
    fn = 'physicalperson'
    elements = [
        {'field': 'last_name'   , 'title': 'Фамилия'        , 'type': 'text',},
        {'field': 'first_name'  , 'title': 'Имя'            , 'type': 'text',},
        {'field': 'middle_name' , 'title': 'Отчество'       , 'type': 'text',},
        {'field': 'city'        , 'title': 'Город'          , 'type': 'text',},
        {'field': 'address'     , 'title': 'Адрес'          , 'type': 'text',},
        {'field': 'birth_date'  , 'title': 'Дата рождения'  , 'type': 'date',},
    ]
    # ФИО, Город, Адрес, Дата рождения
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Клиенты - Физические лица', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)




@permission_required('mainapp.view_doctor', raise_exception=True)
@login_required(login_url=login_view)
def doctor_list(request):
    error = ''
    o = Doctor
    n = 'doctor'
    fn = n
    elements = [
        {'field': 'last_name'       , 'title': 'Фамилия'        , 'type': 'text'    },
        {'field': 'first_name'      , 'title': 'Имя'            , 'type': 'text'    },
        {'field': 'middle_name'     , 'title': 'Отчество'       , 'type': 'text'    },
        {'field': 'facility'        , 'title': 'Мед. Учреждение', 'type': 'link', 'select': 's-facility'},
        {'field': 'specialization'  , 'title': 'Специализация'  , 'type': 'text'    },
        {'field': 'position'        , 'title': 'Должность'      , 'type': 'text'    },
    ]
    # ФИО, Учреждение, Специализация, Должность
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Реестр врачей', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)




@permission_required('mainapp.view_medicalfacility', raise_exception=True)
@login_required(login_url=login_view)
def facility_list(request):
    error = ''
    o = MedicalFacility
    n = 'facility'
    fn = 'medicalfacility'
    elements = [
        {'field': 'name'        , 'title': 'Название учреждения', 'type': 'text'    },
        {'field': 'city'        , 'title': 'Город'              , 'type': 'text'    },
        {'field': 'address'     , 'title': 'Адрес'              , 'type': 'text'    },
    ]
    # Название, Город, Адрес
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Реестр учреждений', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)




@permission_required('mainapp.view_medicinegroup', raise_exception=True)
@login_required(login_url=login_view)
def med_group_list(request):
    error = ''
    o = MedicineGroup
    n = 'med_group'
    fn = 'medicinegroup'
    elements = [
        {'field': 'group_name', 'title': 'Наименование группы', 'type': 'text'  },
    ]
    # Наименование
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Группы препаратов', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)




@permission_required('mainapp.view_receipt', raise_exception=True)
@login_required(login_url=login_view)
def receipt_list(request):
    error = ''
    o = Receipt
    n = 'receipt'
    fn = n
    elements = [
        {'field': 'contract', 'title': 'Договор'        , 'type': 'link'   , 'select': 's-contract'},
        {'field': 'date'    , 'title': 'Дата поставки'  , 'type': 'date'  },
        {'field': 'number'  , 'title': 'Номер'          , 'type': 'number'  },
    ]
    # Договор, дата
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Список поставок', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)




@permission_required('mainapp.view_certificate', raise_exception=True)
@login_required(login_url=login_view)
def certificate_list(request):
    error = ''
    o = Certificate
    n = 'certificate'
    fn = n
    elements = [
        {'field': 'number'      , 'title': 'Номер'      , 'type': 'number'    },
        {'field': 'medicine'    , 'title': 'Препарат'   , 'type': 'link'    , 'select': 's-medicine'},
        {'field': 'supplier'    , 'title': 'Поставщик'  , 'type': 'link'    , 'select': 's-supplier'},
        {'field': 'start_date'  , 'title': 'Дата начала', 'type': 'date'    },
    ]
    # Номер, Лекарство, Поставщик, Дата начала
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Список сертификатов', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)




@permission_required('mainapp.view_contract', raise_exception=True)
@login_required(login_url=login_view)
def contract_list(request):
    error = ''
    o = Contract
    n = 'contract'
    fn = n
    elements = [
        {'field': 'number'      , 'title': 'Номер'      , 'type': 'number'  },
        {'field': 'supplier'    , 'title': 'Поставщик'  , 'type': 'link'    , 'select':'s-supplier' },
        {'field': 'start_date'  , 'title': 'Дата начала', 'type': 'date'    },
    ]
    # Номер, Поставщик, Дата начала
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Список договоров поставок', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)




@permission_required('mainapp.view_supplier', raise_exception=True)
@login_required(login_url=login_view)
def supplier_list(request):
    error = ''
    o = Supplier
    n = 'supplier'
    fn = n
    elements = [
        {'field': 'name'    , 'title': 'Наименование'   , 'type': 'text'    },
        {'field': 'city'    , 'title': 'Город'          , 'type': 'text'    },
        {'field': 'address' , 'title': 'Адрес'          , 'type': 'text'    },
    ]
    # Наименование, Город, Адрес
    records = []
    if request.method == "POST":
        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_' + fn):
            try:
                dl = [int(x) for x in request.POST.get('delete-list').split(',')]
                obj_list = o.objects.filter(id__in=dl)
                clear_files(o, obj_list)
                obj_list.delete()
            except ProtectedError as e:
                error = str(e)
            records = o.objects.all()
        if 'delete-list' not in request.POST:
            records = get_filtered_records(o, request.POST)
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user, title='Реестр поставщиков', error=error)
    list_context = get_list_context(n, elements, records, request.user, fn)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)
