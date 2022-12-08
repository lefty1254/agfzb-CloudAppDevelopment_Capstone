from django.db import models
import datetime


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return "Name: " + self.name + "," + \
            "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    # - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    # - Name
    name = models.CharField(null=False, max_length=100)
    # - Dealer id, used to refer a dealer created in cloudant database
    dealer_id = models.IntegerField()
    # - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    type_choices = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]
    car_type = models.CharField(
        null=False,
        max_length=20,
        choices=type_choices
    )
    # - Year (DateField)
    YEAR_CHOICES = [(y,y) for y in range(1950, datetime.date.today().year+3)]
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    # - Any other fields you would like to include in car model
    # - __str__ method to print a car make object
    def __str__(self):
        return f'Car Make: {self.car_make.name}, Model: {self.name}, Dealer Id: {self.dealer_id}, Type: {self.car_type}, Year: {self.year}'


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, id, purchase_date=None, sentiment=None, car_make=None, car_model=None, car_year=None):
        # review dealership
        self.dealership = dealership
        # review name
        self.name = name
        # was car purchased
        self.purchase = purchase
        # review details
        self.review = review
        # purchased date for car
        self.purchase_date = purchase_date
        # car make for review
        self.car_make = car_make
        # car model for review
        self.car_model = car_model
        # car year
        self.car_year = car_year
        # review sentiment
        self.sentiment = sentiment
        # review id
        self.id = id
    def __str__(self):
        return f'Dealership: {self.dealership}, name: {self.name}, purchase: {self.purchase}, review sentiment: {self.sentiment},\nreview: {self.review}'

