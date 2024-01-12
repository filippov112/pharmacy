from django.urls import path
from .views import index_view, login_view, error_access, reports_list, medicine_list, supplier_list, contract_list, \
    certificate_list, receipt_list, med_group_list, facility_list, doctor_list, physic_list, legal_list, order_list, \
    prescription_list, medicine_edit, supplier_edit, contract_edit, certificate_edit, receipt_edit, facility_edit, \
    doctor_edit, physic_edit, legal_edit, order_edit, prescription_edit, medicine_id, supplier_id, contract_id, \
    certificate_id, receipt_id, facility_id, doctor_id, physic_id, legal_id, order_id, prescription_id, med_group_id, \
    med_group_edit



urlpatterns = [
    path('', index_view, name='index'),

    path('prescription/<int:record>', prescription_id, name='prescription_id'),
    path('order/<int:record>', order_id, name='order_id'),
    path('legal/<int:record>', legal_id, name='legal_id'),
    path('physic/<int:record>', physic_id, name='physic_id'),
    path('doctor/<int:record>', doctor_id, name='doctor_id'),
    path('facility/<int:record>', facility_id, name='facility_id'),
    path('receipt/<int:record>', receipt_id, name='receipt_id'),
    path('certificate/<int:record>', certificate_id, name='certificate_id'),
    path('contract/<int:record>', contract_id, name='contract_id'),
    path('supplier/<int:record>', supplier_id, name='supplier_id'),
    path('medicine/<int:record>', medicine_id, name='medicine_id'),
    path('med-group/<int:record>', med_group_id, name='med_group_id'),

    path('prescription/edit/<int:record>', prescription_edit, name='prescription_edit'),
    path('order/edit/<int:record>', order_edit, name='order_edit'),
    path('legal/edit/<int:record>', legal_edit, name='legal_edit'),
    path('physic/edit/<int:record>', physic_edit, name='physic_edit'),
    path('doctor/edit/<int:record>', doctor_edit, name='doctor_edit'),
    path('facility/edit/<int:record>', facility_edit, name='facility_edit'),
    path('receipt/edit/<int:record>', receipt_edit, name='receipt_edit'),
    path('certificate/edit/<int:record>', certificate_edit, name='certificate_edit'),
    path('contract/edit/<int:record>', contract_edit, name='contract_edit'),
    path('supplier/edit/<int:record>', supplier_edit, name='supplier_edit'),
    path('medicine/edit/<int:record>', medicine_edit, name='medicine_edit'),
    path('med-group/edit/<int:record>', med_group_edit, name='med_group_edit'),

    path('prescription/edit/<str:record>', prescription_edit, name='prescription_new'),
    path('order/edit/<str:record>', order_edit, name='order_new'),
    path('legal/edit/<str:record>', legal_edit, name='legal_new'),
    path('physic/edit/<str:record>', physic_edit, name='physic_new'),
    path('doctor/edit/<str:record>', doctor_edit, name='doctor_new'),
    path('facility/edit/<str:record>', facility_edit, name='facility_new'),
    path('receipt/edit/<str:record>', receipt_edit, name='receipt_new'),
    path('certificate/edit/<str:record>', certificate_edit, name='certificate_new'),
    path('contract/edit/<str:record>', contract_edit, name='contract_new'),
    path('supplier/edit/<str:record>', supplier_edit, name='supplier_new'),
    path('medicine/edit/<str:record>', medicine_edit, name='medicine_new'),
    path('med-group/edit/<str:record>', med_group_edit, name='med_group_new'),

    path('prescription', prescription_list, name='prescription_list'),
    path('order', order_list, name='order_list'),
    path('legal', legal_list, name='legal_list'),
    path('physic', physic_list, name='physic_list'),
    path('doctor', doctor_list, name='doctor_list'),
    path('facility', facility_list, name='facility_list'),
    path('med-group', med_group_list, name='med_group_list'),
    path('receipt', receipt_list, name='receipt_list'),
    path('certificate', certificate_list, name='certificate_list'),
    path('contract', contract_list, name='contract_list'),
    path('supplier', supplier_list, name='supplier_list'),
    path('medicine', medicine_list, name='medicine_list'),

    path('report', reports_list, name='report_list'),
    path('error_access/<int:exception>', error_access, name='err_access'),
    path('login', login_view, name='login'),
]
