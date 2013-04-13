from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
  createdBy = models.ForeignKey(User)
  firstName = models.CharField(max_length = 20)
  lastName = models.CharField(max_length = 20)
  email = models.EmailField() 

class Donation(models.Model):
  donor = models.ForeignKey(Donor)
  donation = models.DecimalField(max_digits=15, decimal_places=2)
  date = models.DateField(auto_now_add=True)
