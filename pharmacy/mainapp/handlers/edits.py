from .commons import *


@permission_required('mainapp.change_prescription', raise_exception=True)
@login_required(login_url=login_view)
def prescription_edit(request, record):
    error = ''
    o = Prescription
    n = 'prescription'
    side_table = 'PrescComposition'
    side_table_struct = 'medicine:link:s-medicine;dosage:text:'
    if request.method == 'POST':
        id_rec = save_record(record, o, request, { side_table: side_table_struct })
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
            {'type': 'file', 'url': '', 'name': 'i-document_scan', 'title': 'Скан документа',
             'value': '', 'text_value': default_val(o, 'document_scan', ob.document_scan),
             'select': ''},
            {'type': 'link', 'url': '', 'name': 'i-physical_person', 'title': 'Клиент', 'value': '',
             'text_value': default_val(o, 'physical_person', ob.physical_person),
             'select': 's-physic'},
            {'type': 'link', 'url': '', 'name': 'i-doctor', 'title': 'Лечащий врач', 'value': '',
             'text_value': default_val(o, 'doctor', ob.doctor),
             'select': 's-doctor'},
            {'type': 'date', 'url': '', 'name': 'i-prescription_date', 'title': 'Дата рецепта',
             'value': default_val(o, 'prescription_date', ob.prescription_date), 'text_value': '',
             'select': ''},
            {'type': 'date', 'url': '', 'name': 'i-pharmacy_visit_date', 'title': 'Дата обращения в аптеку',
             'value': default_val(o, 'pharmacy_visit_date', ob.pharmacy_visit_date), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-number', 'title': 'Номер',
             'value': default_val(o, 'number', ob.number), 'text_value': '',
             'select': ''},
            {'type': 'text', 'url': '', 'name': 'i-status', 'title': 'Статус',
             'value': default_val(o, 'status', ob.status), 'text_value': '',
             'select': ''},
        ],

        'list_selects': [
            {
                'name': 's-physic',
                'title': 'Физ.лица',
                'records': [{'pk': x.id, 'text': str(x)} for x in PhysicalPerson.objects.all()]
            },
            {
                'name': 's-doctor',
                'title': 'Реестр врачей',
                'records': [{'pk': x.id, 'text': str(x)} for x in Doctor.objects.all()]
            },
            {
                'name': 's-medicine',
                'title': 'Каталог препаратов',
                'records': [{'pk': x.id, 'text': str(x)} for x in Medicine.objects.all()]
            },
        ],

        'side_tables': [
            {
                'title': 'Детализация рецепта',
                'head': ['Препарат', 'Дозировка'],
                'structure_fields': side_table_struct,
                'name': side_table,
                'records': [
                    {
                        'pk': x.id,
                        'fields': [
                            {
                                'type': 'link',
                                'value': x.medicine.id if x.medicine else '',
                                'maxlength': '',
                                'text': x.medicine if x.medicine else '',
                                'select': 's-medicine',
                            },
                            {
                                'type': 'text',
                                'value': x.dosage,
                                'maxlength': PrescComposition._meta.get_field('dosage').max_length,
                                'text': '',
                                'select': '',
                            },
                        ]
                    } for x in PrescComposition.objects.filter(prescription=record)
                ] if record != 'new' else []
            },
        ]
    }
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/edit.html', default_context | view_context | custom_context)


