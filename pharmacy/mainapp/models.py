from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Index
from django.urls import reverse


class MedicineGroup(models.Model):
    id              = models.AutoField(primary_key=True)
    group_name      = models.CharField(blank=True, max_length=100, verbose_name='Название группы', default='')  # Название группы

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
    id                  = models.AutoField(primary_key=True)
    name                = models.CharField(max_length=100, verbose_name='Наименование', default='')  # Наименование
    article             = models.CharField(max_length=100, verbose_name='Артикул', default='')  # Артикул
    photo               = models.ImageField(verbose_name='Фото', upload_to='photos/medicine/%Y/%m/%d/', blank=True, null=True)  # Фото
    group               = models.ForeignKey(MedicineGroup, on_delete=models.SET_NULL, verbose_name='Группа', blank=True, null=True)  # Группа
    expiration_date     = models.DateField(verbose_name='Срок годности', auto_now_add=True)  # Срок годности
    storage_conditions  = models.TextField(blank=True, verbose_name='Условия хранения', default='')  # Условия хранения
    interactions        = models.TextField(blank=True, verbose_name='Взаимодействие', default='')  # Взаимодействие
    limitations         = models.TextField(blank=True, verbose_name='Ограничения', default='')  # Ограничения
    side_effects        = models.TextField(blank=True, verbose_name='Побочные эффекты', default='')  # Побочные эффекты
    usage_instruction   = models.TextField(blank=True, verbose_name='Инструкция к применению', default='')  # Инструкция к применению

    Index(fields=['id', 'name', 'article', 'group'])

    def __str__(self):
        return f"{self.name} ({self.article})"  # Возвращает артикул лекарства в админке

    def get_absolute_url(self):
        return reverse('medicine_list', args=[str(self.id)])

    class Meta:
        verbose_name = 'Препарат'
        verbose_name_plural = 'Препараты'
        ordering = ['article', 'name']
        db_table = 'Medicine'


