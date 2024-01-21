from _decimal import Decimal

from django.contrib.auth.models import Group
from django.urls import reverse
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import django.db.models.fields.files as dj_files
from django.db import models
from .models import Medicine, Prescription, Order, LegalEntity, PhysicalPerson, Doctor, MedicalFacility, \
    MedicineGroup, Receipt, Certificate, Contract, Supplier, PrescComposition, Profile, CertificateAttachment, \
    ContractMedicine, ReceiptItem, OrderComposition


def get_link(url_name, field):
    if field:
        return reverse(url_name, args=[field.id])
    return ''

# Формируем фио из составляющих
def get_FIO(last_name, first_name, middle_name):
    formatted_name = last_name.capitalize() if last_name else ''
    if first_name and len(first_name) > 0:
        formatted_name += ' ' + first_name[0].upper() + '.' if formatted_name else first_name[0] + '.'
    if middle_name and len(middle_name) > 0:
        formatted_name += ' ' + middle_name[0].upper() + '.' if formatted_name else middle_name[0] + '.'
    return formatted_name

def check_user_rules(usr, rule):
    if usr.is_superuser or rule in get_user_permissions(usr):
        return True
    return False

def get_user_permissions(usr):
    # Сначала соберем персональные права
    perms = set()
    for p in usr.user_permissions.all():
        perms.add(p.codename)
    # Затем соберем с групп
    groups = usr.groups.all()
    for group in groups:
        permissions = group.permissions.all()
        for p in permissions:
            perms.add(p.codename)
    return perms


# Список выборок
def get_title_select(s_name):
    match s_name:
        case 's-supplier': return 'Поставщики'
        case 's-contract': return 'Договоры'
        case 's-medicine': return 'Каталог препаратов'
        case 's-med-group': return 'Группы препаратов'
        case 's-physic': return 'Клиенты Физ.'
        case 's-legal': return 'Клиенты Юр.'
        case 's-user': return 'Сотрудники'
        case 's-doctor': return 'Врачи'
        case 's-facility': return 'Лечебные организации'
    return ''

def get_obj_select(s_name):
    match s_name:
        case 's-supplier': return Supplier
        case 's-contract': return Contract
        case 's-medicine': return Medicine
        case 's-med-group': return MedicineGroup
        case 's-physic': return PhysicalPerson
        case 's-legal': return LegalEntity
        case 's-user': return Profile
        case 's-doctor': return Doctor
        case 's-facility': return MedicalFacility
    return {}

# Сайдбар
def get_side_menu(usr=None, su_mod=False):
    full_list = [ 'settings', 'view_supplier', 'view_contract', 'view_certificate', 'view_receipt',
        'view_physicalperson', 'view_legalentity', 'view_prescription', 'view_medicine', 'view_medicinegroup',
        'view_order', 'view_doctor', 'view_medicalfacility'
    ]
    tasks = []
    if not su_mod:
        if usr.is_superuser:
            perms = full_list
        else:
            perms = get_user_permissions(usr)
    else:
        perms = full_list
    for p in perms:
        match p:
            case 'settings':
                tasks.append({
                    'name': 'settings',
                    'title': 'Панель администратора',
                    'url': reverse('admin:index'),
                    'static_path': 'mainapp/svg/settings.svg',
                })
            case 'view_supplier':
                tasks.append({
                    'name': 'supplier',
                    'title': 'Реестр поставщиков',
                    'url': reverse('supplier_list'),
                    'static_path': 'mainapp/svg/supplier.svg',
                })
            case 'view_contract':
                tasks.append({
                    'name': 'contract',
                    'title': 'Договора поставок',
                    'url': reverse('contract_list'),
                    'static_path': 'mainapp/svg/contract.svg',
                })
            case 'view_certificate':
                tasks.append({
                    'name': 'certificate',
                    'title': 'Сертификаты качества',
                    'url': reverse('certificate_list'),
                    'static_path': 'mainapp/svg/certificate.svg',
                })
            case 'view_receipt':
                tasks.append({
                    'name': 'receipt',
                    'title': 'Поставки',
                    'url': reverse('receipt_list'),
                    'static_path': 'mainapp/svg/box.svg',
                })
            case 'view_physicalperson':
                tasks.append({
                    'name': 'physic',
                    'title': 'Клиенты физ.',
                    'url': reverse('physic_list'),
                    'static_path': 'mainapp/svg/client_f.svg',
                })
            case 'view_legalentity':
                tasks.append({
                    'name': 'legal',
                    'title': 'Клиенты юр.',
                    'url': reverse('legal_list'),
                    'static_path': 'mainapp/svg/client_u.svg',
                })
            case 'view_prescription':
                tasks.append({
                    'name': 'prescription',
                    'title': 'Рецепты',
                    'url': reverse('prescription_list'),
                    'static_path': 'mainapp/svg/prescription.svg',
                })
            case 'view_medicine':
                tasks.append({
                    'name': 'medicine',
                    'title': 'Каталог препаратов',
                    'url': reverse('medicine_list'),
                    'static_path': 'mainapp/svg/medicine.svg',
                })
            case 'view_medicinegroup':
                tasks.append({
                    'name': 'med_group',
                    'title': 'Группы препаратов',
                    'url': reverse('med_group_list'),
                    'static_path': 'mainapp/svg/medicine_group.svg',
                })
            case 'view_order':
                tasks.append({
                    'name': 'order',
                    'title': 'Список заказов',
                    'url': reverse('order_list'),
                    'static_path': 'mainapp/svg/order.svg',
                })
            case 'view_doctor':
                tasks.append({
                    'name': 'doctor',
                    'title': 'Реестр врачей',
                    'url': reverse('doctor_list'),
                    'static_path': 'mainapp/svg/doctor.svg',
                })
            case 'view_medicalfacility':
                tasks.append({
                    'name': 'facility',
                    'title': 'Реестр учреждений',
                    'url': reverse('facility_list'),
                    'static_path': 'mainapp/svg/hospital.svg',
                })
    return tasks


