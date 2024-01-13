from .commons import *



@login_required(login_url=login_view)
def medicine_list(request):
    o = Medicine
    n = 'medicine'
    elements = [
        {'field': 'article'             , 'title': 'Артикул'                , 'type': 'text'},
        {'field': 'name'                , 'title': 'Наименование'           , 'type': 'text'},
        {'field': 'group.group_name'    , 'title': 'Группа препаратов'      , 'type': 'link', 'select': 's-med-group'},
        {'field': 'pre_required'        , 'title': 'Необходимость рецепта'  , 'type': 'checkbox'},
    ]
    # Артикул, Наименование, Фарм.группа, Требует рецепта
    records = []
    if request.method == "POST":
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass

        if 'delete-list' in request.POST and check_user_rules(request.user, 'delete_medicine'):
            dl = [int(x) for x in request.POST.get('delete-list').split(',')]
            o.objects.filter(id=any(dl)).delete()
            records = o.objects.all()
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records, no_elem_table=True)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
        'desc_table': [x['title'] for x in elements],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, str(x.group), required_presc(x.pre_required)]
            }
            for x in records
        ],
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)


@login_required(login_url=login_view)
def prescription_list(request):
    o = Prescription
    n = 'prescription'
    elements = [
        {'field': 'number'              , 'title': 'Номер'          , 'type': 'text'},
        {'field': 'physical_person'     , 'title': 'Клиент'         , 'type': 'link'    , 'select': 's-physic'},
        {'field': 'prescription_date'   , 'title': 'Дата рецепта'   , 'type': 'date'},
        {'field': 'doctor'              , 'title': 'Врач'           , 'type': 'link'    , 'select': 's-doctor'},
        {'field': 'status'              , 'title': 'Статус'         , 'type': 'text'},
    ]
    # Номер, Клиент, Лекарство, Врач, Статус
    records = []
    if request.method == "POST":
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context    = get_list_context(n, elements, records)
    custom_context  = {
        'add_record': reverse(n+'_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)




@login_required(login_url=login_view)
def order_list(request):
    o = Order
    n = 'order'
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
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records, no_elem_table=True)
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



@login_required(login_url=login_view)
def legal_list(request):
    o = LegalEntity
    n = 'legal'
    elements = [
        {'field': 'name'        , 'title': 'Название'   , 'type': 'text', },
        {'field': 'address'     , 'title': 'Адрес'      , 'type': 'text', },
        {'field': 'inn'         , 'title': 'ИНН'        , 'type': 'text', },
        {'field': 'kpp'         , 'title': 'КПП'        , 'type': 'text', },
    ]
    # Название, Адрес, ИНН, КПП
    records = []
    if request.method == "POST":
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)





@login_required(login_url=login_view)
def physic_list(request):
    o = PhysicalPerson
    n = 'physic'
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
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)





@login_required(login_url=login_view)
def doctor_list(request):
    o = Doctor
    n = 'doctor'
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
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)





@login_required(login_url=login_view)
def facility_list(request):
    o = MedicalFacility
    n = 'facility'
    elements = [
        {'field': 'name'        , 'title': 'Название учреждения', 'type': 'text'    },
        {'field': 'city'        , 'title': 'Город'              , 'type': 'text'    },
        {'field': 'address'     , 'title': 'Адрес'              , 'type': 'text'    },
    ]
    # Название, Город, Адрес
    records = []
    if request.method == "POST":
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)





@login_required(login_url=login_view)
def med_group_list(request):
    o = MedicineGroup
    n = 'med_group'
    elements = [
        {'field': 'group_name', 'title': 'Наименование группы', 'type': 'text'  },
    ]
    # Наименование
    records = []
    if request.method == "POST":
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)





@login_required(login_url=login_view)
def receipt_list(request):
    o = Receipt
    n = 'receipt'
    elements = [
        {'field': 'contract', 'title': 'Договор'        , 'type': 'link'   , 'select': 's-contract'},
        {'field': 'date'    , 'title': 'Дата поставки'  , 'type': 'date'  },
    ]
    # Договор, дата
    records = []
    if request.method == "POST":
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)





@login_required(login_url=login_view)
def certificate_list(request):
    o = Certificate
    n = 'certificate'
    elements = [
        {'field': 'number'      , 'title': 'Номер'      , 'type': 'text'    },
        {'field': 'medicine'    , 'title': 'Препарат'   , 'type': 'link'    , 'select': 's-medicine'},
        {'field': 'supplier'    , 'title': 'Поставщик'  , 'type': 'link'    , 'select': 's-supplier'},
        {'field': 'start_date'  , 'title': 'Дата начала', 'type': 'date'    },
    ]
    # Номер, Лекарство, Поставщик, Дата начала
    records = []
    if request.method == "POST":
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)





@login_required(login_url=login_view)
def contract_list(request):
    o = Contract
    n = 'contract'
    elements = [
        {'field': 'number'      , 'title': 'Номер'      , 'type': 'number'  },
        {'field': 'supplier'    , 'title': 'Поставщик'  , 'type': 'link'    , 'select':'s-supplier' },
        {'field': 'start_date'  , 'title': 'Дата начала', 'type': 'date'    },
    ]
    # Номер, Поставщик, Дата начала
    records = []
    if request.method == "POST":
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)





@login_required(login_url=login_view)
def supplier_list(request):
    o = Supplier
    n = 'supplier'
    elements = [
        {'field': 'name'    , 'title': 'Наименование'   , 'type': 'text'    },
        {'field': 'city'    , 'title': 'Город'          , 'type': 'text'    },
        {'field': 'address' , 'title': 'Адрес'          , 'type': 'text'    },
    ]
    # Наименование, Город, Адрес
    records = []
    if request.method == "POST":
        form_name = request.POST.get('form_name')
        if form_name == "filters":
            pass
            # records = Medicine.objects.filter()
            # ...
            # records = records.order_by(*request.POST.parameter_sorting.split(","))
        if form_name == "table_delete":
            pass
    else:
        records = o.objects.all()

    default_context = get_default_context(n, user=request.user)
    list_context = get_list_context(n, elements, records)
    custom_context = {
        'add_record': reverse(n + '_new', args=['new']),
    }
    return render(request, 'mainapp/list.html', default_context | list_context | custom_context)
