from django import template
from inventory.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(staff=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0
