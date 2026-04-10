from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from MyInventoryApp.models import Supplier, WaterBottle, Account

def view_supplier(request):
    if 'account_id' not in request.session:
        return redirect('login')

    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {
        'suppliers': supplier_objects
    })

def view_bottles(request, supplier_id):
    if 'account_id' not in request.session:
        return redirect('login')

    supplier = get_object_or_404(Supplier, pk=supplier_id)
    bottles = WaterBottle.objects.filter(supplied_by=supplier)

    return render(request, 'MyInventoryApp/view_bottles.html', {
        'bottles': bottles,
        'supplier': supplier
    })

def view_bottle_details(request, pk):
    if 'account_id' not in request.session:
        return redirect('login')

    bottle = get_object_or_404(WaterBottle, pk=pk)

    if request.method == "POST":
        supplier_id = bottle.supplied_by.id
        bottle.delete()
        return redirect('view_bottles', supplier_id=supplier_id)

    return render(request, 'MyInventoryApp/view_bottle_details.html', {
        'bottle': bottle
    })

def add_bottle(request):
    if 'account_id' not in request.session:
        return redirect('login')

    suppliers = Supplier.objects.all()

    if request.method == "POST":
        WaterBottle.objects.create(
            SKU=request.POST['SKU'],
            brand=request.POST['brand'],
            cost=request.POST['cost'],
            size=request.POST['size'],
            mouth_size=request.POST['mouth_size'],
            color=request.POST['color'],
            current_quantity=request.POST['current_quantity'],
            supplied_by=Supplier.objects.get(id=request.POST['supplied_by'])
        )
        return redirect('view_supplier')

    return render(request, 'MyInventoryApp/add_bottle.html', {
        'suppliers': suppliers
    })

def manage_account(request, pk):
    if 'account_id' not in request.session:
        return redirect('login')

    if request.session['account_id'] != pk:
        return redirect('view_supplier')

    account = get_object_or_404(Account, pk=pk)

    return render(request, 'MyInventoryApp/manage_account.html', {
        'account': account
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        account = Account.objects.filter(username=username).first()

        if account and account.password == password:
            request.session['account_id'] = account.id
            return redirect('view_supplier')
        else:
            messages.error(request, 'Invalid login')

    return render(request, 'MyInventoryApp/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')

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

def delete_account(request, pk):
    if 'account_id' not in request.session:
        return redirect('login')

    if request.session['account_id'] != pk:
        return redirect('view_supplier')

    account = get_object_or_404(Account, pk=pk)
    account.delete()

    request.session.flush()
    messages.success(request, "Account deleted successfully")

    return redirect('login')

def change_password(request, pk):
    if 'account_id' not in request.session:
        return redirect('login')

    if request.session['account_id'] != pk:
        return redirect('view_supplier')

    account = get_object_or_404(Account, pk=pk)

    if request.method == "POST":
        current = request.POST['current_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm_password']

        if current != account.password:
            messages.error(request, "Incorrect current password")
        elif new != confirm:
            messages.error(request, "Passwords do not match")
        else:
            account.password = new
            account.save()
            messages.success(request, "Password updated successfully")
            return redirect('manage_account', pk=account.id)

    return render(request, 'MyInventoryApp/change_password.html', {
        'account': account
    })