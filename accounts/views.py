from django.shortcuts import render, redirect
from .models import Accounts
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from accounts.forms import RegistrationForm, AccountsAuthenticationForm, AccountUpdateForm


def registration(request):
    # context = {}
    # if request.POST:
    #     form = RegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         email = form.cleaned_data.get('email')
    #         raw_password = form.cleaned_data.get('password1')
    #         accounts = authenticate(email=email, password= password1)
    #         login(request, accounts)
    #         return redirect('home')
    #     else:
    #         context['registration_form'] = form
    # else:  # GET request
    #     form = RegistrationForm()
    #     context = {"form": form}
    form = RegistrationForm()
    if request.method == "POST":
        print('form valid  ------')
        form = RegistrationForm(request.POST)
        try: 
            if form.is_valid():
                form.save()
                return redirect('home')
            else:
                print('form not  valid  2------')
        except ValueError:
            print('form not valid  ------')
            return redirect('register')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

   
def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    # if request.POST:
    #     form = AccountsAuthenticationForm(request.POST)
    #     if form.is_valid():
    #         email = request.POST['email']
    #         password = request.POST['password']
    #         user = authenticate(email=email, password=password)

    #         if user:
    #             login(request, user)
    #             return redirect('home')
    # else:
    #     form = AccountsAuthenticationForm()

    # context['login_form'] = form
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if User is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or Password incorrect')
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'accounts/login.html', context)


def accounts(request):

    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = AccountsUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_massage'] = "Updated"
    else:
        form = AccountsUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['accounts_form'] = form
    return render(request, "accounts/accounts.html", context)
