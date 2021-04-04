from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
from django.shortcuts import reverse

# Create your models here.

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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
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

class Order(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)

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


