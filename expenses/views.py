from django.shortcuts import render, redirect
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userPreferences.models import UserPreference
import datetime
#TODO: import messages
# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        
        data = expenses.values()
        return JsonResponse(list(data), safe=False)

def index(request):
    categories=Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    # currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses' : expenses,
        'page_obj' : page_obj, 
        # 'currency' : currency
    }
    return render(request, 'expenses/index.html', context)

def add_Expense(request):
    categories=Category.objects.all()
    context = {
            'categories' : categories, 
            'values' : request.POST
        }
    if request.method == 'GET':
        
        
        return render(request, 'expenses/addExpense.html', context)

    if request.method=="POST":
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, 'expenses/addExpense.html', context)
        

        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required!')
            return render(request, 'expenses/addExpense.html', context)
        
        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)

        messages.success(request,'Expense saved successfully!')

        return redirect('expenses')


# def create_dasdhboard_entry(request):
#     if request.method=='POST':
#         event=request.POST.get('event')
#         amount=request.POST.get('amount')
#         entry=Entry(event=event,amount=amount, timestamp=datetime.datetime.now())
#         entry.save()
#         messages.success(request,"Entry saved!")
#         #TODO: render html file path 
#     return render(request,'<html file path>')

def expense_edit(request, id):
    expense=Expense.objects.get(pk=id)
    categories=Category.objects.all()
    context = {
        'expense' : expense,
        'values' : expense,
        'categories' : categories
    }
    if request.method == 'GET':
        
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, 'expenses/edit-expense.html', context)
        

        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required!')
            return render(request, 'expenses/edit-expense.html', context)
        
        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()

        messages.success(request,'Expense updated successfully!')

        return redirect('expenses')


        messages.info(request, 'Handling post form')
        return render(request, 'expenses/edit-expense.html', context)
    

def expense_delete(request,id):
    expense= Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed!')
    return redirect('expenses')



def expense_category_summary(request):
    todays_date=datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    expenses=Expense.objects.filter(owner=request.user, date__gte=six_months_ago,date_lte=todays_date)
    finalrep = {

    }
    def get_category(expense):
        return expense.category

    category_list= list(set(map(get_category,expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category=expenses.filter(category=category)

        for item in filtered_by_category:
            amount+=item.amount

        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)


    return JsonResponse({'expense_category_data' : finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')

