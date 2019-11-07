from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=20)
    email = models.TextField(max_length =20)
    birthday = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()

    def __str__(self):
        return self.name