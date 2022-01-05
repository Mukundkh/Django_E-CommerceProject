# # from django.db import models
# # from store.models import Product
# # from django.contrib.auth import get_user_model
# # from django.dispatch import receiver
# # from django.db.models.signals import post_save
# # # Create your models here.
# # class TimeStampedModel(models.Model):
# #     created = models.DateTimeField(db_index=True, auto_now_add=True)
# #     modified = models.DateTimeField(auto_now=True)

# #     class Meta:
# #         abstract = True

# # User = get_user_model()

# # class Cart(TimeStampedModel):
# #     user = models.OneToOneField(
# #         User, related_name="user_cart", on_delete=models.CASCADE
# #     )
# #     total = models.DecimalField(
# #         max_digits=10, decimal_places=2, default=0, blank=True, null=True
# #     )

# # @receiver(post_save, sender=User)
# # def create_user_cart(sender, created, instance, *args, **kwargs):
# #     if created:
# #         Cart.objects.create(user=instance)

# # class CartItem(TimeStampedModel):
# #     cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
# #     product = models.ForeignKey(
# #         Product, related_name="cart_product", on_delete=models.CASCADE
# #     )
# #     quantity = models.IntegerField(default=1)

# from django.db import models
# from django.contrib.auth.models import User
# from store.models import Product
# from django.db.models.signals import pre_save, post_save


# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     total_price = models.FloatField(default=0)


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.FloatField(default=0)
#     total_items = models.IntegerField(default=0)
#     quantity = models.IntegerField(default=1)

# @receiver(post_save, sender=CartItem)
# def correct_price(sender, **kwargs):
#     print("I got called")

    
from django.contrib.auth import get_user_model
from django.db import models

from store.models import Product

User = get_user_model()

class CartManager(models.Manager):
    def get_existing_or_new(self, request):
        created = False
        cart_id = request.session.get('cart_id')
        if self.get_queryset().filter(id=cart_id, used=False).count() == 1:
            obj = self.model.objects.get(id=cart_id)
        elif self.get_queryset().filter(user=request.user, used=False).count() == 1:
            obj = self.model.objects.get(user=request.user, used=False)
            request.session['cart_id'] = obj.id
        else:
            obj = self.model.objects.create(user=request.user)
            request.session['cart_id'] = obj.id
            created = True
        return obj, created


class Cart(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    @property
    def total(self):
        total = 0
        for item in self.products.all():
            total += int(item.quantity) * float(item.product.price)
        return total

    @property
    def tax_total(self):
        total = 0
        for item in self.products.all():
            total += int(item.quantity) * float(item.product.price) * \
                float(item.product.tax) / 100
        return total

    @property
    def total_cart_products(self):
        return sum(item.quantity for item in self.products.all())


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="products")

    class Meta:
        unique_together = (
            ('product', 'cart')
        )