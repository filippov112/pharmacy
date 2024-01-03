from .commons import *



@login_required(login_url=login_view)
def medicine_list(request):
    # Артикул, Наименование, Фарм.группа, Требует рецепта
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def prescription_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def order_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def legal_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def physic_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def doctor_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def facility_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def med_group_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def receipt_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def certificate_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def contract_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)





@login_required(login_url=login_view)
def supplier_list(request):
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
        records = Medicine.objects.all()
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'add_record': reverse('medicine_new', args=['new']),
        'desc_table': ['Артикул', 'Наименование', 'Группа препаратов', 'Необходимость рецепта'],
        'elem_table': [
            {
                'link': reverse('medicine_id', args=[x.id]),
                'id': x.id,
                'fields': [x.article, x.name, x.group.__str__(), required_presc(x.pre_required)]
            }
            for x in records
        ],
        'filters': [
            {'names': ['f-name',]           , 'title': 'Поиск по названию'       , 'type': 'text'    },
            {'names': ['f-article', ]       , 'title': 'Поиск по артикулу'       , 'type': 'text'    },
            {'names': ['f-group', ]         , 'title': 'Группы'                 , 'type': 'number'  },
            {'names': ['f-pre_required', ]  , 'title': 'Обязательность рецепта' , 'type': 'checkbox'},
        ],
        'sorting_table': [
            {'name': 'article', 'title': 'Артикул'},
            {'name': 'name', 'title': 'Наименование'},
            {'name': 'group.group_name', 'title': 'Группа препаратов'},
            {'name': 'pre_required', 'title': 'Необходимость рецепта'},
        ]
    }
    return render(request, 'mainapp/list.html', context | custom_context)
