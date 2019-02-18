from django.db import models


class UsersDB(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=30)
    token = models.CharField(max_length=30, unique=True, null=True, default=None)
    token_expiration = models.DateTimeField(null=True)
