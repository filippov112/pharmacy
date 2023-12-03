from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100)  # Название группы

    def __str__(self):
        return self.group_name  # Возвращает название группы в админке

# Create your models here.
class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100) # Наименование
    article = models.CharField(max_length=100)  # Артикул
    photo = models.CharField(max_length=200)  # Артикул
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # Группа
    expiration_date = models.DateField()  # Срок годности
    storage_conditions = models.TextField(blank=True)  # Условия хранения
    prescription_required = models.BooleanField(default=False, blank=True)  # Требует рецепта
    interactions = models.TextField(blank=True)  # Взаимодействие
    limitations = models.TextField(blank=True)  # Ограничения
    side_effects = models.TextField(blank=True)  # Побочные эффекты
    usage_instruction = models.TextField(blank=True)  # Инструкция к применению

    def __str__(self):
        return f"{self.name} ({self.article})" # Возвращает артикул лекарства в админке

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Наименование
    city = models.CharField(max_length=100)  # Город
    address = models.CharField(max_length=200)  # Адрес
    phone = models.CharField(max_length=20, blank=True)  # Телефон
    email = models.EmailField(max_length=100, blank=True)  # Электронная почта
    inn = models.CharField(max_length=12)  # ИНН
    kpp = models.CharField(max_length=9)  # КПП
    ogrn = models.CharField(max_length=13)  # ОГРН

    def __str__(self):
        return self.name  # Возвращает наименование поставщика в админке

class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)  # Ссылка на модель "Поставщик"
    delivery_terms = models.TextField()  # Сроки поставки
    batch_sizes = models.TextField()  # Размеры партий
    payment_method = models.TextField()  # Способ оплаты
    delivery_conditions = models.TextField()  # Условия доставки
    start_date = models.DateField()  # Дата начала
    end_date = models.DateField()  # Дата окончания
    prolongation = models.TextField(blank=True)  # Возможность пролонгации
    other_conditions = models.TextField(blank=True)  # Прочие условия сторон
    document_scan = models.TextField()  # Скан документа

    def __str__(self):
        return f"Contract with {self.supplier} starting from {self.start_date}"  # Возвращает информацию о договоре в админке

class ContractMedicine(models.Model):
    id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)  # Ссылка на модель "Договор"
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)  # Ссылка на модель "Лекарство"
    prices = models.TextField()  # Цены
    discount_conditions = models.TextField(blank=True, null=True)  # Условия скидок

    def __str__(self):
        return self.medicine.name  # Возвращает информацию о договоре о лекарстве в админке

class Certificate(models.Model):
    id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)  # Ссылка на модель "Лекарство"
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)  # Ссылка на модель "Поставщик"
    document_scan = models.TextField()  # Скан документа
    number = models.CharField(max_length=100)  # Номер
    start_date = models.DateField()  # Дата начала
    end_date = models.DateField()  # Дата окончания
    certifying_authority = models.TextField()  # Сертифицирующий орган

    def __str__(self):
        return f"Certificate for {self.medicine} from {self.supplier}"  # Возвращает информацию о сертификате в админке

class CertificateAttachment(models.Model):
    id = models.AutoField(primary_key=True)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)  # Ссылка на модель "Сертификат"
    document_scan = models.TextField()  # Скан документа

    def __str__(self):
        return f"Attachment {self.id} for {self.certificate}"  # Возвращает информацию о приложении к сертификату в админке

class Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)  # Ссылка на модель "Поставщик"
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)  # Ссылка на модель "Договор"
    date = models.DateField()  # Дата

    def __str__(self):
        return f"Receipt for {self.date} from {self.supplier}"  # Возвращает информацию о поступлении в админке

class ReceiptItem(models.Model):
    id = models.AutoField(primary_key=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)  # Ссылка на модель "Поступление"
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)  # Ссылка на модель "Лекарство"
    quantity = models.IntegerField()  # Количество
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена за единицу

    def __str__(self):
        return self.medicine.name  # Возвращает информацию о составе поступления в админке

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)  # Фамилия
    first_name = models.CharField(max_length=50)  # Имя
    middle_name = models.CharField(max_length=50, blank=True)  # Отчество
    phone = models.CharField(max_length=15)  # Телефон
    specialization = models.CharField(max_length=100)  # Специализация
    position = models.CharField(max_length=100)  # Должность
    work_schedule = models.CharField(max_length=100)  # График работы

    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.specialization}"  # Отображение врача в админке

