from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    email=models.EmailField(unique=True)
    password=models.CharField(max_length=256)
    username=models.CharField(max_length=256,blank=True)
    private_key=models.CharField(max_length=1024,blank=True)
    public_key=models.CharField(max_length=1024,blank=True)
    blockchain=models.TextField(blank=True)


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=["username"]

class Blockchain(models.Model):
    totalblockchain=models.TextField(blank=True)
    open_transactions=models.TextField(blank=True)
