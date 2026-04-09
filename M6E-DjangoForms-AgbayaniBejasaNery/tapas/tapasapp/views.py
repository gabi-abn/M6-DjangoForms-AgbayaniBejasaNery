from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        account = Account.objects.filter(username=username, password=password).first()

        if account:
            return redirect('view_supplier')  # your main page
        else:
            messages.error(request, 'Invalid login')

    return render(request, 'tapasapp/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if Account.objects.filter(username=username).exists():
            messages.error(request, 'Account already exists')
        else:
            Account.objects.create(username=username, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('login')

    return render(request, 'tapasapp/signup.html')