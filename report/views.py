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
from django.db.models import  F, ExpressionWrapper, DecimalField
 

@login_required
def warehouse(request):
    if request.method == "POST":
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('warehouse')
    else:
        today = date.today()
        yesterday = today - timedelta(days=1)
        form = WarehouseForm()
        stocks = Warehouse.objects.all()
        expired_stocks_count = Warehouse.objects.filter(expiry_date__lt=today).count()
        expired_stocks_soon = Warehouse.objects.filter(expiry_date__range=[today, today + timedelta(days=3)])

        for stock in expired_stocks_soon:
            stock.days_left = (stock.expiry_date - today).days if stock.expiry_date else None
        categories = [choice[0] for choice in Warehouse.CATEGORY_CHOICES]
        category_counts = [Warehouse.objects.filter(category=cat).count() for cat in categories]
        new_items_count = Warehouse.objects.filter(arrival_date__gte=yesterday).count()
        total_value = Warehouse.objects.aggregate(
            total=Sum(
                    ExpressionWrapper(F('purchase_price') * F('quantity'), output_field=DecimalField())
                )
            )['total'] or 0
        selling_total_value = Warehouse.objects.aggregate(
            total=Sum(
                    ExpressionWrapper(F('selling_price') * F('quantity'), output_field=DecimalField())
                )
            )['total'] or 0
        
        profit = (selling_total_value-total_value)/total_value * 100
    context = {
        'total_value': total_value,
        'profit':profit,
        'new_items_count':new_items_count,
        'categories':categories,
        'category_counts':category_counts,
        'form': form,
        'stocks': stocks,
        'all_stock': stocks.count(),
        'today': today,
        'expired_stocks_count': expired_stocks_count,
        'expired_stocks_soon': expired_stocks_soon,
        'expired_stocks_soon_count': expired_stocks_soon.count(),
    }

    return render(request, 'warehouse.html', context)

@login_required
def search_debtors(request):
    query = request.GET.get('q', '')
    
    if query:
        debtors_queryset = Debtor.objects.filter(full_name__icontains=query)  
    else:
        debtors_queryset = Debtor.objects.none()

    data = list(debtors_queryset.values('id', 'full_name'))
    return JsonResponse(data, safe=False)

def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.none()

    data = list(products.values('id', 'name'))

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

    categories = [choice[0] for choice in Warehouse.CATEGORY_CHOICES]
    warehouse = Warehouse.objects.all()

    context = {
        'categories': categories,
        'stocks': warehouse,
    }


    return render(request, 'home.html', context)

@login_required
def tools(request):

    return render(request, 'tools.html')

@login_required
def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    data = {
        'name': product.name,
        'description': product.description,
        'image_url': product.image_url,
    }
    return JsonResponse(data)

@login_required
def products(request):

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_product":
            name = request.POST.get("name")
            description = request.POST.get("description")
            image_url = request.POST.get("image_url")
            user_id = request.POST.get("user")

            if name:
                user = User.objects.get(id=user_id)
                Product.objects.create(name=name, description=description, image_url=image_url, user=user)
                return redirect("products")

    total_products = Product.objects.count()
    products = Product.objects.all()
    form = ProductForm()
    one_month_ago = timezone.now() - timedelta(days=30)
    new_products_last_month = Product.objects.filter(date__gte=one_month_ago).count()
    context = {
        'products': products,
        'form':form,
        'total_products': total_products,
        'new_products_last_month':new_products_last_month,
    }
    return render(request, 'products.html', context)

@login_required
def list_view(request):

    if request.method == "POST":
        if request.method == 'POST':
            action = request.POST.get("action")
            if action == "add_product":
                form = ProductRequestForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('list')
            else:
                print(form.errors)
    else:
            
        form = ProductRequestForm()
        product_requests = ProductRequest.objects.all() 

        context = {
            'form':form,
            'product_requests': product_requests,
            'product_count': product_requests.count(),
            'product_count_that_approve': ProductRequest.objects.filter(status="qabul_qilingan").count() or 0,
            'product_count_that_wait': ProductRequest.objects.filter(status="kutilyapti").count() or 0,
            'product_count_that_reject': ProductRequest.objects.filter(status="bekor_qilingan").count() or 0,
        }

        return render(request, 'list.html', context)
    
@login_required
def approve_request(request, req_id):

    product_request = get_object_or_404(ProductRequest, id=req_id)
    
    product_request.status = 'qabul_qilingan'
    product_request.save()

    return redirect('list')

@login_required
def reject_request(request, req_id):

    product_request = get_object_or_404(ProductRequest, id=req_id)
    
    product_request.status = 'bekor_qilingan'
    product_request.save()

    return redirect('list')

@login_required
def delete_request_product(request, req_id):
    req_product = get_object_or_404(ProductRequest, id=req_id)
    req_product.delete()
    return redirect('list')

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
def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'view_product.html', context)

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

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')  
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
def edit_stock(request, stock_id):
    stock = get_object_or_404(Warehouse, id=stock_id)
    
    if request.method == "POST":
        form = WarehouseForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('warehouse')  
    else:
        form = WarehouseForm(instance=stock)
    
    return render(request, 'edit_stock.html', {'form': form, 'stock': stock})


@csrf_exempt
@login_required
def delete_debtor(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    if request.method == "POST":
        debtor.delete()
        return redirect('debit')
    
@csrf_exempt
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect('products')
    
@csrf_exempt
@login_required
def delete_stock(request, stock_id):
    stock = get_object_or_404(Warehouse, id=stock_id)
    if request.method == "POST":
        stock.delete()
        return redirect('warehouse')

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
def logout_view(request):
    logout(request)
    return redirect('login')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

@login_required
def test(request):
    return render(request, 'test.html')

@login_required
def auth_check(request):
    return JsonResponse({'user': request.user.username})