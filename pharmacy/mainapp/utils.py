from .models import *
from datetime import datetime
from django.core.files.storage import FileSystemStorage


def get_list_v(*kwargs):
    list_v = []
    v_id = 0
    for v in kwargs:
        obj = dict(name=v[0], title=v[1], records=[], id=v_id)
        v_id += 1
        for o in v[2].objects.all():
            if not v[3]:
                obj['records'].append(dict(pk=o.id, value=o.__str__()))
            else:
                obj['records'].append(dict(pk=o.id, photo=o.city.photo.url, value=o.__str__()))

        list_v.append(obj)

    return list_v


def get_default_context(bread_crumbs=False, punkt_selected='', title_view='', user=None, error=''):
    rez = {
        'title_view': title_view,
        'sidebar': punkt_selected != 'login',
        'header': punkt_selected != 'login' and punkt_selected != 'index',
        'punkt_selected': punkt_selected,
        'list_v': [],
        'error': error,
    }
    if user is not None:
        try:
            prf = Profile.objects.get(user=user.id)
        except:
            prf = {}
        side_menu = get_side_menu(user)
        dic_sm = {obj['name']: obj for obj in side_menu}
        if bread_crumbs:
            rez['bread_crumbs'] = [{'link': dic_sm[punkt_selected]['url'], 'title': dic_sm[punkt_selected]['title']}]
        rez['side_menu'] = side_menu
        if len(user.first_name) > 0 and len(getattr(prf, 'middle_name', '')) > 0:
            rez['user'] = {
                'fio': user.last_name+' '+user.first_name[0].upper()+'.'+prf.middle_name[0].upper()+'.',
                'job': prf.position,
            }
        rez['is_admin'] = user.is_superuser
    return rez


def get_side_menu(usr):
    perms = usr.user_permissions.all()
    punkts = []
    if usr.is_superuser:
        punkts.append({
            'name': 'settings',
            'title': 'Панель администратора',
            'url': reverse('admin:index'),
            'static_path': 'mainapp/svg/settings.svg',
        })
        perms = ['supplier', 'contract', 'certificate', 'receipt', 'physic', 'legal', 'prescription', 'medicine',
                 'med_group', 'order', 'doctor', 'facility']
    for p in perms:
        match p:
            case 'supplier':
                punkts.append({
                    'name': p,
                    'title': 'Реестр поставщиков',
                    'url': reverse('supplier_list'),
                    'static_path': 'mainapp/svg/supplier.svg',
                })
            case 'contract':
                punkts.append({
                    'name': p,
                    'title': 'Договора поставок',
                    'url': reverse('contract_list'),
                    'static_path': 'mainapp/svg/contract.svg',
                })
            case 'certificate':
                punkts.append({
                    'name': p,
                    'title': 'Сертификаты качества',
                    'url': reverse('certificate_list'),
                    'static_path': 'mainapp/svg/certificate.svg',
                })
            case 'receipt':
                punkts.append({
                    'name': p,
                    'title': 'Поставки',
                    'url': reverse('receipt_list'),
                    'static_path': 'mainapp/svg/box.svg',
                })
            case 'physic':
                punkts.append({
                    'name': p,
                    'title': 'Клиенты физ.',
                    'url': reverse('physic_list'),
                    'static_path': 'mainapp/svg/client_f.svg',
                })
            case 'legal':
                punkts.append({
                    'name': p,
                    'title': 'Клиенты юр.',
                    'url': reverse('legal_list'),
                    'static_path': 'mainapp/svg/client_u.svg',
                })
            case 'prescription':
                punkts.append({
                    'name': p,
                    'title': 'Рецепты',
                    'url': reverse('prescription_list'),
                    'static_path': 'mainapp/svg/prescription.svg',
                })
            case 'medicine':
                punkts.append({
                    'name': p,
                    'title': 'Каталог препаратов',
                    'url': reverse('medicine_list'),
                    'static_path': 'mainapp/svg/medicine.svg',
                })
            case 'med_group':
                punkts.append({
                    'name': p,
                    'title': 'Группы препаратов',
                    'url': reverse('med_group_list'),
                    'static_path': 'mainapp/svg/medicine_group.svg',
                })
            case 'order':
                punkts.append({
                    'name': p,
                    'title': 'Список заказов',
                    'url': reverse('order_list'),
                    'static_path': 'mainapp/svg/order.svg',
                })
            case 'doctor':
                punkts.append({
                    'name': p,
                    'title': 'Реестр врачей',
                    'url': reverse('doctor_list'),
                    'static_path': 'mainapp/svg/doctor.svg',
                })
            case 'facility':
                punkts.append({
                    'name': p,
                    'title': 'Реестр учреждений',
                    'url': reverse('facility_list'),
                    'static_path': 'mainapp/svg/hospital.svg',
                })
    return punkts


def replace_null(dic, row=''):
    ret_dic = {}
    for key in dic.keys():
        if dic[key] == '':
            if key in ['couple-' + row + '-3', 'time_begin', 'time_end']:
                ret_dic[key] = '00:00'
            if key in ['date', 'birth', 'd_passport', 'dn']:
                ret_dic[key] = '1900-01-01'
            if key in ['de']:
                ret_dic[key] = '2045-05-09'
            if key in ['couple-' + row + '-0', 'couple-' + row + '-1', 'hippodrome', 'city', 'owner', 'race', 'horse',
                       'jockey']:
                ret_dic[key] = '-1'
            if key in ['couple-' + row + '-2', 'distance', 'summa', 's_passport', 'n_passport', 'age', 'report']:
                ret_dic[key] = '0'
        else:
            ret_dic[key] = dic[key]
    return ret_dic


def required_presc(v):
    if v:
        return "Требует"
    else:
        return "Не требует"