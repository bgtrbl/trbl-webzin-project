
from allauth.account.forms import LoginForm

def login_proc(request):
    if not request.user.is_authenticated():
        return {'modal_login_form' : LoginForm()}
    else:
        return {}

