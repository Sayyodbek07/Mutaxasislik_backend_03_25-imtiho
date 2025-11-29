from django.db import models
from django.core.validators import MinValueValidator

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(Author, max_length=225)
    genres = models.ManyToManyField(Genre)
    published_year = models.PositiveIntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    copies_available = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
