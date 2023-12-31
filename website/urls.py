from django.urls import path
from website.views import *
app_name = 'website'
urlpatterns = [
    #path('url address', 'view', 'name')

    path('',shop_view,name="shop"),
    path('<str:filter>',shop_view,name='shop'),
    path('single/<int:pid>',shop_single,name="single"),
    path('cart/',cart_view,name='cart'),
    path('update_item/', updateItem, name='update_item'),
    path('checkout/',checkout_view,name='checkout'),
    path('search/',search_view,name='search'),
    path('tag/<str:tag_name>',shop_view,name="tag"),
    # path('about',about_view,name="about"),
    # path('test',test,name="test"),
    # path('newsletter',newsletter_view,name="newsletter"),
]
