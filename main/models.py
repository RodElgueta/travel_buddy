from django.db import models
import re
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 4:
            errors['firstname_len'] = "Name at least 4 characters";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid mail"

        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "Only letters on name pls"

        if len(postData['password']) < 8:
            errors['password'] = "Password at least 8 characters";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "Password and Password confirm dont coincide "

        
        return errors

class TripManager(models.Manager):
    def basic_valid(self,postData):
        errors = {}

        if len(postData['dest']) < 3:
            errors['dest'] = "Your Destiny should have more than 3 letters"
        
        if len(postData['plan']) < 10:
            errors['plan'] = "Your travel Plan should be at least 10 characters"

        if datetime.strptime(postData['date_from'],"%Y-%m-%d").date() < datetime.today().date():
            errors['date'] = "Please Trip start Date Cant be in the past"
        
        if datetime.strptime(postData['date_to'],"%Y-%m-%d").date() < datetime.strptime(postData['date_from'],"%Y-%m-%d").date():
            errors['date'] = "Please Trip to Date Cant be before Trip Start Date"
        
        return errors

class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

class Trips(models.Model):
    plan = models.TextField(max_length=100)
    date_from = models.DateField()
    date_to = models.DateField()
    dest = models.CharField(max_length=100)
    creator = models.ForeignKey(User,related_name="my_trip",on_delete=models.CASCADE)
    travellers = models.ManyToManyField(User,related_name="others_trips")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()

    def __str__(self):
        return f"{self.dest} {self.id}"

    def __repr__(self):
        return f"{self.dest} {self.id}"

