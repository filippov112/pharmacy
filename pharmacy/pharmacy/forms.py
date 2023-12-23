from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.remember = kwargs.pop('remember', False) == 'on'
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)