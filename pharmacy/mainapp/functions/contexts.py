from django.urls import reverse

from .geters import get_side_menu, get_FIO, get_title_select, get_obj_select, \
    get_bread_crumbs, get_user_permissions
from ..models import Profile


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