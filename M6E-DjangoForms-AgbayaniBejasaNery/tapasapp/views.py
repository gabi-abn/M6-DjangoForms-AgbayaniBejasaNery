from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Dish, Account

# Create your views here.


def better_menu(request):
    if 'account_id' not in request.session:
        return redirect('login')

    dish_objects = Dish.objects.all()
    account_id = request.session.get('account_id')

    return render(request, 'tapasapp/better_list.html', {
        'dishes': dish_objects,
        'account_id': account_id
    })

def add_menu(request):
    if request.method == "POST":
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')

        if not dishname or not cooktime or not preptime:
            messages.error(request, "Please fill up all fields.")
            return redirect('add_menu')

        else:
            Dish.objects.create( name=dishname, cook_time=cooktime, prep_time=preptime )
            messages.success(request, "Dish added successfully!")
            return redirect('better_menu')

    return render(request, 'tapasapp/add_menu.html')

def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')

    if request.method == "POST":
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')

        try:
            cooktime = float(cooktime)
            preptime = float(preptime)
        except (TypeError, ValueError):
            messages.error(request, "Please enter valid numbers.")
            return redirect("update_dish", pk=pk)

        if cooktime <= 0 or preptime <= 0:
            messages.error(request, "Values must be positive numbers only.")
            return redirect("update_dish", pk=pk)

        Dish.objects.filter(pk=pk).update(
            cook_time=cooktime,
            prep_time=preptime
        )

        return redirect('view_detail', pk=pk)

    return render(request, 'tapasapp/update_menu.html', {'d': d})    
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', "").strip()
        password = request.POST.get('password', "").strip()
        account = Account.objects.filter(username=username, password=password).first()

        if account:
            request.session['account_id'] = account.id #store user
            return redirect('better_menu')
        else:
            messages.error(request, 'Invalid login')

    return render(request, 'tapasapp/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', "").strip()
        password = request.POST.get('password', "").strip()
        if Account.objects.filter(username=username).exists():
            messages.error(request, 'Account already exists')
        else:
            Account.objects.create(username=username, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('login')
        
    return render(request, 'tapasapp/signup.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'tapasapp/manage_account.html', {'account': account})

def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    account.delete()
    request.session.flush()
    return redirect('login')

def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)

    if request.method == "POST":
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if account.password != current:
            messages.error(request, "Incorrect current password")
        elif new != confirm:
            messages.error(request, "Passwords do not match")
        else:
            account.password = new
            account.save()
            messages.success(request, "Password updated")
            return redirect('manage_account', pk=pk)

    return render(request, 'tapasapp/change_password.html', {'account': account})
