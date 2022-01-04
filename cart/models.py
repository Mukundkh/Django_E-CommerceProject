# from django.db import models
# from store.models import Product
# from django.contrib.auth import get_user_model
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# # Create your models here.
# class TimeStampedModel(models.Model):
#     created = models.DateTimeField(db_index=True, auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True

# User = get_user_model()

# class Cart(TimeStampedModel):
#     user = models.OneToOneField(
#         User, related_name="user_cart", on_delete=models.CASCADE
#     )
#     total = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0, blank=True, null=True
#     )

# @receiver(post_save, sender=User)
# def create_user_cart(sender, created, instance, *args, **kwargs):
#     if created:
#         Cart.objects.create(user=instance)

# class CartItem(TimeStampedModel):
#     cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         Product, related_name="cart_product", on_delete=models.CASCADE
#     )
#     quantity = models.IntegerField(default=1)

from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import pre_save, post_save


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    total_items = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

@receiver(pre_save, sender=CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = Product.objects.get(id=cart_items.product.id)
    cart_items.price = cart_items.quantity * float(price_of_product.price)
    total_cart_items = CartItems.objects.filter(user = cart_items.user )
    cart = Cart.objects.get(id = cart_items.cart.id)
    cart.total_price = cart_items.price
    cart.save()
