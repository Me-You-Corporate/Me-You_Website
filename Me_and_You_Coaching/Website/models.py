from django.db import models

# Create your models here.


class User(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    # Identity
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # Credentials
    password = models.CharField(max_length=255)
    # Crontab action & keep track of user
    registration_date = models.DateTimeField(auto_now_add=True)
    unregister_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    # Documents
    id_card_path = models.CharField(max_length=255)
    pro_card_path = models.CharField(max_length=255)


class Email(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    user_id = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False)
    address = models.CharField(max_length=255)


class Address(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    user_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    address_type_id = models.BigIntegerField()


# "Facturation" "Domicile"
class Address_type(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    type = models.CharField(max_length=255)


class Client:
    user_id = models.CharField(max_length=255, unique=True, primary_key=True)
    test = models.BooleanField()


class Coach:
    user_id = models.CharField(max_length=255, unique=True, primary_key=True)
    test = models.BooleanField()


class Admin:
    user_id = models.CharField(max_length=255, unique=True, primary_key=True)
    test = models.BooleanField()


# Facturation
# payment_first_name = models.CharField(max_length=255)
# payment_last_name = models.CharField(max_length=255)
# payment_address = models.CharField(max_length=255)
# payment_city = models.CharField(max_length=255)
# payment_zipcode = models.CharField(max_length=255)
# payment_counter = models.CharField(max_length=255)
