import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request,'djangoapp/about.html',{}) 
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request,'djangoapp/contact.html',{})

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('djangoapp:index')
    #     else:
    #         context['message'] = "Invalid username or password."
    #         return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    # else:
    #     return render(request, 'onlinecourse/user_login_bootstrap.html', context)
# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/b7930494-260b-49a3-9dd3-393eb7245020/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = {'dealerships':dealerships}

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}

    url = "https://us-south.functions.appdomain.cloud/api/v1/web/b7930494-260b-49a3-9dd3-393eb7245020/dealership-package/get-review"
    

    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    if reviews:
        context = {'reviews' : reviews}
    return render(request, 'djangoapp/dealer_details.html', context)

# ...

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == 'GET':
        return render(request, 'djangoapp/add_review.html', {'dealerId':dealer_id})
    elif request.method == 'POST':
        review = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/b7930494-260b-49a3-9dd3-393eb7245020/dealership-package/post-review"
        print(request.POST)
        

        review['dealership']=dealer_id
        review['id'] = request.POST['id']
        review['name'] = request.POST['name']
        review['review'] = request.POST['review']
        if request.POST['purchace']=='1':
            review['purchace'] = True
        else:
            review['purchace'] = False
        if len(request.POST['purchace_date'])>0:
            review['purchace_date'] = request.POST['purchace_date']
        if len(request.POST['car_make'])>0:
            review['car_make'] = request.POST['car_make']
        if len(request.POST['car_model'])>0:
            review['car_model'] = request.POST['car_model']
        if len(request.POST['car_year'])>0:
            review['car_year'] = request.POST['car_year']

        json_payload= {'review' : review}
        response = post_request(url=url, json_payload=json_payload,request=request, dealerId=dealer_id)
        return HttpResponse(response)
        
