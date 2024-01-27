from django.db.models import ManyToOneRel, ManyToManyRel

from .commons import *


@permission_required('mainapp.view_medicine', raise_exception=True)
@login_required(login_url=login_view)
def medicine_id(request, record):
    error = ''
    o = Medicine
    n = 'medicine'
    fn = 'medicine'

    ob = o.objects.get(id=record)
    if request.method == 'POST' and check_user_rules(request.user, 'delete_'+fn):
        try:
            ob.delete()
            return redirect(n + '_list')
        except IntegrityError as e:
            error = 'Существуют связанные записи: '+ ', '.join([str(x) for x in (e.protected_objects if e.protected_objects else [])])

    default_context = get_default_context(n, user=request.user, title=str(ob), error=error)
    view_context = get_view_context(n, record, ob, fn, request.user)
    custom_context = {
        'task': 'view',
        # Фото, Артикул, Название, Группа, Срок, Условия хранения, Взаимодействие, Ограничения, Побочные эффекты, Инструкция
        'content_view': [
            {'type': 'image', 'link': ob.photo.url if ob.photo else '', 'title': '', 'text': ''},
            {'type': 'text', 'link': '', 'title': 'Артикул', 'text': ob.article},
            {'type': 'text', 'link': '', 'title': 'Наименование', 'text': ob.name},
            {'type': 'link', 'link': get_link('med_group_id', ob.group), 'title': 'Лекарственная группа', 'text': default_val(o, 'group', ob.group)},
            {'type': 'text', 'link': '', 'title': 'Срок годности (лет)', 'text': ob.expiration_date},
            {'type': 'text', 'link': '', 'title': 'Условия хранения', 'text': ob.storage_conditions},
            {'type': 'text', 'link': '', 'title': 'Взаимодействие с другими лекарствами', 'text': ob.interactions},
            {'type': 'text', 'link': '', 'title': 'Ограничения', 'text': ob.limitations},
            {'type': 'text', 'link': '', 'title': 'Побочные эффекты', 'text': ob.side_effects},
            {'type': 'text', 'link': '', 'title': 'Инструкция к применению', 'text': ob.usage_instruction},
        ],
    }
    return render(request, 'mainapp/simple_view_edit.html', default_context | view_context | custom_context)