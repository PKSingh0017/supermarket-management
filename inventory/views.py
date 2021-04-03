from django.shortcuts import render
from .models import Item, Category

# Create your views here.


def home(request):
    all_items = Item.objects.all()
    all_categories = Category.objects.all()
    categorypk = request.GET.get('categorypk')
    if categorypk:
        category = Category.objects.get(pk=categorypk)
        all_items = Item.objects.filter(cataegory=category)
    context = {
        'all_items': all_items,
        'all_categories': all_categories
    }
    return render(request, 'inventory/home.html', context)


def about(request):
    return render(request, 'inventory/about.html')

def billing(request):
    return render(request, 'inventory/billing.html')