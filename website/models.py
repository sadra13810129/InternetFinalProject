from django.db import models
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import F, ExpressionWrapper, DecimalField
from django.contrib.auth.models import User
class Item(models.Model):
    Size_options = [
        ('tiny', 'tiny'),
        ('small', 'small'),
        ('medium', 'medium'),
        ('large','large')
        
    ]
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='items_image/')
    category = TaggableManager()
    off = models.BooleanField(default=False)
    description = models.TextField()
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True, blank=True)
    size = models.CharField(max_length=10, choices=Size_options)
    color = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        if self.discount is not None:
            self.final_price = self.price - (self.discount * self.price) / 100
        else:
            self.final_price = self.price
        super().save(*args, **kwargs)
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    # def snippets(self):
    #     return self.content[:100] + "..."
    



    
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField()  # Corrected typo from 'emal' to 'email'

    def __str__(self):
        return self.name

        
        
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([orderitem.get_total for orderitem in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([orderitem.quantity for orderitem in orderitems])
        return total
    
    def __str__(self):
        return str(self.id)
    
    
class OrderItem(models.Model):
    item = models.ForeignKey(Item,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.item.final_price * self.quantity
        return total
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    adderss = models.CharField(max_length=255,null=False)
    city = models.CharField(max_length=255,null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    