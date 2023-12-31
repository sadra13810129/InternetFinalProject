from django.contrib import admin
from website.models import *
class ItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('title','status','published_date','created_date')
    list_filter = ('status',)
    ordering = ['-created_date']
    search_fields = ['title']

    
admin.site.register(Item,ItemAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)