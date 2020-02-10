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
    unregister_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    # Documents
    id_card_path = models.CharField(max_length=255, null=True, unique=True)
    pro_card_path = models.CharField(max_length=255, null=True, unique=True)


class Email(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)
    validated = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False)
    address = models.CharField(max_length=255, unique=True)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    address_type_id = models.BigIntegerField()


# "Facturation" "Domicile"
class AddressType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, unique=True)


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255, unique=True)


class UserRole(models.Model):
    user_id = models.CharField(max_length=255)
    role_id = models.CharField(max_length=255)

# Facturation
# payment_first_name = models.CharField(max_length=255)
# payment_last_name = models.CharField(max_length=255)
# payment_address = models.CharField(max_length=255)
# payment_city = models.CharField(max_length=255)
# payment_zipcode = models.CharField(max_length=255)
# payment_counter = models.CharField(max_length=255)
