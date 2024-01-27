from django.db.models import ManyToOneRel, ManyToManyRel

from .utils import replace_null
from ..models import CertificateAttachment, ContractMedicine, ReceiptItem, OrderComposition, \
    PrescComposition


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


def clear_files(model, obj_list):
    field_names = [
        field.name for field in model._meta.get_fields()
        if not (field.auto_created and isinstance(field, (ManyToOneRel, ManyToManyRel)))
    ]
    for obj in obj_list:
        for f in field_names:
            if model._meta.get_field(f).get_internal_type() in ('ImageField', 'FileField'):
                field = getattr(obj, f)
                if field:
                    field.delete(False)


class MyClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def set_empty_object(model):
    field_names = [
        field.name for field in model._meta.get_fields()
        if not (field.auto_created and isinstance(field, (ManyToOneRel, ManyToManyRel)))
    ]
    obj = {}
    for name in field_names:
        obj[name] = None
    obj = MyClass(**obj)
    return obj


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
        ob = o.objects.create(**obj_record)

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
                    field = getattr(ob, field_name)
                    if field:
                        field.delete(False)
                    field.save(file.name, file)

    # Почистим записи сторонних таблиц, прежде чем добавлять измененные (кроме файлов для сертификатов)
    for table_name in side_table_names.keys():
        o = get_object(table_name)
        rec = {o['fk']:ob.id}
        objs_delete = o['obj'].objects.filter(**rec)
        if len(fsr) > 0:
            objs_delete = objs_delete.exclude(id__in=fsr)
        clear_files(o['obj'], objs_delete)
        objs_delete.delete()

    # Пробросим новые сторонние записи
    for table_name in ls_tables.keys():
        o = get_object(table_name)
        for rec in ls_tables[table_name].keys():
            r_dic = { o['fk']:ob, }
            for f in ls_tables[table_name][rec].keys():
                v = replace_null(o['obj'], f, ls_tables[table_name][rec][f])
                if v:
                    r_dic[f] = v
            if len(r_dic.keys()) > 1:
                o['obj'].objects.create(**r_dic)

    # Сохраним файлы сертификатов
    for table_name in mFiles.keys():
        o = get_object(table_name)
        for rec in mFiles[table_name].keys():
            for f in mFiles[table_name][rec].keys():
                file = mFiles[table_name][rec][f]
                if file:
                    r_dic = {o['fk']: ob, }
                    obj = o['obj'].objects.create(**r_dic)
                    getattr(obj, f).save(file.name, file)

    return ob.id