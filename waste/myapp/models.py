from django.db import models
from django.contrib.auth.models import AbstractUser 


class Login(AbstractUser): 
  userType = models.CharField( max_length=50 )
  viewPass = models.CharField( max_length=100, null=True, blank=True )
  
  def __str__(self): return self.username