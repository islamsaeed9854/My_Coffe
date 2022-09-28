from django.urls import path 
from . import views
urlpatterns = [
    path('<int:pro_id>', views.product,name = "product"),
    path('/products', views.products,name = "products"),
    path('/search', views.search,name = "search"),
]