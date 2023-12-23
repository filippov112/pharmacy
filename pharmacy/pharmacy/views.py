from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, remember=request.POST.get('remember'))
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if form.remember:
                request.session.set_expiry(2592000)  # устанавливаем срок действия сессии на 30 дней (в секундах)
            return redirect('admin:index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'mainapp/login.html', {'form': form})