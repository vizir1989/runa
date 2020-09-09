from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)
    parent = models.CharField(max_length=250)
