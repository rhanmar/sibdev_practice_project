from django.db.models.signals import m2m_changed

from apps.restaurants.models import Restaurant


def calc_average_cost(sender, **kwargs):
    dishes = kwargs['instance'].dishes.all()
    cost = None
    if len(dishes) != 0:
        cost = sum(dish.price for dish in dishes) / len(dishes)
    kwargs['instance'].average_cost = cost
    kwargs['instance'].save()


m2m_changed.connect(calc_average_cost, sender=Restaurant.dishes.through)
