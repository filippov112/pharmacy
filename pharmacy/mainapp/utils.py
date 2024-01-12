from django.contrib.auth.models import Group

from .models import *
from datetime import datetime
from django.core.files.storage import FileSystemStorage


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

# def replace_null(dic, row=''):
#     ret_dic = {}
#     for key in dic.keys():
#         if dic[key] == '':
#             if key in ['couple-' + row + '-3', 'time_begin', 'time_end']:
#                 ret_dic[key] = '00:00'
#             if key in ['date', 'birth', 'd_passport', 'dn']:
#                 ret_dic[key] = '1900-01-01'
#             if key in ['de']:
#                 ret_dic[key] = '2045-05-09'
#             if key in ['couple-' + row + '-0', 'couple-' + row + '-1', 'hippodrome', 'city', 'owner', 'race', 'horse',
#                        'jockey']:
#                 ret_dic[key] = '-1'
#             if key in ['couple-' + row + '-2', 'distance', 'summa', 's_passport', 'n_passport', 'age', 'report']:
#                 ret_dic[key] = '0'
#         else:
#             ret_dic[key] = dic[key]
#     return ret_dic



# Логическое поле "Требует рецепта" для модели лекарства
def required_presc(v):
    if v:
        return "Требует"
    else:
        return "Не требует"


# Список выборок
def get_selects(s_list):
    list_s = []
    for v in s_list:
        obj = check_select(v)
        if obj != {}:
            list_s.append(obj)
    return list_s
def check_select(s):
    match s:
        case 's-supplier':
            return {
                'name': s,
                'title': 'Поставщики',
                'records': [ {'pk': x.id, 'text': x.__str__() } for x in Supplier.objects.all()]
            }
        case 's-contract':
            return {
                'name': s,
                'title': 'Договоры',
                'records': [{'pk': x.id, 'text': x.__str__()} for x in Contract.objects.all()]
            }
        case 's-medicine':
            return {
                'name': s,
                'title': 'Каталог препаратов',
                'records': [{'pk': x.id, 'text': x.__str__()} for x in Medicine.objects.all()]
            }
        case 's-med-group':
            return {
                'name': s,
                'title': 'Группы препаратов',
                'records': [{'pk': x.id, 'text': x.__str__()} for x in MedicineGroup.objects.all()]
            }
        case 's-physical':
            return {
                'name': s,
                'title': 'Клиенты Физ.',
                'records': [{'pk': x.id, 'text': x.__str__()} for x in PhysicalPerson.objects.all()]
            }
        case 's-legal':
            return {
                'name': s,
                'title': 'Клиенты Юр.',
                'records': [{'pk': x.id, 'text': x.__str__()} for x in LegalEntity.objects.all()]
            }
        case 's-user':
            return {
                'name': s,
                'title': 'Сотрудники',
                'records': [{'pk': x.id, 'text': x.__str__()} for x in User.objects.all()]
            }
        case 's-doctor':
            return {
                'name': s,
                'title': 'Врачи',
                'records': [{'pk': x.id, 'text': x.__str__()} for x in Doctor.objects.all()]
            }
        case 's-facility':
            return {
                'name': s,
                'title': 'Лечебные организации',
                'records': [{'pk': x.id, 'text': x.__str__()} for x in MedicalFacility.objects.all()]
            }
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
def get_default_context(_task='', user=None):
    rez = {
        'sidebar': _task != 'login',
        'header': _task != 'login' and _task != 'index',
        'task': _task,
    }
    if user is not None:
        try:
            prf = Profile.objects.get(user=user.id)
            rez['user'] = {
                'fio': user.last_name + ' ' + user.first_name[0].upper() + '.' + prf.middle_name[0].upper() + '.',
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
    ret['desc_table'] = [ x['title'] for x in _elements ]
    ret['sorting_table'] = [{'name': e['field'], 'title': e['title']} for e in _elements]
    ret['list_selects'] = get_selects([e['select'] if e['type'] == 'link' else '' for e in _elements])
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
        ret['elem_table'] = [
            {
                'link': reverse(_name+'_id', args=[x.id]),
                'id': x.id,
                'fields': [
                    getattr(x, e['field']) if e['type'] != 'link' else getattr(x, e['field']).__str__()
                    for e in _elements
                ]
            }
            for x in _records
        ]
    return ret


# Контекст представлений
def get_view_context(_name, _record, _ob):
    ret = {}
    ret['edit_link'] = reverse(_name+'_edit', args=[_record])
    ret['title_view'] = _ob.__str__()
    ret['bread_crumbs'] = get_bread_crumbs(_name)
    return ret