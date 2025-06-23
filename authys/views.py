from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('adminDashboard:dashboard_home') 
            return redirect('dashboard:landing_page') 
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'authys/login.html')
    
    return render(request, 'authys/login.html')


def welcome_page(request):
    return render(request, 'authys/welcomePage.html')