class Supplier(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(blank=True, max_length=100, verbose_name='Наименование', default='')  # Наименование
    city        = models.CharField(blank=True, max_length=100, verbose_name='Город', default='')  # Город
    address     = models.CharField(blank=True, max_length=200, verbose_name='Адрес', default='')  # Адрес
    phone       = models.CharField(max_length=20, blank=True, verbose_name='Телефон', default='')  # Телефон
    email       = models.CharField(max_length=100, blank=True, verbose_name='Электронная почта', default='')  # Электронная почта
    inn         = models.CharField(blank=True, max_length=12, verbose_name='ИНН', default='')  # ИНН
    kpp         = models.CharField(blank=True, max_length=9, verbose_name='КПП', default='')  # КПП
    ogrn        = models.CharField(blank=True, max_length=13, verbose_name='ОГРН', default='')  # ОГРН

    Index(fields=['id', 'name', 'inn', 'kpp', 'ogrn'])

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
    id                      = models.AutoField(primary_key=True)
    document_scan           = models.FileField(blank=True, null=True, verbose_name='Скан документа', upload_to='photos/contract/%Y/%m/%d/')  # Скан документа
    supplier                = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Поставщик')  # Ссылка на модель "Поставщик"
    number                  = models.IntegerField(blank=True, default=0, verbose_name='Номер')  # Номер договора
    start_date              = models.DateField(blank=True, verbose_name='Дата начала', auto_now_add=True)  # Дата начала
    end_date                = models.DateField(blank=True, verbose_name='Дата окончания', auto_now_add=True)  # Дата окончания
    delivery_terms          = models.TextField(blank=True, verbose_name='Сроки поставки', default='')  # Сроки поставки
    batch_sizes             = models.TextField(blank=True, verbose_name='Размеры партий', default='')  # Размеры партий
    payment_method          = models.TextField(blank=True, verbose_name='Способ оплаты', default='')  # Способ оплаты
    delivery_conditions     = models.TextField(blank=True, verbose_name='Условия доставки', default='')  # Условия доставки
    prolongation            = models.TextField(blank=True, verbose_name='Возможность пролонгации', default='')  # Возможность пролонгации
    other_conditions        = models.TextField(blank=True, verbose_name='Прочие условия сторон', default='')  # Прочие условия сторон

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
    id                      = models.AutoField(primary_key=True)
    contract                = models.ForeignKey(Contract, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Договор')  # Ссылка на модель "Договор"
    medicine                = models.ForeignKey(Medicine, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Препарат')  # Ссылка на модель "Лекарство"
    prices                  = models.TextField(blank=True, default='', verbose_name='Цены')  # Цены
    discount_conditions     = models.TextField(blank=True, default='', verbose_name='Условия скидок')  # Условия скидок

    Index(fields=['id', 'contract', 'medicine'])

    def __str__(self):
        return self.medicine.name  # Возвращает информацию о договоре о лекарстве в админке

    class Meta:
        verbose_name = 'Препарат по договору'
        verbose_name_plural = 'Препараты по договорам'
        ordering = ['contract', 'medicine']
        db_table = 'ContractMedicine'


class Certificate(models.Model):
    id                      = models.AutoField(primary_key=True)
    medicine                = models.ForeignKey(Medicine, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Препарат')  # Ссылка на модель "Лекарство"
    supplier                = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Поставщик')  # Ссылка на модель "Поставщик"
    document_scan           = models.FileField(blank=True, null=True, verbose_name='Скан документа', upload_to='photos/certificate/%Y/%m/%d/')  # Скан документа
    number                  = models.CharField(blank=True, max_length=100, verbose_name='Номер', default='')  # Номер
    start_date              = models.DateField(blank=True,  verbose_name='Дата начала', auto_now_add=True)  # Дата начала
    end_date                = models.DateField(blank=True,  verbose_name='Дата окончания', auto_now_add=True)  # Дата окончания
    certifying_authority    = models.TextField(blank=True, default='', verbose_name='Сертифицирующий орган')  # Сертифицирующий орган

    Index(fields=['id', 'medicine', 'supplier', 'number'])

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
    id                  = models.AutoField(primary_key=True)
    certificate         = models.ForeignKey(Certificate, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Сертификат')  # Ссылка на модель "Сертификат"
    document_scan       = models.FileField(blank=True, null=True, verbose_name='Скан документа', upload_to='photos/certificate_attachment/%Y/%m/%d/')  # Скан документа

    Index(fields=['id', 'certificate'])

    def __str__(self):
        return f"Приложение № {self.id}, к сертификату - {self.certificate}"  # Возвращает информацию о приложении к сертификату в админке

    class Meta:
        verbose_name = 'Приложение к сертификату'
        verbose_name_plural = 'Приложения к сертификатам'
        ordering = ['certificate']
        db_table = 'CertificateAttachment'


class Receipt(models.Model):
    id          = models.AutoField(primary_key=True)
    contract    = models.ForeignKey(Contract, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Договор')  # Ссылка на модель "Договор"
    date        = models.DateField(blank=True, auto_now_add=True, verbose_name='Дата')  # Дата

    Index(fields=['id', 'contract', 'date'])

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
    id              = models.AutoField(primary_key=True)
    receipt         = models.ForeignKey(Receipt, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Поступление')  # Ссылка на модель "Поступление"
    medicine        = models.ForeignKey(Medicine, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Препарат')  # Ссылка на модель "Лекарство"
    quantity        = models.IntegerField(blank=True, default=0, verbose_name='Количество')  # Количество
    unit_price      = models.DecimalField(blank=True, default=0, max_digits=10, decimal_places=2, verbose_name='Цена за единицу')  # Цена за единицу

    Index(fields=['receipt', 'medicine'])

    def __str__(self):
        return self.medicine.name  # Возвращает информацию о составе поступления в админке

    class Meta:
        verbose_name = 'Препарат в поставке'
        verbose_name_plural = 'Препараты в поставках'
        ordering = ['receipt', 'medicine']
        db_table = 'ReceiptItem'


class MedicalFacility(models.Model):
    id              = models.AutoField(primary_key=True)
    name            = models.CharField(blank=True, max_length=100, verbose_name='Название', default='')  # Название
    city            = models.CharField(blank=True, max_length=100, verbose_name='Город', default='')  # Город
    address         = models.CharField(blank=True, max_length=255, verbose_name='Адрес', default='')  # Адрес
    phone           = models.CharField(blank=True, max_length=15, verbose_name='Телефон', default='')  # Телефон
    email           = models.CharField(blank=True, max_length=100, verbose_name='Электронная почта', default='')  # Электронная почта
    work_schedule   = models.CharField(blank=True, max_length=100, verbose_name='График работы', default='')  # График работы
    profiles        = models.CharField(blank=True, max_length=255, verbose_name='Профили', default='')  # Профили

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
    id                  = models.AutoField(primary_key=True)
    facility            = models.ForeignKey(MedicalFacility, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Учреждение')  # Учреждение
    last_name           = models.CharField(blank=True, default='', max_length=50, verbose_name='Фамилия')  # Фамилия
    first_name          = models.CharField(blank=True, default='', max_length=50, verbose_name='Имя')  # Имя
    middle_name         = models.CharField(blank=True, default='', max_length=50, verbose_name='Отчество')  # Отчество
    phone               = models.CharField(blank=True, default='', max_length=15, verbose_name='Телефон')  # Телефон
    specialization      = models.CharField(blank=True, default='', max_length=100, verbose_name='Специализация')  # Специализация
    position            = models.CharField(blank=True, default='', max_length=100, verbose_name='Должность')  # Должность
    work_schedule       = models.CharField(blank=True, default='', max_length=100, verbose_name='График работы')  # График работы

    Index(fields=['id', 'last_name', 'first_name', 'middle_name', 'facility'])

    @staticmethod
    def fio(last_name, first_name, middle_name):
        formatted_name = last_name.capitalize() if last_name else ''
        if first_name and len(first_name) > 0:
            formatted_name += ' ' + first_name[0].upper() + '.' if formatted_name else first_name[0] + '.'
        if middle_name and len(middle_name) > 0:
            formatted_name += ' ' + middle_name[0].upper() + '.' if formatted_name else middle_name[0] + '.'
        return formatted_name

    def __str__(self):
        ln = self.last_name if self.last_name else ''
        fn = self.first_name if self.first_name else ''
        mn = self.middle_name if self.middle_name else ''
        return self.fio(ln, fn, mn)

    def get_absolute_url(self):
        return reverse('doctor_list', args=[str(self.id)])

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ['facility', 'last_name', 'first_name', 'middle_name']
        db_table = 'Doctor'


class PhysicalPerson(models.Model):
    id              = models.AutoField(primary_key=True)
    last_name       = models.CharField(blank=True, default='', max_length=50, verbose_name='Фамилия')  # Фамилия
    first_name      = models.CharField(blank=True, default='', max_length=50, verbose_name='Имя')  # Имя
    middle_name     = models.CharField(blank=True, default='', max_length=50, verbose_name='Отчество')  # Отчество
    city            = models.CharField(blank=True, default='', max_length=100, verbose_name='Город')  # Город
    address         = models.CharField(blank=True, default='', max_length=255, verbose_name='Адрес')  # Адрес
    phone           = models.CharField(blank=True, default='', max_length=15, verbose_name='Телефон')  # Телефон
    birth_date      = models.DateField(blank=True, auto_now_add=True, verbose_name='Дата рождения')  # Дата рождения
    benefits        = models.TextField(blank=True, default='', verbose_name='Предоставляемые льготы')  # Предоставляемые льготы

    Index(fields=['id', 'last_name', 'first_name', 'middle_name'])

    @staticmethod
    def fio(last_name, first_name, middle_name):
        formatted_name = last_name.capitalize() if last_name else ''
        if first_name and len(first_name) > 0:
            formatted_name += ' ' + first_name[0].upper() + '.' if formatted_name else first_name[0] + '.'
        if middle_name and len(middle_name) > 0:
            formatted_name += ' ' + middle_name[0].upper() + '.' if formatted_name else middle_name[0] + '.'
        return formatted_name

    def __str__(self):
        ln = self.last_name if self.last_name else ''
        fn = self.first_name if self.first_name else ''
        mn = self.middle_name if self.middle_name else ''
        return self.fio(ln, fn, mn)

    def get_absolute_url(self):
        return reverse('physicalperson_list', args=[str(self.id)])

    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'
        ordering = ['last_name', 'first_name', 'middle_name']
        db_table = 'PhysicalPerson'


class LegalEntity(models.Model):
    id                      = models.AutoField(primary_key=True)
    name                    = models.CharField(blank=True, default='', max_length=100, verbose_name='Название')  # Название
    inn                     = models.CharField(blank=True, default='', max_length=12, verbose_name='ИНН')  # ИНН
    kpp                     = models.CharField(blank=True, default='', max_length=9, verbose_name='КПП')  # КПП
    address                 = models.CharField(blank=True, default='', max_length=255, verbose_name='Адрес')  # Адрес
    phone                   = models.CharField(blank=True, default='', max_length=15, verbose_name='Телефон')  # Телефон
    contact_person          = models.CharField(blank=True, default='', max_length=100, verbose_name='Контактное лицо')  # Контактное лицо
    contact_person_position = models.CharField(blank=True, default='', max_length=100, verbose_name='Должность контактного лица')  # Должность контактного лица
    discounts               = models.TextField(blank=True, default='', verbose_name='Скидки')  # Скидки

    Index(fields=['name', 'id', 'inn', 'kpp'])

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
    id              = models.AutoField(primary_key=True)
    user            = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')  # Пользователь
    photo           = models.ImageField(blank=True, null=True, verbose_name='Фото', upload_to='photos/profile/%Y/%m/%d/', default='')  # Фото
    middle_name     = models.CharField(blank=True, default='', max_length=50, verbose_name='Отчество')  # Отчество
    position        = models.CharField(blank=True, default='', max_length=100, verbose_name='Должность')  # Должность
    address         = models.CharField(blank=True, default='', max_length=255, verbose_name='Адрес')  # Адрес
    passport        = models.CharField(blank=True, default='', max_length=255, verbose_name='Паспорт')  # Паспорт
    phone           = models.CharField(blank=True, default='', max_length=15, verbose_name='Телефон')  # Телефон

    Index(fields=['user', ])

    @staticmethod
    def fio(last_name, first_name, middle_name):
        formatted_name = last_name.capitalize() if last_name else ''
        if first_name and len(first_name) > 0:
            formatted_name += ' ' + first_name[0].upper() + '.' if formatted_name else first_name[0] + '.'
        if middle_name and len(middle_name) > 0:
            formatted_name += ' ' + middle_name[0].upper() + '.' if formatted_name else middle_name[0] + '.'
        return formatted_name

    def __str__(self):
        ln = self.user.last_name if self.user.last_name else ''
        fn = self.user.first_name if self.user.first_name else ''
        mn = self.middle_name if self.middle_name else ''
        return self.fio(ln, fn, mn)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        db_table = 'Profile'


class Order(models.Model):
    id                  = models.AutoField(primary_key=True)
    physical_person     = models.ForeignKey(PhysicalPerson, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Физическое лицо')  # Физическое лицо
    legal_entity        = models.ForeignKey(LegalEntity, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Юридическое лицо')  # Юридическое лицо
    seller              = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Продавец')  # Продавец
    date                = models.DateField(blank=True, auto_now_add=True, verbose_name='Дата')  # Дата
    number              = models.IntegerField(blank=True, default=0, verbose_name='Номер', unique=True)  # Номер заказа


    Index(fields=['number', 'date', 'physical_person', 'legal_entity', 'seller', ])

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
    id              = models.AutoField(primary_key=True)
    order           = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Заказ')  # Заказ
    medicine        = models.ForeignKey(Medicine, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Препарат')  # Лекарство
    price           = models.FloatField(blank=True, default=0, verbose_name='Цена')  # Цена
    quantity        = models.IntegerField(blank=True, default=0, verbose_name='Количество')  # Количество

    Index(fields=['order', 'medicine'])

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity}шт. - {self.price}р."

    class Meta:
        verbose_name = 'Препарат в заказе'
        verbose_name_plural = 'Препараты в заказах'
        ordering = ['order', 'medicine']
        db_table = 'OrderComposition'


class Prescription(models.Model):
    id                      = models.AutoField(primary_key=True)
    document_scan           = models.FileField(blank=True, null=True, verbose_name='Скан документа', upload_to='photos/prescription/%Y/%m/%d/')  # Скан документа
    physical_person         = models.ForeignKey(PhysicalPerson, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Физическое лицо')  # Физическое лицо
    doctor                  = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Врач')  # Врач
    prescription_date       = models.DateField(blank=True, auto_now_add=True, verbose_name='Дата рецепта')  # Дата выписки рецепта
    pharmacy_visit_date     = models.DateField(blank=True, auto_now_add=True, verbose_name='Дата обращения')  # Дата обращения в аптеку
    number                  = models.CharField(blank=True, default='', max_length=100, verbose_name='Номер')  # Номер
    status                  = models.CharField(blank=True, default='', max_length=100, verbose_name='Статус')  # Статус

    Index(fields=['id', 'number', 'physical_person'])

    def __str__(self):
        return f"Рецепт №{self.number} от {self.prescription_date}, Врач - {str(self.doctor)}"

    def get_absolute_url(self):
        return reverse('prescription_list', args=[str(self.id)])

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['number', 'physical_person']
        db_table = 'Prescription'


class PrescComposition(models.Model):
    id              = models.AutoField(primary_key=True)
    prescription    = models.ForeignKey(Prescription, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Рецепт')  # Физическое лицо
    medicine        = models.ForeignKey(Medicine, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Препарат')  # Лекарство
    dosage          = models.CharField(blank=True, default='', max_length=255, verbose_name='Дозировка')  # Дозировка

    Index(fields=['id', 'prescription'])

    class Meta:
        verbose_name = 'Состав рецепта'
        verbose_name_plural = 'Составы рецептов'
        db_table = 'PrescComposition'
