from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    score = models.PositiveIntegerField(default=0)
    follows = models.ManyToManyField('self', related_name='followers')
