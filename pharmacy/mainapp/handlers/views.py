from .commons import *



@login_required(login_url=login_view)
def medicine_id(request, record):
    context = get_default_context('medicine', user=request.user)
    custom_context = {
        'edit_link': reverse('medicine_edit', args=[record])
    }
    return render(request, 'mainapp/view.html', context | custom_context)


@login_required(login_url=login_view)
def prescription_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def order_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def legal_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def physic_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def doctor_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def facility_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def receipt_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def certificate_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def contract_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)


@login_required(login_url=login_view)
def supplier_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/index.html', context | custom_context)



@login_required(login_url=login_view)
def med_group_id(request):
    context = get_default_context('index', user=request.user)
    custom_context = {}
    return render(request, 'mainapp/view.html', context | custom_context)
