from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

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