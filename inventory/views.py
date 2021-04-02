from django.shortcuts import render
from .models import Item, Category

# Create your views here.


def home(request):
    all_items = Item.objects.all()
    context = {
        'all_items': all_items
    }
    return render(request, 'inventory/home.html', context)


def about(request):
    return render(request, 'inventory/about.html')

def billing(request):
    return render(request, 'inventory/billing.html')