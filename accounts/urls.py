from django.urls import path
from . import views
urlpatterns = [
    path('/signin', views.signin, name="signin"),
    path('/signup', views.signup, name="signup"),
    path('/profile', views.profile, name="profile"),
    path('/logout', views.logout, name="logout"),
    path('/fav<int:pro_id>', views.product_fav, name="fav"),
    path('/favorites', views.show_product_favorite, name="favorites"),
]
