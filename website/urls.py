from django.urls import path
from website.views import *
app_name = 'website'
urlpatterns = [
    #path('url address', 'view', 'name')
    path('index',index_view,name="index"),
    path('',shop_view,name="shop"),
    path('<int:pid>',shop_single,name="single"),
    path('cart/',cart_view,name='cart'),
    path('update_item/', updateItem, name='update_item'),
    path('checkout/',checkout_view,name='checkout'),
    # path('about',about_view,name="about"),
    # path('test',test,name="test"),
    # path('newsletter',newsletter_view,name="newsletter"),
]
