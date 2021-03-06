from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.

# class Customer(models.Model):
#     firstname = models.CharField(max_length=50)
#     lastname = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=15)
#     brownie_points = models.IntegerField(default=0)
#     slug = models.SlugField(unique=True)

#     def __str__(self):
#         return render(self.firstname)

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Item(models.Model):
    cataegory = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    price = models.IntegerField()
    discount_percentage = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'pk': self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })

    def actual_price(self):
        return self.price - (self.price * self.discount_percentage)/100

class OrderItem(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.get_total_item_price() - (self.quantity * self.item.discount_percentage * self.item.price / 100)

    def get_amount_saved(self):
        return self.quantity * self.item.discount_percentage * self.item.price / 100

    def get_final_price(self):
        if self.item.discount_percentage:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    
    
    def __str__(self):
        return f"{self.quantity} of {self.item.name}"


class Order(models.Model):
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    paymentid = models.CharField(max_length=8, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.customer.firstname

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total = total + order_item.get_final_price()
        return total
    
    def get_total_quantity(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity
        return total
    
    def __str__(self):
        return f"order of {self.firstname} created by {self.staff.username}"

class Payment(models.Model):
    paymentid = models.CharField(max_length=8)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.paymentid



