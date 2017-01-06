from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=200)
    cardset = models.CharField(max_length=200)
    num = models.IntegerField()
    foil = models.BooleanField()

    class Meta:
        unique_together = ('name', 'cardset', 'foil')


class Pricing(models.Model):
    card = models.ForeignKey(Card)
    price = models.FloatField()
    date = models.DateField()

    class Meta:
        unique_together = ('card', 'date')
