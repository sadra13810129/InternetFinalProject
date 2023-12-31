from django.shortcuts import render
from django.http import JsonResponse
from website.models import Item,Order,OrderItem
from django.views.decorators.csrf import csrf_exempt
from taggit.models import Tag
from django.contrib import messages
import json
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import redirect
# Create your views here.


def shop_view(request,**kwargs):
    
    items = Item.objects.filter(status=1)
    if kwargs.get('tag_name') != None:
        items = items.filter(category__name__in = [kwargs['tag_name']])
    if kwargs.get('filter') != None:
        if kwargs.get('filter') == 'latest':
            items = items.filter(status=1).order_by('-published_date')
            print('hello')
        elif kwargs.get('filter') == 'lower':
            items = items.filter(status=1).order_by('-final_price')
        elif kwargs.get('filter') == 'highter' : 
            items = items.filter(status=1).order_by('final_price')
        elif kwargs.get('filter') == 'discount':
            items = items.filter(status=1,off=1).order_by('discount')
            

        # customer = request.user.customer
        # order= Order.objects.get(customer=customer,complete=False)
        # cartItems = order.get_cart_items
        # order.delete()
        # cartItems.delete()
    
    items = Paginator(items,6)
    try:    
        page_number = request.GET.get('page')
        items = items.get_page(page_number)
    except PageNotAnInteger:
        items = items.get_page(1)
    except EmptyPage:
        items = items.get_page(1)
    tags = Tag.objects.all()
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        orderitems = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cartItems = 0
        orderitems = {}
        order = {}
    context = {'items' : items, 'tags' : tags,'orderitems' : orderitems,'order' : order,'cartItems' : cartItems}
    return render(request,'website_templates\shop.html',context=context)



def shop_single(request,pid):
    print('single')
    try:
        item = Item.objects.get(pk=pid, status=1)
    except Item.DoesNotExist:
        return render(request, '404.html')
    # comments = Comment.objects.filter(post = post.id, approved=True).order_by('created_date')
    # form = CommentForm()
    # context = {'post' : post, 'next_post' : next_post, 'prev_post' : prev_post, 'form':form, 'comments' : comments , 'img':img}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        orderitems = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cartItems = 0
        orderitems = {}
        order = {}
    context = {'orderitems' : orderitems,'order' : order,'cartItems' : cartItems,'item' : item}
    
    return render(request,'website_templates/shop-single.html',context=context)



def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        orderitems = order.orderitem_set.all()
        cartItems = order.get_cart_items
        print('orderitems:' , orderitems)
        return render(request,'website_templates/cart.html',{'orderitems' : orderitems,'order' : order,'cartItems' : cartItems})
    else:
        return render('/')



def checkout_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        orderitems = order.orderitem_set.all()
        print('orderitems:' , orderitems)
        return render(request,'website_templates/checkout.html',{'orderitems' : orderitems,'order' : order})
    else:
        return render('/')
    
def updateItem(request):
    print(request.method)  # Debug print to check the request method
    print(request.body)    # Debug print to check the request body

    if request.method == 'POST':
        data = json.loads(request.body)
        itemId = data.get('itemId')
        action = data.get('action')
        customer = request.user.customer
        item = Item.objects.get(id=itemId)
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order,item=item)
        
        if action == 'add':
            orderItem.quantity = orderItem.quantity + 1
        elif action == 'remove':
            orderItem.quantity = orderItem.quantity - 1
        
        orderItem.save()
        
        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('success', safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
def search_view(request):
    items = Item.objects.filter(status=1)  # Initial queryset

    if 's' in request.GET:
        query = request.GET.get('s')
        if query:
            items = items.filter(description__icontains=query) | items.filter(title__contains=query) | items.filter(final_price__contains=query)| items.filter(size__contains=query) | items.filter(color__contains=query) | items.filter(discount__contains=query,off=1)
            
    context = {'items': items}
    print(items)
    return render(request, 'website_templates/shop.html', context=context)





