from models import *
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


def get_default_context(punkt_selected='', user=None):
    prf = Profile.objects.get(user_id=user.id)
    admin = user.is_superuser
    return {
        'user': {'fio': user.last_name+' '+user.first_name[0].upper()+'.'+prf.middle_name[0].upper()+'.',
                 'job': prf.position,
                 },
        'sidebar': punkt_selected != 'login',
        'side_menu': get_side_menu(user),
        'side_menu': [
            {'name': 0, 'title': "Заглавная", 'url_name': 'races_list'},
            {'name': 1, 'title': "Список лошадей", 'url_name': 'horses_list'},
            {'name': 2, 'title': "Список жокеев", 'url_name': 'jockeys_list'},
            {'name': 3, 'title': "Список владельцев", 'url_name': 'owners_list'},
            {'name': 4, 'title': "Список печати", 'url_name': 'reports_list'},
        ],
        'punkt_selected': -1,
        'is_admin': admin,
        'list_v': [],
    }

def get_side_menu(usr):
    pmsns = usr.user_permissions.all()
    punkts = []
    if usr.is_superuser:
        punkts.append({
            'name': 'settings',
            'title': 'Панель администратора',
            'url': reverse('admin:index'),
            'static_path': 'mainapp/svg/settings.svg',
        })
    for p in pmsns:
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


# def get_self_account(_request):
#     profile = Profile.objects.filter(user=_request.user.id)
#     if profile.exists():
#         if Owner.objects.filter(user=profile[0].id).exists():
#             return reverse('owner_id', args=[Owner.objects.get(user=profile[0].id).id])
#         if Jockey.objects.filter(user=profile[0].id).exists():
#             return reverse('jockey_id', args=[Jockey.objects.get(user=profile[0].id).id])
#     return '#'


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

#
# def save_user(d, record, obj):
#     acc = obj.objects.get(id=record)
#     prof = Profile.objects.get(id=acc.user.id)
#     usr = User.objects.get(id=prof.user.id)
#
#     dic = replace_null(d.POST)
#
#     prof.s_passport = int(dic['s_passport'])
#     prof.n_passport = int(dic['n_passport'])
#     usr.first_name = dic['first_name']
#     usr.last_name = dic['last_name']
#     usr.email = dic['email']
#     prof.middle_name = dic['middle_name']
#     prof.phone = dic['phone']
#     prof.w_passport = dic['w_passport']
#     prof.city = City.objects.get(id=int(dic['city']))
#     prof.birth = datetime.strptime(dic['birth'], "%Y-%m-%d").date()
#     prof.d_passport = datetime.strptime(dic['d_passport'], "%Y-%m-%d").date()
#     if obj == Jockey:
#         acc.category = dic['category']
#
#     if d.FILES:
#         if prof.photo:
#             prof.photo.delete(False)
#         file = d.FILES['photo']
#         fs = FileSystemStorage()
#         filename = fs.save(
#             'photos/user/' + datetime.now().year.__str__() + '/' + datetime.now().month.__str__() + '/' + datetime.now().day.__str__() + '/' + file.name,
#             file)
#         prof.photo = filename
#
#     acc.save()
#     prof.save()
#     usr.save()
#
#     return acc.id
