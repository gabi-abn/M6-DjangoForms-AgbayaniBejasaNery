from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Account

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        account = Account.objects.filter(username=username, password=password).first()

        if account:
            return redirect('basic_list', pk=account.id)  # ✅ PASS PK
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

def basic_list(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'tapasapp/basic_list.html', {'account': account})


def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'tapasapp/manage_account.html', {'account': account})


def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)

    if request.method == 'POST':
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if account.password != current:
            messages.error(request, 'Incorrect current password')
        elif new != confirm:
            messages.error(request, 'Passwords do not match')
        else:
            account.password = new
            account.save()
            messages.success(request, 'Password updated successfully')
            return redirect('manage_account', pk=pk)

    return render(request, 'tapasapp/change_password.html', {'account': account})


def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    account.delete()
    return redirect('login')


def logout_view(request):
    return redirect('login')