from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, Group, Permission

class AttacksCategory(models.Model):
    def __str__(self):
        return self.categoryName
    
    categoryName = models.CharField(max_length=100)
    categoryDesc = models.CharField(max_length=500)

class Attacks(models.Model):
    def __str__(self):
        return self.attackName
    
    attackName = models.CharField(max_length=100)
    createDate = models.DateTimeField('date created')
    attackCat = models.ForeignKey(AttacksCategory,on_delete=models.CASCADE)
    attackDesc = models.CharField(max_length=1000,null=True)
    drsLevel = models.IntegerField(validators=[MaxValueValidator(7),MinValueValidator(0)],null=True)

# class Users(AbstractUser):
#     def __str__(self):
#         return self.username
    
#     username = models.CharField(max_length=150, unique=True)
#     name = models.CharField(max_length=150, null=True)
#     surname = models.CharField(max_length=150, null=True)
#     mail = models.EmailField(max_length=50, null=True)
#     password = models.CharField(max_length=128)

