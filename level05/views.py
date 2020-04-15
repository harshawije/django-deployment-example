from django.shortcuts import render
from level05.forms import UserForm, UserProfileInfoForm

# login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request,'level05/index.html')


@login_required() # Decorator to check login status
def user_logout(request):
    logout(request) # build in django function
    return HttpResponseRedirect(reverse('index'))


@login_required()
def special(request):
    return HttpResponse("Special logged in page")


def register(request):

    registered = False

    if request.method == "POST":

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False) # dont save yet
            profile.user = user # set up one to one relationship with user

            # if theres a profile picture

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:

        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'level05/registration.html', {
                                            'user_form':user_form,
                                            'profile_form': profile_form,
                                            'registered': registered})


def user_login(request):
    print("Called")
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        print("Username: {} Password: {}".format(username, password))

        # automatically authenticante the user usign django
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user) # login user from imported django function
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active!")
        else:
            print("Someone tried to login and failed")

            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'level05/login.html')


def test_func(request):
    return HttpResponse("Test OK")

