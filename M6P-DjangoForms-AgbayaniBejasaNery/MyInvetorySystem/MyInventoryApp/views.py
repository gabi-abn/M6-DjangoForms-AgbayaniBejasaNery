from django.shortcuts import render, redirect
from django.contrib import messages
from MyInventoryApp.models import Supplier, WaterBottle, Account

def view_supplier(request):
    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {'suppliers': supplier_objects})

def view_bottles(request):
    bottle_objects = WaterBottle.objects.all()
    return render(request, 'MyInventoryApp/view_bottles.html', {'bottles': bottle_objects})

def add_bottle(request):
    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/add_bottle.html', {'suppliers': supplier_objects})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        account = Account.objects.filter(username=username, password=password).first()
        if account:
            return redirect('view_supplier')
        else:
            messages.error(request, 'Invalid login')
    return render(request, 'MyInventoryApp/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if Account.objects.filter(username=username).exists():
            messages.error(request, 'Account already exists')
            return render(request, 'MyInventoryApp/signup.html')
        else:
            Account.objects.create(username=username, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('login')

    return render(request, 'MyInventoryApp/signup.html')