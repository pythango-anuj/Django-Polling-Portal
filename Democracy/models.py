from django.db import models
from django.contrib.auth.models import AbstractUser


class Custom_User_Model(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Vote(models.Model):
    user_id = models.IntegerField(unique=True, default=0)
    yes = models.IntegerField(default=0)
    no = models.IntegerField(default=0)
    do_not_know = models.IntegerField(default=0)



class Laws(models.Model):
    law_code = models.IntegerField(null=True)
    user = models.ForeignKey(Custom_User_Model, on_delete=models.CASCADE)
