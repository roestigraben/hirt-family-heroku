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
    phone_number = models.CharField(max_length=12, blank=True)
    cell_number = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} :    {}'.format(self.first_name, self.last_name, self.id)


class Relation(models.Model):
   parent = models.ForeignKey(Person, on_delete=models.CASCADE)
   child = models.ForeignKey(Person, related_name='+', on_delete=models.CASCADE, default=0)

   def __str__(self):
        return '{} {}  -->   {}  {}'.format(self.parent.first_name, self.parent.last_name, self.child.first_name, self.child.last_name)

class XtraPhotos(models.Model):
   parent = models.ForeignKey(Person, on_delete=models.CASCADE)
   title = models.CharField(max_length=100, blank=True)
   caption = models.CharField(max_length=100, blank=True)
   source = models.CharField(max_length=50, blank=True, null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
        verbose_name_plural = "Extra Photos"

   def __str__(self):
        return self.title


class XtraInfo(models.Model):
   parent = models.ForeignKey(Person, on_delete=models.CASCADE)
   title = models.CharField(max_length=100, blank=True)
   text = models.TextField(blank=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
        verbose_name_plural = "Extra Information"

   def __str__(self):
        return self.title