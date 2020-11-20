from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Group(models.Model):
   name = models.CharField(max_length=100, unique=True)
   password = models.CharField(max_length=30)
   users = models.ManyToManyField(User)
   admin = models.ForeignKey(User, on_delete=models.CASCADE)

   def __str__(self):
      return self.name


class Category(models.Model):
   name = models.CharField(max_length=100)
   group = models.ForeignKey(Group, on_delete=models.CASCADE)

   class Meta:
      unique_together = ["name", "group"]

   def __str__(self):
      return f"{self.name}"


class Bill(models.Model):
   name = models.CharField(max_length=100)
   date = models.DateField(default=timezone.now)
   edited = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   category = models.ForeignKey(Category, on_delete=models.CASCADE)
   amount = models.FloatField()
   discription = models.TextField(null=True, blank=True)
   group = models.ForeignKey(Group, on_delete=models.CASCADE)

   def __str__(self):
      return self.name