from django.shortcuts import get_object_or_404 , render
from .models import Product
def get_title(request):
    path = request.path
    path = path[::-1]
    tit = ""
    for i in path:
        if i=='/':
          break
        tit = tit + i
    tit = tit[::-1]
    if len(tit) == 0: 
       tit = "Home"    
    return tit 
# Create your views here.
def products(request):
    pro =  Product.objects.all()
    frm = -1
    to = -1
    if 'searchname' in request.GET:
       name = request.GET['searchname']
       if name:
          pro = pro.filter(name__icontains=name)
    else : name = 'coffe'
    if 'searchpricefrom' in request.GET and 'searchpriceto' in request.GET:
       frm = request.GET['searchpricefrom']
       to = request.GET['searchpriceto']
       if frm and to :
            if frm.isdigit() and to.isdigit():
               pro = pro.filter(price__gte=frm , price__lte = to)
    context = {
        'myprod' : pro,
         'name' : name,
         'tit' : get_title(request)
    }
    return render (request , 'products/products.html' ,context )
def product(request,pro_id):

    context = {
        'pro' : get_object_or_404(Product ,pk=pro_id),
        'tit' : get_title(request)
    }
    return render (request , 'products/product.html' ,context )

def search(request):
    return render (request , 'products/search.html', { 'tit' : get_title(request)})



