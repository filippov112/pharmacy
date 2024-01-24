from _decimal import Decimal


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
        case 'IntegerField':
            return int(val)
        case 'DecimalField':
            return Decimal(val)
        case 'FloatField':
            return float(val)
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