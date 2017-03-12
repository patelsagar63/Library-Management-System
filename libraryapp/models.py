from django.db import models
import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Libuser(User):
    PROVINCE_CHOICES = (
        ('AB','Alberta'),  # The first value is actually stored in db, the second is descriptive
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    phone = models.IntegerField(null=True)
    postalcode = models.CharField(max_length=7, blank=True, null=True)
    # model_pic = models.ImageField()

    def __str__(self):
        return self.username +' from ' + self.province

class Libitem(models.Model):
    TYPE_CHOICES = (
        ('Book', 'Book'),
        ('List_of_Books', 'List_of_Books'),
        ('DVD','DVD'),
        ('Other', 'Other'),
    )
    title = models.CharField(max_length=100)
    itemtype = models.CharField(max_length=6, choices=TYPE_CHOICES, default='Book')
    checked_out=models.BooleanField(default=False)
    user=models.ForeignKey(Libuser, default=None, null=True, blank=True)
    duedate=models.DateField(default=None, null=True, blank=True)
    last_chkout = models.DateField(default=None, null=True, blank=True)
    date_acquired = models.DateField(default=datetime.date.today())
    # pubyr = models.IntegerField()
    pubyr = models.IntegerField(validators=[MinValueValidator(1900),
                                          MaxValueValidator(2016)])
    num_chkout = models.IntegerField(default=0)

    def overdue(self):
        if self.checked_out == True:
            if self.duedate.__le__(datetime.date.today()) :
                return "Yes"
            else:
                 return  'NO'


class Book(Libitem):
    CATEGORY_CHOICES = (
        (1, 'Fiction'),
        (2, 'Biography'),
        (3, 'Self Help'),
        (4, 'Education'),
        (5, 'Children'),
        (6, 'Teen'),
        (7, 'Other'),
    )
    author = models.CharField(max_length=100)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)

    def __str__(self):
        return self.title + ' by ' + self.author


class Dvd(Libitem):
    RATING_CHOICES = (
        (1, 'G'),
        (2, 'PG'),
        (3, 'PG-13'),
        (4, '14A'),
        (5, 'R'),
        (6, 'NR'),
    )
    maker = models.CharField(max_length=100)
    duration = models.IntegerField(max_length=100)
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    def __str__(self):
        return self.title + ' by ' + self.maker

class List_of_Books(Libitem):
    b= models.ForeignKey(Book, default=None, null=True, blank=True)
    def __str__(self):
        return self.title + ' by ' + self.author

class Suggestion(models.Model):

    TYPE_CHOICES = (
        (1, 'Book'),
        (2,'DVD'),
        (3, 'Other'),
    )
    title = models.CharField(max_length=100)
    pubyr = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(default=1, choices=TYPE_CHOICES)
    cost = models.IntegerField()
    num_interested = models.IntegerField()
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.title
