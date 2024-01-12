from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Index
from django.urls import reverse

class MedicineGroup(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100, verbose_name='Название группы')  # Название группы

    Index(fields=['id', 'group_name'])
    def __str__(self):
        return self.group_name  # Возвращает название группы в админке
    class Meta:
        verbose_name = 'Группа лекарств'
        verbose_name_plural = 'Группы лекарств'
        ordering = ['group_name']
        db_table = 'MedicineGroup'

# Create your models here.
class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Наименование') # Наименование
    article = models.CharField(max_length=100, verbose_name='Артикул')  # Артикул
    photo = models.ImageField(verbose_name='Фото', upload_to='photos/medicine/')  # Фото
    group = models.ForeignKey(MedicineGroup, on_delete=models.SET_NULL, verbose_name='Группа', blank=True, null=True)  # Группа
    expiration_date = models.DateField( verbose_name='Срок годности')  # Срок годности
    storage_conditions = models.TextField(blank=True, verbose_name='Условия хранения')  # Условия хранения
    pre_required = models.BooleanField(default=False, blank=True, verbose_name='Требует рецепта')  # Требует рецепта
    interactions = models.TextField(blank=True, verbose_name='Взаимодействие')  # Взаимодействие
    limitations = models.TextField(blank=True, verbose_name='Ограничения')  # Ограничения
    side_effects = models.TextField(blank=True, verbose_name='Побочные эффекты')  # Побочные эффекты
    usage_instruction = models.TextField(blank=True, verbose_name='Инструкция к применению')  # Инструкция к применению

    Index(fields=['id', 'name', 'article', 'group' ])
    def __str__(self):
        return f"{self.name} ({self.article})" # Возвращает артикул лекарства в админке
    def get_absolute_url(self):
        return reverse('medicine_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Препарат'
        verbose_name_plural = 'Препараты'
        ordering = ['article', 'name']
        db_table = 'Medicine'

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Наименование')  # Наименование
    city = models.CharField(max_length=100, verbose_name='Город')  # Город
    address = models.CharField(max_length=200, verbose_name='Адрес')  # Адрес
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')  # Телефон
    email = models.CharField(max_length=100, blank=True, verbose_name='Электронная почта')  # Электронная почта
    inn = models.CharField(max_length=12, verbose_name='ИНН')  # ИНН
    kpp = models.CharField(max_length=9, verbose_name='КПП')  # КПП
    ogrn = models.CharField(max_length=13, verbose_name='ОГРН')  # ОГРН

    Index(fields=['id', 'name', 'inn', 'kpp', 'ogrn' ])
    def __str__(self):
        return self.name  # Возвращает наименование поставщика в админке
    def get_absolute_url(self):
        return reverse('supplier_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['name']
        db_table = 'Supplier'

class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name='Поставщик')  # Ссылка на модель "Поставщик"
    number = models.IntegerField(verbose_name='Номер', unique=True)  # Номер договора
    delivery_terms = models.TextField(verbose_name='Сроки поставки')  # Сроки поставки
    batch_sizes = models.TextField(verbose_name='Размеры партий')  # Размеры партий
    payment_method = models.TextField(verbose_name='Способ оплаты')  # Способ оплаты
    delivery_conditions = models.TextField(verbose_name='Условия доставки')  # Условия доставки
    start_date = models.DateField(verbose_name='Дата начала')  # Дата начала
    end_date = models.DateField(verbose_name='Дата окончания')  # Дата окончания
    prolongation = models.TextField(blank=True, verbose_name='Возможность пролонгации')  # Возможность пролонгации
    other_conditions = models.TextField(blank=True, verbose_name='Прочие условия сторон')  # Прочие условия сторон
    document_scan = models.FileField( verbose_name='Скан документа', upload_to='photos/contract/')  # Скан документа

    Index(fields=['number', 'supplier'])
    def __str__(self):
        return f"Договор №{self.number}"  # Возвращает информацию о договоре в админке
    def get_absolute_url(self):
        return reverse('contract_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'
        ordering = ['supplier', 'start_date', 'end_date']
        db_table = 'Contract'

class ContractMedicine(models.Model):
    id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')  # Ссылка на модель "Договор"
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, verbose_name='Препарат')  # Ссылка на модель "Лекарство"
    prices = models.TextField( verbose_name='Цены')  # Цены
    discount_conditions = models.TextField(blank=True, null=True, verbose_name='Условия скидок')  # Условия скидок

    Index(fields=['id', 'contract', 'medicine' ])
    def __str__(self):
        return self.medicine.name  # Возвращает информацию о договоре о лекарстве в админке
    class Meta:
        verbose_name = 'Препарат по договору'
        verbose_name_plural = 'Препараты по договорам'
        ordering = ['contract', 'medicine']
        db_table = 'ContractMedicine'

class Certificate(models.Model):
    id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name='Препарат')  # Ссылка на модель "Лекарство"
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Поставщик')  # Ссылка на модель "Поставщик"
    document_scan = models.FileField( verbose_name='Скан документа', upload_to='photos/certificate/')  # Скан документа
    number = models.CharField(max_length=100, verbose_name='Номер')  # Номер
    start_date = models.DateField( verbose_name='Дата начала')  # Дата начала
    end_date = models.DateField( verbose_name='Дата окончания')  # Дата окончания
    certifying_authority = models.TextField( verbose_name='Сертифицирующий орган')  # Сертифицирующий орган

    Index(fields=['id', 'medicine', 'supplier', 'number' ])
    def __str__(self):
        return f"Сертификат №{self.number}, препарат - {self.medicine}, поставщик - {self.supplier}"  # Возвращает информацию о сертификате в админке
    def get_absolute_url(self):
        return reverse('certificate_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
        ordering = ['number', 'supplier', 'medicine']
        db_table = 'Certificate'

class CertificateAttachment(models.Model):
    id = models.AutoField(primary_key=True)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, verbose_name='Сертификат')  # Ссылка на модель "Сертификат"
    document_scan = models.FileField( verbose_name='Скан документа', upload_to='photos/certificate_attachment/')  # Скан документа

    Index(fields=['id', 'certificate' ])
    def __str__(self):
        return f"Приложение № {self.id}, к сертификату - {self.certificate}"  # Возвращает информацию о приложении к сертификату в админке
    class Meta:
        verbose_name = 'Приложение к сертификату'
        verbose_name_plural = 'Приложения к сертификатам'
        ordering = ['certificate']
        db_table = 'CertificateAttachment'

class Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, verbose_name='Договор')  # Ссылка на модель "Договор"
    date = models.DateField( verbose_name='Дата')  # Дата

    Index(fields=['id', 'contract', 'date' ])
    def __str__(self):
        return f"Поставка от {self.date}, по договору {self.contract}"  # Возвращает информацию о поступлении в админке
    def get_absolute_url(self):
        return reverse('receipt_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
        ordering = ['date', 'contract']
        db_table = 'Receipt'

class ReceiptItem(models.Model):
    id = models.AutoField(primary_key=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, verbose_name='Поступление')  # Ссылка на модель "Поступление"
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, verbose_name='Препарат')  # Ссылка на модель "Лекарство"
    quantity = models.IntegerField( verbose_name='Количество')  # Количество
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')  # Цена за единицу

    Index(fields=['receipt', 'medicine' ])
    def __str__(self):
        return self.medicine.name  # Возвращает информацию о составе поступления в админке
    class Meta:
        verbose_name = 'Препарат в поставке'
        verbose_name_plural = 'Препараты в поставках'
        ordering = ['receipt', 'medicine']
        db_table = 'ReceiptItem'

class MedicalFacility(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Название')  # Название
    city = models.CharField(max_length=100, verbose_name='Город')  # Город
    address = models.CharField(max_length=255, verbose_name='Адрес')  # Адрес
    phone = models.CharField(max_length=15, verbose_name='Телефон')  # Телефон
    email = models.EmailField(max_length=100, verbose_name='Электронная почта')  # Электронная почта
    work_schedule = models.CharField(max_length=100, verbose_name='График работы')  # График работы
    profiles = models.CharField(max_length=255, verbose_name='Профили')  # Профили

    Index(fields=['id', 'name'])
    def __str__(self):
        return self.name  # Отображение названия учреждения в админке
    def get_absolute_url(self):
        return reverse('medicalfacility_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Медицинское учреждение'
        verbose_name_plural = 'Медицинские учреждения'
        ordering = ['name', 'city']
        db_table = 'MedicalFacility'

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')  # Фамилия
    first_name = models.CharField(max_length=50, verbose_name='Имя')  # Имя
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество')  # Отчество
    facility = models.ForeignKey(MedicalFacility, on_delete=models.SET_NULL, verbose_name='Учреждение', blank=True, null=True)  # Учреждение
    phone = models.CharField(max_length=15, verbose_name='Телефон')  # Телефон
    specialization = models.CharField(max_length=100, verbose_name='Специализация')  # Специализация
    position = models.CharField(max_length=100, verbose_name='Должность')  # Должность
    work_schedule = models.CharField(max_length=100, verbose_name='График работы')  # График работы

    Index(fields=['id', 'last_name', 'first_name', 'middle_name', 'facility'])
    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.specialization}"  # Отображение врача в админке
    def get_absolute_url(self):
        return reverse('doctor_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ['facility', 'last_name', 'first_name', 'middle_name']
        db_table = 'Doctor'



class PhysicalPerson(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')  # Фамилия
    first_name = models.CharField(max_length=50, verbose_name='Имя')  # Имя
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество')  # Отчество
    city = models.CharField(max_length=100, verbose_name='Город')  # Город
    address = models.CharField(max_length=255, verbose_name='Адрес')  # Адрес
    phone = models.CharField(max_length=15, verbose_name='Телефон')  # Телефон
    birth_date = models.DateField( verbose_name='Дата рождения')  # Дата рождения
    gender = models.BooleanField(default=False, blank=True, verbose_name='Пол (True - женский, False - мужской)')  # Пол (True - женский, False - мужской)
    benefits = models.TextField(blank=True, verbose_name='Предоставляемые льготы')  # Предоставляемые льготы

    Index(fields=['id', 'last_name', 'first_name', 'middle_name' ])
    def __str__(self):
        return f"{self.last_name} {self.first_name}"  # Отображение имени и фамилии лица в админке
    def get_absolute_url(self):
        return reverse('physicalperson_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'
        ordering = ['last_name', 'first_name', 'middle_name']
        db_table = 'PhysicalPerson'

class LegalEntity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Название')  # Название
    inn = models.CharField(max_length=12, verbose_name='ИНН')  # ИНН
    kpp = models.CharField(max_length=9, verbose_name='КПП')  # КПП
    address = models.CharField(max_length=255, verbose_name='Адрес')  # Адрес
    phone = models.CharField(max_length=15, verbose_name='Телефон')  # Телефон
    contact_person = models.CharField(max_length=100, verbose_name='Контактное лицо')  # Контактное лицо
    contact_person_position = models.CharField(max_length=100, verbose_name='Должность контактного лица')  # Должность контактного лица
    discounts = models.TextField(blank=True, verbose_name='Скидки')  # Скидки

    Index(fields=['name', 'id', 'inn', 'kpp' ])
    def __str__(self):
        return self.name  # Отображение названия юридического лица в админке
    def get_absolute_url(self):
        return reverse('legalentity_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'
        ordering = ['name']
        db_table = 'LegalEntity'

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь') # Пользователь
    photo = models.ImageField(blank=True, null=True, verbose_name='Фото', upload_to='photos/profile/', default='')  # Фото
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество')  # Отчество
    position = models.CharField(max_length=100, verbose_name='Должность')  # Должность
    address = models.CharField(max_length=255, verbose_name='Адрес')  # Адрес
    passport = models.CharField(max_length=255, verbose_name='Паспорт')  # Паспорт
    phone = models.CharField(max_length=15, verbose_name='Телефон')  # Телефон

    Index(fields=['user', ])
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        db_table = 'Profile'

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField( verbose_name='Дата')  # Дата
    number = models.IntegerField( verbose_name='Номер', unique=True)  # Номер заказа
    physical_person = models.ForeignKey(PhysicalPerson, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Физическое лицо')  # Физическое лицо
    legal_entity = models.ForeignKey(LegalEntity, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Юридическое лицо')  # Юридическое лицо
    seller = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Продавец')  # Продавец

    Index(fields=['number', 'date', 'physical_person', 'legal_entity', 'seller', ])

    def clean(self):
        if self.physical_person is None and self.legal_entity is None:
            raise ValidationError('Необходимо заполнить либо поле "Физическое лицо", либо "Юридическое лицо"')

    def save(self, *args, **kwargs):
        self.clean()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Заказ №{self.number}"  # Отображение названия юридического лица в админке
    def get_absolute_url(self):
        return reverse('order_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['date', 'physical_person', 'legal_entity', 'seller']
        db_table = 'Order'

class OrderComposition(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')  # Заказ
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, verbose_name='Препарат')  # Лекарство
    price = models.FloatField( verbose_name='Цена')  # Цена
    quantity = models.IntegerField( verbose_name='Количество')  # Количество

    Index(fields=['order', 'medicine' ])
    def __str__(self):
        return f"{self.medicine.name} - {self.quantity}шт. - {self.price}р."
    class Meta:
        verbose_name = 'Препарат в заказе'
        verbose_name_plural = 'Препараты в заказах'
        ordering = ['order', 'medicine']
        db_table = 'OrderComposition'

class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=100, verbose_name='Номер')  # Номер
    physical_person = models.ForeignKey(PhysicalPerson, on_delete=models.CASCADE, verbose_name='Физическое лицо')  # Физическое лицо
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')  # Врач
    status = models.CharField(max_length=100, verbose_name='Статус')  # Статус
    prescription_date = models.DateField( verbose_name='Дата рецепта')  # Дата выписки рецепта
    pharmacy_visit_date = models.DateField( verbose_name='Дата обращения')  # Дата обращения в аптеку
    document_scan = models.FileField( verbose_name='Скан документа', upload_to='photos/prescription/')  # Скан документа

    Index(fields=['id', 'number', 'physical_person'])
    def __str__(self):
        return f"Рецепт №{self.number} от {self.prescription_date}, Врач - {self.doctor.__str__()}"
    def get_absolute_url(self):
        return reverse('prescription_list', args=[str(self.id)])
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['number', 'physical_person']
        db_table = 'Prescription'

class PrescComposition(models.Model):
    id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, verbose_name='Рецепт')  # Физическое лицо
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name='Препарат')  # Лекарство
    dosage = models.CharField(max_length=255, verbose_name='Дозировка')  # Дозировка

    Index(fields=['id', 'prescription'])
    class Meta:
        verbose_name = 'Состав рецепта'
        verbose_name_plural = 'Составы рецептов'
        db_table = 'PrescComposition'