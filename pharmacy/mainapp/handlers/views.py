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
            {'type': 'image', 'link': ob.document_scan.url, 'title': '', 'text': ''},
            {'type': 'text', 'link': '', 'title': 'Номер', 'text': ob.number},
            {'type': 'text', 'link': '', 'title': 'Клиент', 'text': ob.physical_person},
            {'type': 'link', 'link': get_link('doctor_id', ob.doctor), 'title': 'Врач', 'text': str(ob.doctor)},
            {'type': 'text', 'link': '', 'title': 'Дата выписки рецепта', 'text': ob.prescription_date},
            {'type': 'text', 'link': '', 'title': 'Дата обращения в аптеку', 'text': ob.pharmacy_visit_date},
            {'type': 'text', 'link': '', 'title': 'Статус', 'text': ob.status},
        ],
        # Состав рецепта
        'side_tables': [
            {
                'title': 'Состав рецепта',
                'head': ['Препарат', 'Дозировка'],
                'records': [
                    {
                        'link': reverse('medicine_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': str(x.medicine), 'link': ''},
                            {'type': 'text', 'text': x.dosage, 'link': ''},
                        ]
                    }
                    for x in PrescComposition.objects.filter(prescription=record)  # названия сторонних моделей
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
    if ob.physical_person is None:
        client_link = reverse("legal_id", args=[ob.legal_entity.id])
        client = ob.legal_entity
    else:
        client_link = reverse("physic_id", args=[ob.physical_person.id])
        client = ob.physical_person
    custom_context = {
        # Номер, Дата, Физ.лицо, Юр.Лицо, Продавец
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'Номер', 'text': ob.number},
            {'type': 'text', 'link': '', 'title': 'Дата заказа', 'text': ob.date},
            {'type': 'link', 'link': client_link, 'title': 'Клиент', 'text': str(client)},
            {'type': 'text', 'link': '', 'title': 'Продавец', 'text': str(ob.seller)},
        ],
        # Состав заказа
        'side_tables': [
            {
                'title': 'Состав заказа',
                'head': ['Препарат', 'Цена за единицу', 'Кол-во товара'],
                'records': [
                    {
                        'link': reverse('medicine_id', args=[x.medicine.id]),
                        'fields': [
                            {'type': 'text', 'text': str(x.medicine), 'link': ''},
                            {'type': 'text', 'text': str(x.price) + " руб.", 'link': ''},
                            {'type': 'text', 'text': str(x.quantity) + " шт.", 'link': ''},
                        ]
                    }
                    for x in OrderComposition.objects.filter(order=record)  # названия сторонних моделей
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
            {'type': 'text', 'link': '', 'title': 'Название', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'ИНН', 'text': ob.inn},
            {'type': 'text', 'link': '', 'title': 'КПП', 'text': ob.kpp},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Контактное лицо', 'text': ob.contact_person},
            {'type': 'text', 'link': '', 'title': 'Должность контактного лица', 'text': ob.contact_person_position},
            {'type': 'text', 'link': '', 'title': 'Предоставляемые скидки', 'text': ob.discounts},
        ],
        # Список заказов
        'side_tables': [
            {
                'title': 'Список заказов',
                'head': ['Номер', 'Дата заказа', 'Продавец'],
                'records': [
                    {
                        'link': reverse('order_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.date, 'link': ''},
                            {'type': 'text', 'text': str(x.seller), 'link': ''},
                        ]
                    }
                    for x in Order.objects.filter(legal_entity=record)  # названия сторонних моделей
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
        # ФИО, Город, Адрес, Телефон, Дата рождения, Пол, Льготы
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'ФИО', 'text': ob.last_name.capitalize() + " " + ob.first_name.capitalize() + " " + ob.middle_name.capitalize() },
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Дата рождения', 'text': ob.birth_date},
            {'type': 'text', 'link': '', 'title': 'Пол', 'text': get_gender(ob.gender)},
            {'type': 'text', 'link': '', 'title': 'Предоставляемые льготы', 'text': ob.benefits},
        ],
        # Рецепты, Заказы
        'side_tables': [
            {
                'title': 'Список рецептов',
                'head': ['Номер', 'Доктор', 'Статус'],
                'records': [
                    {
                        'link': reverse('prescription_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.doctor), 'link': ''},
                            {'type': 'text', 'text': x.status, 'link': ''},
                        ]
                    }
                    for x in Prescription.objects.filter(physical_person=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Список заказов',
                'head': ['Номер', 'Дата заказа', 'Продавец'],
                'records': [
                    {
                        'link': reverse('order_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': x.date, 'link': ''},
                            {'type': 'text', 'text': str(x.seller), 'link': ''},
                        ]
                    }
                    for x in Order.objects.filter(physical_person=record)  # названия сторонних моделей
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
        # ФИО, Должность, Специализация, Учреждение, Телефон, График работы
        'content_view': [
            {'type': 'text', 'link': '', 'title': 'ФИО', 'text': ob.last_name.capitalize() + " " + ob.first_name.capitalize() + " " + ob.middle_name.capitalize() },
            {'type': 'text', 'link': '', 'title': 'Должность', 'text': ob.position},
            {'type': 'text', 'link': '', 'title': 'Специализация', 'text': ob.specialization},
            {'type': 'link', 'link': get_link('facility_id', ob.facility), 'title': 'Мед. учреждение', 'text': str(ob.facility)},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'График работы', 'text': ob.work_schedule},
        ],
        # Список рецептов
        'side_tables': [
            {
                'title': 'Список рецептов',
                'head': ['Номер', 'Клиент', 'Статус'],
                'records': [
                    {
                        'link': reverse('prescription_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.number, 'link': ''},
                            {'type': 'text', 'text': str(x.physical_person), 'link': ''},
                            {'type': 'text', 'text': x.status, 'link': ''},
                        ]
                    }
                    for x in Prescription.objects.filter(doctor=record)  # названия сторонних моделей
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
            {'type': 'text', 'link': '', 'title': 'Название', 'text': ob.name},
            {'type': 'text', 'link': '', 'title': 'Город', 'text': ob.city},
            {'type': 'text', 'link': '', 'title': 'Адрес', 'text': ob.address},
            {'type': 'text', 'link': '', 'title': 'Телефон', 'text': ob.phone},
            {'type': 'text', 'link': '', 'title': 'Электронная почта', 'text': ob.email},
            {'type': 'text', 'link': '', 'title': 'График работы', 'text': ob.work_schedule},
            {'type': 'text', 'link': '', 'title': 'Профили услуг', 'text': ob.profiles},
        ],
        # Список врачей
        'side_tables': [
            {
                'title': 'Список врачей',
                'head': ['ФИО', 'Должность', 'Специализация'],
                'records': [
                    {
                        'link': reverse('doctor_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': get_FIO(x.last_name, x.first_name, x.middle_name), 'link': ''},
                            {'type': 'text', 'text': str(x.position), 'link': ''},
                            {'type': 'text', 'text': str(x.specialization), 'link': ''},
                        ]
                    }
                    for x in Doctor.objects.filter(facility=record)  # названия сторонних моделей
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
            {'type': 'link', 'link': get_link('contract_id', ob.contract), 'title': 'Договор', 'text': str(ob.contract)},
            {'type': 'text', 'link': '', 'title': 'Дата поставки', 'text': ob.date},
        ],
        # Детализация поставки
        'side_tables': [
            {
                'title': 'Детализация поставки',
                'head': ['Препарат', 'Цена за единицу', 'Кол-во товара'],
                'records': [
                    {
                        'link': reverse('medicine_id', args=[x.medicine.id]),
                        'fields': [
                            {'type': 'text', 'text': str(x.medicine), 'link': ''},
                            {'type': 'text', 'text': str(x.quantity) + " руб.", 'link': ''},
                            {'type': 'text', 'text': str(x.unit_price) + " шт.", 'link': ''},
                        ]
                    }
                    for x in ReceiptItem.objects.filter(receipt=record)  # названия сторонних моделей
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
        # Скан, Номер, Препарат, Поставщик, Дата начала, Дата окончания, Орган
        'content_view': [
            {'type': 'image', 'link': ob.document_scan.url, 'title': '', 'text': ''},
            {'type': 'text', 'link': '', 'title': 'Номер', 'text': ob.number},
            {'type': 'link', 'link': get_link('medicine_id', ob.medicine), 'title': 'Препарат', 'text': str(ob.medicine)},
            {'type': 'link', 'link': get_link('supplier_id', ob.supplier), 'title': 'Поставщик', 'text': str(ob.supplier)},
            {'type': 'text', 'link': '', 'title': 'Дата начала действия', 'text': ob.start_date},
            {'type': 'text', 'link': '', 'title': 'Дата окончания действия', 'text': ob.end_date},
            {'type': 'text', 'link': '', 'title': 'Сертифицирующий орган', 'text': ob.certifying_authority},
        ],
        # Приложения к сертификату
        'side_tables': [
            {
                'title': 'Приложения к сертификату',
                'head': ['Файл'],
                'records': [
                    {
                        'link': '',
                        'fields': [
                            {'type': 'file', 'text': x.document_scan.name.split('/')[-1], 'link': x.document_scan.url},
                        ]
                    }
                    for x in CertificateAttachment.objects.filter(certificate=record)  # названия сторонних моделей
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
        # Скан, Номер, Поставщик, Дата начала, Дата окончания, Сроки поставки, Размеры партий,
        # Способ оплаты, Условия доставки, Возможность пролонгации, Прочие условия
        'content_view': [
            {'type': 'image', 'link': ob.document_scan.url, 'title': '', 'text': ''},
            {'type': 'text', 'link': '', 'title': 'Номер договора', 'text': ob.number},
            {'type': 'link', 'link': get_link('supplier_id', ob.supplier), 'title': 'Поставщик', 'text': str(ob.supplier)},
            {'type': 'text', 'link': '', 'title': 'Дата начала действия', 'text': ob.start_date},
            {'type': 'text', 'link': '', 'title': 'Дата окончания действия', 'text': ob.end_date},
            {'type': 'text', 'link': '', 'title': 'Сроки поставки', 'text': ob.delivery_terms},
            {'type': 'text', 'link': '', 'title': 'Размеры партий', 'text': ob.batch_sizes},
            {'type': 'text', 'link': '', 'title': 'Способ оплаты', 'text': ob.payment_method},
            {'type': 'text', 'link': '', 'title': 'Условия доставки', 'text': ob.delivery_conditions},
            {'type': 'text', 'link': '', 'title': 'Возможность пролонгации', 'text': ob.prolongation},
            {'type': 'text', 'link': '', 'title': 'Прочие условия', 'text': ob.other_conditions},
        ],
        # Препараты, Поставки
        'side_tables': [
            {
                'title': 'Список препаратов',
                'head': ['Препарат', 'Цены', 'Скидки'],
                'records': [
                    {
                        'link': reverse('medicine_id', args=[x.medicine.id]),
                        'fields': [
                            {'type': 'text', 'text': str(x.medicine), 'link': ''},
                            {'type': 'text', 'text': x.prices, 'link': ''},
                            {'type': 'text', 'text': x.discount_conditions, 'link': ''},
                        ]
                    }
                    for x in ContractMedicine.objects.filter(contract=record)  # названия сторонних моделей
                ]
            },
            {
                'title': 'Поставки по договору',
                'head': ['Код поставки', 'Дата'],
                'records': [
                    {
                        'link': reverse('receipt_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.id, 'link': ''},
                            {'type': 'text', 'text': x.date, 'link': ''},
                        ]
                    }
                    for x in Receipt.objects.filter(contract=record)  # названия сторонних моделей
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
                            {'type': 'text', 'text': x.start_date, 'link': ''},
                            {'type': 'text', 'text': x.end_date, 'link': ''},
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
                            {'type': 'text', 'text': str(x.medicine), 'link': ''},
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
            {'type': 'text', 'link': '', 'title': 'Название группы', 'text': ob.group_name},
        ],
        # Препараты
        'side_tables': [
            {
                'title': 'Препараты группы',
                'head': ['Артикул', 'Наименование'],
                'records': [
                    {
                        'link': reverse('medicine_id', args=[x.id]),
                        'fields': [
                            {'type': 'text', 'text': x.article, 'link': ''},
                            {'type': 'text', 'text': x.name, 'link': ''},
                        ]
                    }
                    for x in Medicine.objects.filter(group=record)  # названия сторонних моделей
                ]
            },
        ]
    }
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)