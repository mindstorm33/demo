from django.shortcuts import render
from account.models import Account
# Create your views here.

def home_screen_view(request):

    users = Account.objects.all()
    context = {'users': users}
    return render(request, 'personal/home.html', context)
