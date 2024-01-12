from .commons import *
@permission_required('mainapp.view_prescription', raise_exception=True)
@login_required(login_url=login_view)
def prescription_id(request, record):
    ob = Prescription.objects.get(id=record)
    n = 'prescription'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_prescription'):
        ob.delete()
        return redirect(n + '_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Скан, Номер, Физ.лицо, Врач, Дата рецепта, Дата обращения, Статус
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        # Состав рецепта
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)

@permission_required('mainapp.view_order', raise_exception=True)
@login_required(login_url=login_view)
def order_id(request, record):
    ob = Order.objects.get(id=record)
    n = 'order'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_order'):
        ob.delete()
        return redirect(n + '_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Номер, Дата, Физ.лицо, Юр.Лицо, Продавец
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        # Состав заказа
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)

@permission_required('mainapp.view_legalentity', raise_exception=True)
@login_required(login_url=login_view)
def legal_id(request, record):
    ob = LegalEntity.objects.get(id=record)
    n = 'legal'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_legalentity'):
        ob.delete()
        return redirect(n + '_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Название, Адрес, ИНН, КПП, Телефон, Контакт, Должность контакта, Скидки
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        # Список заказов
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)

@permission_required('mainapp.view_physicalperson', raise_exception=True)
@login_required(login_url=login_view)
def physic_id(request, record):
    ob = PhysicalPerson.objects.get(id=record)
    n = 'physic'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_physicalperson'):
        ob.delete()
        return redirect(n + '_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Фамилия, Имя, Отчество, Город, Адрес, Телефон, Дата рождения, Пол, Льготы
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        # Рецепты, Заказы
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)

@permission_required('mainapp.view_doctor', raise_exception=True)
@login_required(login_url=login_view)
def doctor_id(request, record):
    ob = Doctor.objects.get(id=record)
    n = 'doctor'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_doctor'):
        ob.delete()
        return redirect(n + '_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Фамилия, Имя, Отчество, Учреждение, Телефон, Специализация, Должность, График работы
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        # Список рецептов
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)

@permission_required('mainapp.view_medicalfacility', raise_exception=True)
@login_required(login_url=login_view)
def facility_id(request, record):
    ob = MedicalFacility.objects.get(id=record)
    n = 'facility'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_medicalfacility'):
        ob.delete()
        return redirect(n + '_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Название, Город, Адрес, Телефон, Почта, График работы, Профили
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        # Список врачей
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)

@permission_required('mainapp.view_receipt', raise_exception=True)
@login_required(login_url=login_view)
def receipt_id(request, record):
    ob = Receipt.objects.get(id=record)
    n = 'receipt'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_receipt'):
        ob.delete()
        return redirect(n + '_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Договор, Дата
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        # Состав поставки
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)

@permission_required('mainapp.view_certificate', raise_exception=True)
@login_required(login_url=login_view)
def certificate_id(request, record):
    ob = Certificate.objects.get(id=record)
    n = 'certificate'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_certificate'):
        ob.delete()
        return redirect(n + '_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Препарат, Поставщик, Скан, Номер, Дата начала, Дата окончания, Орган
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        # Приложения к сертификату
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)

@permission_required('mainapp.view_contract', raise_exception=True)
@login_required(login_url=login_view)
def contract_id(request, record):
    ob = Contract.objects.get(id=record)
    n = 'contract'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_contract'):
        ob.delete()
        return redirect(n + '_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Скан, Поставщик, Номер, Дата начала, Дата окончания, Сроки поставки, Размеры партий,
        # Способ оплаты, Условия доставки, Возможность пролонгации, Прочие условия
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        # Препараты, Поставки
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)

@permission_required('mainapp.view_supplier', raise_exception=True)
@login_required(login_url=login_view)
def supplier_id(request, record):
    ob = Supplier.objects.get(id=record)
    n = 'supplier'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_supplier'):
        ob.delete()
        return redirect(n+'_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Наименование, Город, Адрес, Телефон, Почта, ИНН, КПП, ОГРН
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)


@permission_required('mainapp.view_medicinegroup', raise_exception=True)
@login_required(login_url=login_view)
def med_group_id(request, record):
    ob = MedicineGroup.objects.get(id=record)
    n = 'med_group'
    if request.method == 'POST' and check_user_rules(request.user, 'delete_medicinegroup'):
        ob.delete()
        return redirect(n + '_list')

    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, ob)
    custom_context = {
        # Название
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'ОГРН', 'text': ob.ogrn},
        ],
        # Препараты
        'side_tables': [
            {
                'title': 'Договоры',
                'head': ['Номер', 'Дата начала', 'Дата окончания'],
                'records': [
                    {
                        'link': reverse('contract_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.start_date), 'link': ''},
                            {'type': 'text', 'text': str(x.end_date), 'link': ''},
                        ]
                    }
                    for x in Contract.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Сертификаты',
                'head': ['Номер', 'Препарат', 'Орган'],
                'records': [
                    {
                        'link': reverse('certificate_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.medicine.__str__(), 'link': ''},
                            {'type': 'text', 'text': x.certifying_authority, 'link': ''},
                        ]
                    }
                    for x in Certificate.objects.filter(supplier=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)