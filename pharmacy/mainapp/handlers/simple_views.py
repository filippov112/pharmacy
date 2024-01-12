from .commons import *

@login_required(login_url=login_view)
def medicine_id(request, record):
    o = Medicine
    n = 'medicine'
    default_context = get_default_context(n, user=request.user)
    view_context = get_view_context(n, record, o)
    custom_context = {}
    return render(request, 'mainapp/view.html', default_context | view_context | custom_context)