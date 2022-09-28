from cgitb import html
from distutils.log import error
import imp
from multiprocessing import context
from platform import node
from pyexpat.errors import messages
from this import d
from urllib import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import User_Profile
from django.contrib import auth
from products.models import Product
import re


def get_title(request):
    path = request.path
    path = path[::-1]
    tit = ""
    for i in path:
        if i == '/':
            break
        tit = tit + i
    tit = tit[::-1]
    return tit


def signin(request):
    if request.method == 'POST' and "btnlogin" in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
        else:
            messages.error(request, "user name or password invalid")
        return redirect('signin')
    else:
        return render(request, 'accounts/signin.html', {'tit': get_title(request)})


def signup(request):
    if request.method == 'POST' and "btnsignup" in request.POST:
        fname = None
        lname = None
        address = None
        address2 = None
        city = None
        state = None
        zip = None
        email = None
        username = None
        password = None
        terms = None
        is_added = None

        if 'fname' in request.POST:
            fname = request.POST['fname']
        else:
            messages.error(request, "There is error !")
        if 'lname' in request.POST:
            lname = request.POST['lname']
        else:
            messages.error(request, "There is error !")
        if 'address' in request.POST:
            address = request.POST['address']
        else:
            messages.error(request, "There is error !")
        if 'address2' in request.POST:
            address2 = request.POST['address2']
        else:
            messages.error(request, "There is error !")
        if 'city' in request.POST:
            city = request.POST['city']
        else:
            messages.error(request, "There is error !")
        if 'state' in request.POST:
            state = request.POST['state']
        else:
            messages.error(request, "There is error !")
        if 'zip' in request.POST:
            zip = request.POST['zip']
        else:
            messages.error(request, "There is error !")
        if 'username' in request.POST:
            username = request.POST['username']
        else:
            messages.error(request, "There is error !")
        if 'password' in request.POST:
            password = request.POST['password']
        else:
            messages.error(request, "There is error !")
        if 'terms' in request.POST:
            terms = request.POST['terms']
        else:
            messages.error(request, "There is error !")
        if 'email' in request.POST:
            email = request.POST['email']
        else:
            messages.error(request, "There is error !")

        if terms == 'on' and lname and fname and address and address2 and city and state and zip and email and username and password:
            # check if user name is taken
            if User.objects.filter(email=email) or User.objects.filter(username=username).exists():
                messages.error(request, "This user name is taken")
            else:
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                if (re.fullmatch(regex, email)):
                    # add User
                    user = User.objects.create(
                        first_name=fname, last_name=lname, email=email, username=username, password=password)
                    user.save()
                    # add User Profile
                    userprofile = User_Profile.objects.create(
                        user=user, address=address, address2=address2, city=city, state=state, zip_number=zip, email=email)
                    userprofile.save()
                    messages.success(request, "Your Account is Created")
                    is_added = True
                else:
                    messages.error(request, "Invalid Email")

        else:
            messages.error(request, "Check empty fields")

        return render(request, 'accounts/signup.html', {
            'fname': fname,
            'lname': lname,
            'email': email,
            'pass': password,
            'address': address,
            'address2': address2,
            'state': state,
            'city': city,
            'zip': zip,
            'is_added': is_added,
        })
    else:
        return render(request, 'accounts/signup.html', {'tit': get_title(request)})


def profile(request):
    if request.user.is_anonymous:
        return render(request, 'accounts/profile.html', {'tit': get_title(request)})
    profile = User_Profile.objects.get(user=request.user)
    if request.method == 'POST' and "profile" in request.POST:
        if request.POST['fname'] and \
           request.POST['lname'] and request.POST['address'] and request.POST['address2'] and \
           request.POST['state'] and request.POST['zip'] and request.POST['city'] \
           and request.POST['email']:
            request.user.first_name = request.POST['fname']
            request.user.last_name = request.POST['lname']
            profile.address = request.POST['address']
            profile.address2 = request.POST['address2']
            profile.city = request.POST['city']
            profile.state = request.POST['state']
            profile.zip_number = request.POST['zip']
            password = request.POST['password']
            if not password.startswith("pbkdf2_sha256$"):
                request.user.set_password(request.POST['password'])
            request.user.save()
            profile.save()
            auth.login(request, request.user)
            messages.success(request, "your data has been saved")
            return redirect("profile")
        else:
            messages.error(request, "Check you values and Elemnts")
            return redirect("profile")
    else:
        return render(request, 'accounts/profile.html', {'profile': profile, 'tit': get_title(request)})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')


def product_fav(request, pro_id):
    if not request.user.is_anonymous and request.user.is_authenticated:
        pro_fav = Product.objects.get(pk=pro_id)
        if User_Profile.objects.filter(user=request.user, product_fav=pro_fav).exists():
            messages.success(request, "Already Prouduct in the Favourite list")
        else:
            userprofile = User_Profile.objects.get(user=request.user)
            userprofile.product_fav.add(pro_fav)
            messages.success(request, "Prouduct has been added")
        return redirect('/products'+str(pro_id))
    else:
        messages.error(request, "you must be logged in")
        return redirect('signin')


def show_product_favorite(request):
    if not request.user.is_anonymous and request.user.is_authenticated:
        user = request.user
        prof = User_Profile.objects.get(user=user)
        favs = prof.product_fav.all()
        context = {
            'myprod': favs,
            'tit': get_title(request)
        }
        return render(request, 'products/products.html', context)
    else:
        messages.error(request, "you must be logged in")
        return redirect('signin')
