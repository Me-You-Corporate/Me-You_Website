from django.db import models

# Create your models here.


class User(models.Model):
    # Credentials
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    # Identity
    user_first_name = models.CharField(max_length=255)
    user_last_name = models.CharField(max_length=255)

    # Location
    user_address = models.CharField(max_length=255)
    user_city = models.CharField(max_length=255)
    user_zipcode = models.CharField(max_length=255)  # usually a 5 digits input
    user_country = models.CharField(max_length=255, default="France")  # in first time : France

    # Facturation
    payment_first_name = models.CharField(max_length=255)
    payment_last_name = models.CharField(max_length=255)
    payment_address = models.CharField(max_length=255)
    payment_city = models.CharField(max_length=255)
    payment_zipcode = models.CharField(max_length=255)
    payment_counter = models.CharField(max_length=255)
    # Id
    user_id = models.CharField(max_length=255, primary_key=True)  # change 255 by max length of ZIP + name[5:] + safe[2]

    # Crontab action & keep track of user
    registration_date = models.DateTimeField(auto_now_add=True)
    unregister_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    # Mails
    email_subscribed = models.BooleanField(default=False)  # if false : email non-subscribed
    email_validated = models.BooleanField(default=False)  # if email hasn't be confirmed yet

    # Documents
    id_card_path = models.CharField(max_length=255)
    pro_card_path = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
