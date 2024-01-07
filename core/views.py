from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'core/index.html')

def about(request):
    return render(request,'core/about.html')

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.object.get(username=username)
        except:
            print('username Does Not Exist !!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'dashboard:index')
        else:
            messages.error(request,'User Name or password is incorrect')
    context = {'page': 'Login'}
    return render(request, 'core/login_register.html', context)

