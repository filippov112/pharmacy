from _decimal import Decimal
from datetime import datetime


def replace_null(o, field, val):
    f = o._meta.get_field(field)
    field_type = f.get_internal_type()
    match field_type:
        case 'FileField'|'ImageField':
            return None
        case 'ForeignKey'|'OneToOneField':
            rem_m = f.remote_field.model
            return rem_m.objects.get(id=val) if val else None
        case 'IntegerField':
            return int(val) if val else 0
        case 'DecimalField':
            return Decimal(val) if val else 0
        case 'FloatField':
            return float(val) if val else 0
        case 'DateField':
            return datetime.strptime(val, '%Y-%m-%d') if val else datetime(1900, 1, 1, 0, 0, 0)
    return val


def default_val(o, field, val, is_link=False, is_date=False):
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
            if is_date:
                return datetime.strptime(val, '%Y-%m-%d') if val else datetime(1900, 1, 1, 0, 0, 0)
            else:
                return str(val) if val else ''
        case 'IntegerField':
            return int(val) if val else 0
        case 'DecimalField':
            return Decimal(val) if val else 0
        case 'FloatField':
            return float(val) if val else 0
        case 'TextField'|'CharField':
            return val if val else ''
    return val


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