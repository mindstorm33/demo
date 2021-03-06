from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm



# Create your views here.

def registration_view(request):
    """ render and serve the registration page for the user"""

    if request.method != 'POST':
        # No data submited; serve blank form
        form = RegistrationForm()
    
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
            
    context = {"form": form}
    return render(request, 'account/register.html', context)



def logout_view(request):
    """ log out the user """
    logout(request)
    return redirect("home")



def login_view(request):
    """ user login form view """

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.method != 'POST':
        # is a get request, serve blank form
        form = AccountAuthenticationForm()

    else:
        # is a post request; get and process data
        form = AccountAuthenticationForm(request.POST)

        # first validate form
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            authenticated_user = authenticate(email=email, password=password)

            if authenticated_user:
                login(request, authenticated_user)
                return redirect("home")
    
    context = {'form':form}
    return render(request, 'account/login.html', context)
        

def account_view(request):
    """"""
    if not request.user.is_authenticated:
        return redirect("home")

    context={}

    if request.method != 'POST':
        # is a GET request
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    else:
        # is POST request; process data
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial={
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated!"
            
    context['form'] = form
    return render(request, 'account/account.html', context)


def must_authenticate_view(request):
    """"""
    return render(request, 'account/must_authenticate.html', {})
    


