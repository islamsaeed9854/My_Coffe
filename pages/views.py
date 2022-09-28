from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from products.models import Product 
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
def index(request):
    context = {
      'mypro' : Product.objects.all(),
      'tit' : get_title(request)
    }
    return render(request,'pages/index.html' ,context)


def about(request):
   return render(request  , 'pages/about.html',{ 'tit' : get_title(request)})

def coffe(request):
   return render(request  , 'pages/coffe.html',{ 'tit' : get_title(request)})