# Хлебные крошки для шапок отдельных записей
def get_bread_crumbs(_task):
    side_menu = get_side_menu(su_mod=True)
    dic_sm = { obj['name']: obj for obj in side_menu }
    return [{'link': dic_sm[_task]['url'], 'title': dic_sm[_task]['title']}]



# Общий контекст
def get_default_context(_task='', user=None, title='', error=''):
    rez = {
        'title': title,
        'sidebar': _task != 'login',
        'header': _task != 'login' and _task != 'index',
        'task': _task,
        'error': error,
    }
    if user is not None:
        try:
            prf = Profile.objects.get(user=user.id)
            rez['user'] = {
                'fio': get_FIO(user.last_name, user.first_name, prf.middle_name),
                'job': prf.position,
            }
        except:
            pass
        rez['side_menu'] = get_side_menu(usr=user)
    return rez


# Контекст списков
def get_list_context(_name, _elements, _records, no_elem_table=False):
    ret = {}
    ret['title_view'] = { x['name']: x['title'] for x in get_side_menu(su_mod=True)}[_name]
    ret['sorting_table'] = [{'name': e['field'], 'title': e['title']} for e in _elements]

    ret['list_selects'] = []
    for e in _elements:
        if e['type'] == 'link':
            s = e['select']
            ret['list_selects'].append({
                'name': s,
                'title': get_title_select(s),
                'records': [{'pk': x.id, 'text': str(x)} for x in get_obj_select(s).objects.all()]
            })

    ret['filters'] = [
        {
            'names': ['f-' + e['field'], ] if e['type'] != 'date' else ['f-' + e['field'] + '-dn',
                                                                        'f-' + e['field'] + '-dk'],
            'title': e['title'],
            'type': e['type'],
            'select': e['select'] if e['type'] == 'link' else ''
        }
        for e in _elements
    ]
    if not no_elem_table:
        ret['desc_table'] = [x['title'] for x in _elements]
        ret['elem_table'] = [
            {
                'link': reverse(_name+'_id', args=[x.id]),
                'id': x.id,
                'fields': [
                    getattr(x, e['field']) if e['type'] != 'link' else str(getattr(x, e['field']))
                    for e in _elements
                ]
            }
            for x in _records
        ]
    return ret


# Контекст представлений
def get_view_context(_name, _record, _ob, _fn, _usr):
    ret = {}
    ret['edit_link'] = reverse(_name+'_edit', args=[_record])
    ret['title_view'] = str(_ob)
    ret['bread_crumbs'] = get_bread_crumbs(_name)
    rules = get_user_permissions(_usr)
    ret['delete_rule'] = 'delete_'+_fn in rules or _usr.is_superuser
    ret['change_rule'] = 'change_'+_fn in rules or _usr.is_superuser
    return ret


def get_edit_context(task, _name, _ob):
    ret = {}
    ret['bread_crumbs'] = get_bread_crumbs(_name)
    ret['title_view'] = 'Редактирование: '+str(_ob) if task != 'new' else 'Новая запись'
    return ret


def get_object(n):
    match n:
        case 'CertificateAttachment':
            return { 'obj':CertificateAttachment, 'fk':'certificate' }
        case 'ContractMedicine':
            return { 'obj':ContractMedicine, 'fk':'contract' }
        case 'ReceiptItem':
            return { 'obj':ReceiptItem, 'fk':'receipt' }
        case 'OrderComposition':
            return { 'obj':OrderComposition, 'fk':'order' }
        case 'PrescComposition':
            return { 'obj':PrescComposition, 'fk':'prescription' }
    return {}

