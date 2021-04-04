from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .models import Item, Category, OrderItem,  Order, Payment
from .forms import BillingForm
import random
import string
# Create your views here.

def create_paymentid(n):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

def gen_custid(n):
    id = ''.join(random.choices(string.digits, k=n))
    return int(id)

def home(request):
    all_items = Item.objects.all()
    all_categories = Category.objects.all()
    categorypk = request.GET.get('categorypk')
    if categorypk:
        category = Category.objects.get(pk=categorypk)
        all_items = Item.objects.filter(cataegory=category)
    all_items_p = Paginator(all_items, 10)
    page = request.GET.get('page')
    all_items = all_items_p.get_page(page)
    context = {
        'all_items': all_items,
        'all_categories': all_categories
    }
    return render(request, 'inventory/home.html', context)

def about(request):
    return render(request, 'inventory/about.html')

def billing(request):
    curr_staff = request.user
    curr_order = Order.objects.get(staff=curr_staff)
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            curr_order.firstname = form.cleaned_data.get('firstname')
            curr_order.lastname = form.cleaned_data.get('lastname')
            curr_order.phone_number = form.cleaned_data.get('phone_number')
            curr_order.save()
            messages.success(request, f"Order created for {curr_order.firstname}")
            return redirect('payment')
    else:
        context = {
            'order': curr_order
        }
        return render(request, 'inventory/billing.html', context)
    

def payment(request):
    curr_staff = request.user
    curr_order = Order.objects.get(staff=curr_staff)
    new_payment = Payment()
    new_payment.paymentid = create_paymentid(8)
    new_payment.staff = curr_staff
    new_payment.timestamp = timezone.now
    new_payment.save()
    curr_order.ordered = True
    curr_order.payment = new_payment
    curr_order.paymentid = new_payment.paymentid
    curr_order.save()
    order_items = curr_order.items.all()
    order_items.update(ordered=True)
    for item in order_items:
        item.save()
    messages.success(request, f"Order completed for  {curr_order.firstname}!")
    context = {
        'order': curr_order
    }
    return render(request, 'inventory/payment_info.html', context)


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        staff=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(staff=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated in your cart.")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("home")
    else:
        order = Order.objects.create(
            staff=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect("home")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(
        staff=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                staff=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Item Removed!")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in cart.")
            return redirect("home")

    else:
        messages.info(request, "There is no active order.")
        return redirect("home")
    

@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        staff=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                staff=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "Item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("home")
    else:
        messages.info(request, "You do not have an active order! Try adding items to your cart.")
        return redirect("home")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(staff=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'inventory/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")