@permission_required('mainapp.change_order', raise_exception=True)
@login_required(login_url=login_view)
def order_edit(request, record):
    error = ''
    o = Order
    n = 'order'
    side_table = 'OrderComposition'
    side_table_struct = 'medicine:link:s-medicine;price:number:;quantity:number:'
    if request.method == 'POST':
        id_rec = save_record(record, o, request, { side_table: side_table_struct })
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
            {'type': 'link', 'url': '', 'name': 'i-physical_person', 'title': 'Заказчик физ.лицо', 'value': '',
             'text_value': default_val(o, 'physical_person', ob.physical_person),
             'select': 's-physic'},
            {'type': 'link', 'url': '', 'name': 'i-legal_entity', 'title': 'Заказчик юр.лицо', 'value': '',
             'text_value': default_val(o, 'legal_entity', ob.legal_entity),
             'select': 's-legal'},
            {'type': 'link', 'url': '', 'name': 'i-seller', 'title': 'Продавец', 'value': '',
             'text_value': default_val(o, 'seller', ob.seller),
             'select': 's-profile'},
            {'type': 'date', 'url': '', 'name': 'i-date', 'title': 'Дата заказа',
             'value': default_val(o, 'date', ob.date), 'text_value': '',
             'select': ''},
            {'type': 'number', 'url': '', 'name': 'i-number', 'title': 'Номер заказа',
             'value': default_val(o, 'number', ob.number), 'text_value': '',
             'select': ''},
        ],

        'list_selects': [
            {
                'name': 's-physic',
                'title': 'Физ.лица',
                'records': [{'pk': x.id, 'text': str(x)} for x in PhysicalPerson.objects.all()]
            },
            {
                'name': 's-legal',
                'title': 'Юр.лица',
                'records': [{'pk': x.id, 'text': str(x)} for x in Supplier.objects.all()]
            },
            {
                'name': 's-profile',
                'title': 'Сотрудники',
                'records': [{'pk': x.id, 'text': str(x)} for x in Profile.objects.all()]
            },
            {
                'name': 's-medicine',
                'title': 'Каталог препаратов',
                'records': [{'pk': x.id, 'text': str(x)} for x in Medicine.objects.all()]
            },
        ],

        'side_tables': [
            {
                'title': 'Препараты в заказе',
                'head': ['Препарат', 'Цена', 'Кол-во'],
                'structure_fields': side_table_struct,
                'name': side_table,
                'records': [
                    {
                        'pk': x.id,
                        'fields': [
                            {
                                'type': 'link',
                                'value': x.medicine.id if x.medicine else '',
                                'maxlength': '',
                                'text': x.medicine if x.medicine else '',
                                'select': 's-medicine',
                            },
                            {
                                'type': 'number',
                                'value': x.price,
                                'maxlength': OrderComposition._meta.get_field('price').max_length,
                                'text': '',
                                'select': '',
                            },
                            {
                                'type': 'number',
                                'value': x.quantity,
                                'maxlength': OrderComposition._meta.get_field('quantity').max_length,
                                'text': '',
                                'select': '',
                            },
                        ]
                    } for x in OrderComposition.objects.filter(order=record)
                ] if record != 'new' else []
            },
        ]
    }
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/edit.html', default_context | view_context | custom_context)


@permission_required('mainapp.change_receipt', raise_exception=True)
@login_required(login_url=login_view)
def receipt_edit(request, record):
    error = ''
    o = Receipt
    n = 'receipt'
    side_table = 'ReceiptItem'
    side_table_struct = 'medicine:link:s-medicine;quantity:number:;unit_price:number:'
    if request.method == 'POST':
        id_rec = save_record(record, o, request, { side_table: side_table_struct })
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
            {'type': 'link', 'url': '', 'name': 'i-contract', 'title': 'Договор', 'value': '',
             'text_value': default_val(o, 'contract', ob.contract),
             'select': 's-contract'},
            {'type': 'date', 'url': '', 'name': 'i-date', 'title': 'Дата поставки',
             'value': default_val(o, 'date', ob.date), 'text_value': '',
             'select': ''},
        ],

        'list_selects': [
            {
                'name': 's-contract',
                'title': 'Список договоров',
                'records': [{'pk': x.id, 'text': str(x)} for x in Contract.objects.all()]
            },
            {
                'name': 's-medicine',
                'title': 'Каталог препаратов',
                'records': [{'pk': x.id, 'text': str(x)} for x in Medicine.objects.all()]
            },
        ],

        'side_tables': [
            {
                'title': 'Детализация рецепта',
                'head': ['Препарат', 'Кол-во', 'Цена за штуку'],
                'structure_fields': side_table_struct,
                'name': side_table,
                'records': [
                    {
                        'pk': x.id,
                        'fields': [
                            {
                                'type': 'link',
                                'value': x.medicine.id if x.medicine else '',
                                'maxlength': '',
                                'text': x.medicine if x.medicine else '',
                                'select': 's-medicine',
                            },
                            {
                                'type': 'number',
                                'value': x.quantity,
                                'maxlength': ReceiptItem._meta.get_field('quantity').max_length,
                                'text': '',
                                'select': '',
                            },
                            {
                                'type': 'number',
                                'value': x.unit_price,
                                'maxlength': ReceiptItem._meta.get_field('unit_price').max_length,
                                'text': '',
                                'select': '',
                            },
                        ]
                    } for x in ReceiptItem.objects.filter(receipt=record)
                ] if record != 'new' else []
            },
        ]
    }
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/edit.html', default_context | view_context | custom_context)


