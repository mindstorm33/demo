from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm



# Create your views here.

def registration_view(request):
    """ render and serve the registration page for the user"""

    if request.method != 'POST':
        # No data submited; serve blank form
        form = RegistrationForm()
        context = {'form': form}
    
    else:
        # POST data submitted; process data
        form = RegistrationForm(request.POST)
        # first validate form
        if form.is_valid():
            # if valid, save data
            form.save()
            # then authenticate user
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            authenticated_user = authenticate(email=email, password=raw_password)
            # then log in the user and redirect to home page
            login(request, authenticated_user)
            return redirect("home")
        else:
            context = {"form": form}
    
    return render(request, 'account/register.html', context)

def logout_view(request):
    """ log out the user """
    logout(request)
    return redirect("home")
