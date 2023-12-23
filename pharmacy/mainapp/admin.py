from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MedicineGroup)
admin.site.register(Medicine)
admin.site.register(Supplier)
admin.site.register(Contract)
admin.site.register(ContractMedicine)
admin.site.register(Certificate)
admin.site.register(CertificateAttachment)
admin.site.register(Receipt)
admin.site.register(ReceiptItem)
admin.site.register(MedicalFacility)
admin.site.register(Doctor)
admin.site.register(PhysicalPerson)
admin.site.register(LegalEntity)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderComposition)
admin.site.register(Prescription)