@permission_required('mainapp.change_certificate', raise_exception=True)
@login_required(login_url=login_view)
def certificate_edit(request, record):
    error = ''
    o = Certificate
    n = 'certificate'
    side_table = 'CertificateAttachment'
    side_table_struct = 'document_scan:file:'

    if request.method == 'POST':
        fsr = [int(x) for x in request.POST['fsr'].split(',')] if request.POST['fsr'] != '' else []
        id_rec = save_record(record, o, request, { side_table: side_table_struct }, fsr)
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
        ],

        'side_tables': [
            {
                'title': 'Приложения к сертификату',
                'head': ['Файл'],
                'structure_fields': side_table_struct,
                'name': side_table,
                'records': [
                    {
                        'pk': x.id,
                        'fields': [
                            {
                                'type': 'file',
                                'value': '',
                                'maxlength': '',
                                'text': x.document_scan.name.split('/')[0] if x.document_scan else '',
                                'select': '',
                            },
                        ]
                    } for x in CertificateAttachment.objects.filter(certificate=record)
                ] if record != 'new' else []
            },
        ]
    }
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/edit.html', default_context | view_context | custom_context)


@permission_required('mainapp.change_contract', raise_exception=True)
@login_required(login_url=login_view)
def contract_edit(request, record):
    error = ''
    o = Contract
    n = 'contract'
    side_table = 'ContractMedicine'
    side_table_struct = 'medicine:link:s-medicine;prices:text:;discount_conditions:text:'
    if request.method == 'POST':
        id_rec = save_record(record, o, request, { side_table: side_table_struct })
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
            {'type': 'file', 'url': '', 'name': 'i-document_scan', 'title': 'Скан документа',
             'value': '', 'text_value': default_val(o, 'document_scan', ob.document_scan),
             'select': ''},
            {'type': 'link', 'url': '', 'name': 'i-supplier', 'title': 'Поставщик', 'value': '',
             'text_value': default_val(o, 'supplier', ob.supplier),
             'select': 's-supplier'},
            {'type': 'number', 'url': '', 'name': 'i-number', 'title': 'Номер',
             'value': default_val(o, 'number', ob.number), 'text_value': '',
             'select': ''},
            {'type': 'date', 'url': '', 'name': 'i-start_date', 'title': 'Дата начала действия',
             'value': default_val(o, 'start_date', ob.start_date), 'text_value': '',
             'select': ''},
            {'type': 'date', 'url': '', 'name': 'i-end_date', 'title': 'Дата окончания действия',
             'value': default_val(o, 'end_date', ob.end_date), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-delivery_terms', 'title': 'Сроки поставок',
             'value': default_val(o, 'delivery_terms', ob.delivery_terms), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-batch_sizes', 'title': 'Размеры партий',
             'value': default_val(o, 'batch_sizes', ob.batch_sizes), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-payment_method', 'title': 'Способ оплаты',
             'value': default_val(o, 'payment_method', ob.payment_method), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-delivery_conditions', 'title': 'Условия доставки',
             'value': default_val(o, 'delivery_conditions', ob.delivery_conditions), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-prolongation', 'title': 'Возможность пролонгации',
             'value': default_val(o, 'prolongation', ob.prolongation), 'text_value': '',
             'select': ''},
            {'type': 'textarea', 'url': '', 'name': 'i-other_conditions', 'title': 'Прочие условия сторон',
             'value': default_val(o, 'other_conditions', ob.other_conditions), 'text_value': '',
             'select': ''},
        ],

        'list_selects': [
            {
                'name': 's-supplier',
                'title': 'Реестр поставщиков',
                'records': [{'pk': x.id, 'text': str(x)} for x in Supplier.objects.all()]
            },
            {
                'name': 's-medicine',
                'title': 'Каталог препаратов',
                'records': [{'pk': x.id, 'text': str(x)} for x in Medicine.objects.all()]
            },
        ],

        'side_tables': [
            {
                'title': 'Препараты по договору',
                'head': ['Препарат', 'Цены', 'Условия скидок'],
                'structure_fields': side_table_struct,
                'name': side_table,
                'records': [
                    {
                        'pk': x.id,
                        'fields': [
                            {
                                'type': 'link',
                                'value': x.medicine.id if x.medicine else '',
                                'maxlength': '',
                                'text': x.medicine if x.medicine else '',
                                'select': 's-medicine',
                            },
                            {
                                'type': 'text',
                                'value': x.prices,
                                'maxlength': ContractMedicine._meta.get_field('prices').max_length,
                                'text': '',
                                'select': '',
                            },
                            {
                                'type': 'text',
                                'value': x.discount_conditions,
                                'maxlength': ContractMedicine._meta.get_field('discount_conditions').max_length,
                                'text': '',
                                'select': '',
                            },
                        ]
                    } for x in ContractMedicine.objects.filter(contract=record)
                ] if record != 'new' else []
            },
        ]
    }
    if record == 'new':
        ob.delete()
    return render(request, 'mainapp/edit.html', default_context | view_context | custom_context)