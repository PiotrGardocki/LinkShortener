from django.db import models

from shortener.appcode.django_models.users_model import UsersDB


class LinksDB(models.Model):
    shortlink = models.CharField(max_length=40, primary_key=True)
    longlink = models.URLField()   # db_index, validators
    password = models.CharField(max_length=30)
    user = models.ForeignKey(UsersDB, on_delete=models.CASCADE, null=True, blank=True)
