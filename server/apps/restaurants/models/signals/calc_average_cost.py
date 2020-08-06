from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from apps.restaurants.models import Restaurant


@receiver(m2m_changed, sender=Restaurant.dishes.through)
def calc_average_cost(sender, **kwargs):
    dishes = kwargs['instance'].dishes.all()
    cost = None
    if len(dishes) != 0:
        cost = sum(dish.price for dish in dishes) / len(dishes)
    kwargs['instance'].average_cost = cost
    kwargs['instance'].save()