def replace_null(o, field, val):
    f = o._meta.get_field(field)
    field_type = f.get_internal_type()
    match field_type:
        case 'FileField'|'ImageField':
            return None
        case 'ForeignKey'|'OneToOneField':
            rem_m = f.remote_field.model
            return rem_m.objects.get(id=val) if val else None
    return val

def s_file(ob, field, FILES, key):
    file = getattr(FILES, key, None)
    if file:
        getattr(ob, field).save(file.name, file)
    return ob


def default_val(o, field, val, is_link=False):
    f = o._meta.get_field(field).get_internal_type()
    match f:
        case 'ForeignKey'|'OneToOneField':
            return val if val else ''
        case 'ImageField':
            return val.url if val else ''
        case 'FileField':
            if is_link:
                return val.url if val else ''
            return val.name.split('/')[-1] if val else ''
        case 'DateField':
            return str(val)
    return val

def save_record(record, o, request, side_table_names={}, fsr=[]):
    # side_table_names = {'name': 'structure',}
    dic = request.POST
    FILES = getattr(request, 'FILES', None)

    ls_tables = {}
    ob = {}
    obj_record = {}

    if record != 'new':
        ob = o.objects.get(id=record)

    for key in dic.keys():
        str_key = key.split("-")
        table_name = str_key[0]

        # Найдем всё что связано со сторонними таблицами
        if len(str_key) == 3 and table_name in side_table_names.keys():
            field_name = str_key[1]
            field_n = str_key[2]
            field_val = dic[key]

            if table_name not in ls_tables.keys():
                ls_tables[table_name] = {}
            if field_n not in ls_tables[table_name].keys():
                ls_tables[table_name][field_n] = {}
            ls_tables[table_name][field_n][field_name] = field_val

        # Если это поле записи - внесем изменения
        if len(str_key) == 2 and str_key[0] == 'i':
            field_name = str_key[1]
            field_val = replace_null(o, field_name, dic[key])
            if field_val:
                if record != 'new':
                    setattr(ob, field_name, field_val)
                else:
                    obj_record[field_name] = field_val

    # Сохраним запись после изменения
    if record == 'new':
        ob = o(**obj_record)

    mFiles = {}
    if FILES:
        for key in FILES.keys():
            str_key = key.split("-")
            table_name = str_key[0]

            # Найдем всё что связано со сторонними таблицами
            if len(str_key) == 3 and table_name in side_table_names.keys():
                field_name = str_key[1]
                field_n = str_key[2]
                f = FILES[key]

                if table_name not in mFiles.keys():
                    mFiles[table_name] = {}
                if field_n not in mFiles[table_name].keys():
                    mFiles[table_name][field_n] = {}
                mFiles[table_name][field_n][field_name] = f

            if len(str_key) == 2 and str_key[0] == 'i':
                field_name = str_key[1]
                file = FILES[key]
                if file:
                    getattr(ob, field_name).save(file.name, file, save=True)
    ob.save()

    # Почистим записи сторонних таблиц, прежде чем добавлять измененные (кроме файлов для сертификатов)
    for table_name in side_table_names.keys():
        o = get_object(table_name)
        rec = {o['fk']:ob.id}
        objs_delete = o['obj'].objects.filter(**rec)
        if len(fsr) > 0:
            objs_delete = objs_delete.exclude(id__in=fsr)
        objs_delete.delete()

    # Пробросим новые сторонние записи
    for table_name in ls_tables.keys():
        o = get_object(table_name)
        for rec in ls_tables[table_name].keys():
            r_dic = {}
            for f in ls_tables[table_name][rec].keys():
                v = replace_null(o['obj'], f, ls_tables[table_name][rec][f])
                if v:
                    r_dic[f] = v
            r_dic[o['fk']] = ob
            obj = o['obj'].objects.create(**r_dic)

            if getattr(mFiles, table_name, None):
                if getattr(mFiles[table_name], rec, None):
                    for f in mFiles[table_name][rec].keys():
                        file = mFiles[table_name][rec][f]
                        if file:
                            getattr(obj, f).save(file.name, file, save=True)

    return ob.id


def get_filtered_records(o, dic):
    mF = {}
    for f in dic.keys():
        str_keys = f.split('-')
        if str_keys[0] == 'f':
            key = str_keys[1]
            val = dic[f]
            field_type = o._meta.get_field(key).get_internal_type()
            if val:
                match(field_type):
                    case 'DateField':
                        key += '__gte' if str_keys[2] == 'dn' else '__lte'
                    case 'CharField'|'TextField':
                        key += '__icontains'
                    case 'ForeignKey':
                        key += '__in'
                        val = [int(x) for x in val.split(',')]
                mF[key] = val

    objs = o.objects.filter(**mF) if len(mF.keys()) > 0 else o.objects.all()

    ps = dic['parameter_sorting']
    if ps != '':
        ps = ps.split(',')
        objs = objs.order_by(*ps)

    return objs