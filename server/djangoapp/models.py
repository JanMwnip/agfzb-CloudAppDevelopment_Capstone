import sys
from django.db import models
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    make_name = models.CharField(null=False, max_length=30, default='name')
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.make_name + "," + \
               "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    make_name = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    model_name = models.CharField(null=False, max_length=30, default='name')
    dealer_id = models.IntegerField(default=0)
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
    ]
    car_type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    year=models.DateField(null=False)

    def __str__(self):
        return "Make: " + str(self.make_name) + "," + \
               "Model: " + self.model_name + "," + \
               "Dealer ID: " + str(self.dealer_id) + "," + \
               "Type: " + self.car_type + "," + \
               "Year of Manufacture: " + str(self.year)

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

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id): 
        # Review dealership
        self.dealership = dealership
        # Review name
        self.name = name
        # Review purchase
        self.purchase = purchase
        # Review review
        self.review = review
        # Review purchase_date
        self.purchase_date = purchase_date
        # Review car_make
        self.car_make = car_make
        # Review car_model
        self.car_model = car_model
        # Review car_year
        self.car_year = car_year
        # Review sentiment
        self.sentiment = sentiment
        # Review id
        self.id = id

    def __str__(self):
        return "Dealership: " + self.name