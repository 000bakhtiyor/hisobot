from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum,Min

def search_debtors(request):
    query = request.GET.get('q', '')
    if query:
        debtors = Debtor.objects.filter(full_name__icontains=query)
    else:
        debtors = Debtor.objects.none()

    data = list(debtors.values('id', 'full_name'))
    
    return JsonResponse(data, safe=False)

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Ism yoki parolingiz xato")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def home(request):

    return render(request, 'home.html')

@login_required
def tools(request):

    return render(request, 'tools.html')

@login_required
def excel(request):

    return render(request, 'excel.html')

@login_required
def view_debts_that_debtor(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    debts = debtor.debts.all()
    total_debt = debts.aggregate(total=Sum('amount'))['total'] or 0
    context = {
        'debtor': debtor,
        'debts': debts,
        'total_debt':total_debt,
    }
    return render(request, 'debtor_debts.html', context)

@login_required
def edit_debtor(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    
    if request.method == "POST":
        form = DebtorForm(request.POST, instance=debtor)
        if form.is_valid():
            form.save()
            return redirect('debit')  
    else:
        form = DebtorForm(instance=debtor)
    
    return render(request, 'edit_debtor.html', {'form': form, 'debtor': debtor})

@csrf_exempt
@login_required
def delete_debtor(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    if request.method == "POST":
        debtor.delete()
        return redirect('debit')

@csrf_exempt
@login_required
def debit(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_debtor":
            full_name = request.POST.get("full_name")
            social_link = request.POST.get("social_link")
            phone = request.POST.get("phone")
            address = request.POST.get("address")

            if full_name:
                Debtor.objects.create(full_name=full_name, social_link=social_link, phone_number=phone, address=address)
                return redirect("debit")
             
        elif action == "add_debt":
            debtor_id = request.POST.get("debtor")
            amount = request.POST.get("amount")
            date = request.POST.get("date")
            note = request.POST.get("note")

            if debtor_id and amount and date:
                debtor = Debtor.objects.get(id=debtor_id)
                Debt.objects.create(debtor=debtor, amount=amount, date=date, note=note)
                return redirect("debit")
            
    # debtors = Debtor.objects.all()
    # debts = Debt.objects.all()
    debtors = Debtor.objects.annotate(total_debt=Sum('debts__amount'),oldest_debt_date=Min('debts__date'))
    total_debt_sum = debtors.aggregate(Sum('total_debt'))['total_debt__sum'] or 0
    old_debtors = 0
    new_debt_sum = 0
    for debtor in debtors:
        if debtor.oldest_debt_date:
            if debtor.oldest_debt_date < timezone.now().date() - timedelta(days=30):
                debtor.debt_status = 'old'
                old_debtors+=1
            else:
                debtor.debt_status = 'new'
                new_debt_sum += debtor.total_debt
        else:
            debtor.debt_status = 'no'
    
    return render(request, 'debits.html',{
                      "debtors":debtors,
                      'total_debt_sum': total_debt_sum,
                      'old_debtors':old_debtors,
                      'new_debt_sum':new_debt_sum,
                    }
                )


@login_required
def test(request):

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def custom_404(request, exception):
    return render(request, '404.html', status=404)