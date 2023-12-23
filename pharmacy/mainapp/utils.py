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


# def get_default_context(request, record=-1):
#     return {
#         'add_record': 'owner_new',
#         'self_account': get_self_account(request),
#         'side_menu': [
#             {'pk': 0, 'title': "Заглавная", 'url_name': 'races_list'},
#             {'pk': 1, 'title': "Список лошадей", 'url_name': 'horses_list'},
#             {'pk': 2, 'title': "Список жокеев", 'url_name': 'jockeys_list'},
#             {'pk': 3, 'title': "Список владельцев", 'url_name': 'owners_list'},
#             {'pk': 4, 'title': "Список печати", 'url_name': 'reports_list'},
#         ],
#         'rule_edit': request.user.id == record or request.user.is_superuser,
#         'punkt_selected': -1,
#         'is_login': request.user.is_authenticated,
#         'is_admin': request.user.is_superuser,
#         'list_v': [],
#         'photo': '',
#     }


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
