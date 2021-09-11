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
            errors['firstname_len'] = "nombre debe tener al menos 4 caracteres de largo";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "solo letras en nombreporfavor"

        if len(postData['password']) < 8:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors

class TripManager(models.Manager):
    def basic_valid(self,postData):
        errors = {}
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

