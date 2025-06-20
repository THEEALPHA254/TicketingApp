from django.db import models

# custom user model
class User(models.Model):
    user_type = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    contact = models.CharField(max_length=15, blank=True) 
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return self.username