class MedicalFacility(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Название
    city = models.CharField(max_length=100)  # Город
    address = models.CharField(max_length=255)  # Адрес
    phone = models.CharField(max_length=15)  # Телефон
    email = models.EmailField(max_length=100)  # Электронная почта
    work_schedule = models.CharField(max_length=100)  # График работы
    profiles = models.CharField(max_length=255)  # Профили

    def __str__(self):
        return self.name  # Отображение названия учреждения в админке

class PhysicalPerson(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)  # Фамилия
    first_name = models.CharField(max_length=50)  # Имя
    middle_name = models.CharField(max_length=50, blank=True)  # Отчество
    city = models.CharField(max_length=100)  # Город
    address = models.CharField(max_length=255)  # Адрес
    phone = models.CharField(max_length=15)  # Телефон
    birth_date = models.DateField()  # Дата рождения
    gender = models.BooleanField(default=False, blank=True)  # Пол (True - женский, False - мужской)
    benefits = models.TextField(blank=True)  # Предоставляемые льготы

    def __str__(self):
        return f"{self.last_name} {self.first_name}"  # Отображение имени и фамилии лица в админке

class LegalEntity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Название
    inn = models.CharField(max_length=12)  # ИНН
    kpp = models.CharField(max_length=9)  # КПП
    address = models.CharField(max_length=255)  # Адрес
    phone = models.CharField(max_length=15)  # Телефон
    contact_person = models.CharField(max_length=100)  # Контактное лицо
    contact_person_position = models.CharField(max_length=100)  # Должность контактного лица
    discounts = models.TextField(blank=True)  # Скидки

    def __str__(self):
        return self.name  # Отображение названия юридического лица в админке

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.TextField(blank=True, null=True)  # Фото
    middle_name = models.CharField(max_length=50, blank=True)  # Отчество
    position = models.CharField(max_length=100)  # Должность
    address = models.CharField(max_length=255)  # Адрес
    passport = models.CharField(max_length=255)  # Паспорт
    phone = models.CharField(max_length=15)  # Телефон

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()  # Дата
    physical_person = models.ForeignKey(PhysicalPerson, on_delete=models.SET_NULL, blank=True, null=True)  # Физическое лицо
    legal_entity = models.ForeignKey(LegalEntity, on_delete=models.SET_NULL, blank=True, null=True)  # Юридическое лицо
    seller = models.ForeignKey(User, on_delete=models.CASCADE)  # Продавец

    def clean(self):
        if self.physical_person is None and self.legal_entity is None:
            raise ValidationError('Необходимо заполнить либо поле "Физическое лицо", либо "Юридическое лицо"')

    def save(self, *args, **kwargs):
        self.clean()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order №{self.id}"  # Отображение названия юридического лица в админке

class OrderComposition(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Заказ
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)  # Лекарство
    price = models.FloatField()  # Цена
    quantity = models.IntegerField()  # Количество

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity}шт. - {self.price}р."

class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=100)  # Номер
    physical_person = models.ForeignKey(PhysicalPerson, on_delete=models.CASCADE)  # Физическое лицо
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)  # Лекарство
    medical_facility = models.ForeignKey(MedicalFacility, on_delete=models.CASCADE)  # Лечебное учреждение
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Врач
    status = models.CharField(max_length=100)  # Статус
    prescription_date = models.DateField()  # Дата выписки
    doctor_visit_date = models.DateField()  # Дата обращения к врачу
    pharmacy_visit_date = models.DateField()  # Дата обращения в аптеку
    document_scan = models.TextField()  # Скан документа

    def __str__(self):
        return f"Prescription №{self.number} for {self.prescription_date}, {self.medicine.name} - {self.doctor.__str__()}"

