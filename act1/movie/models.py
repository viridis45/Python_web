# act1 > movie > models.py

from django.db import models

class Movies(models.Model):
    title = models.CharField(max_length=40)
    title_en = models.TextField(max_length=40)
    audience = models.IntegerField()
    open_date = models.DateField(auto_now=False)
    genre = models.TextField(max_length=10)
    watch_grade = models.TextField(max_length=8)
    score = models.IntegerField()
    poster_url = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title