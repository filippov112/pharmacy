from django.urls import reverse
from ..models import Medicine, LegalEntity, PhysicalPerson, Doctor, MedicalFacility, \
    MedicineGroup, Contract, Supplier, Profile

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

    perms = ['reports'] + perms
    for p in perms:
        match p:
            case 'reports':
                tasks.append({
                    'name': 'reports',
                    'title': 'Отчетные формы',
                    'url': reverse('report_list'),
                    'static_path': 'mainapp/svg/reports.svg',
                })
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