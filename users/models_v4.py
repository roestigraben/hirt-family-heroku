from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.email


class Person(models.Model):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.IntegerField(default=1900, blank=True, null=True)
    date_of_death = models.IntegerField(default=1900, blank=True, null=True)
    x_pos = models.IntegerField(default=0, blank=True, null=True)
    y_pos = models.IntegerField(default=0, blank=True, null=True)
    thumbnail = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '{} {} :    {}'.format(self.first_name, self.last_name, self.city)


class Relation(models.Model):
   parent = models.ForeignKey(Person, on_delete=models.CASCADE)
   child = models.ForeignKey(Person, related_name='+', on_delete=models.CASCADE, default=0)

   def __str__(self):
        return '{} {}  -->   {}  {}'.format(self.parent.first_name, self.parent.last_name, self.child.first_name, self.child.last_name)
