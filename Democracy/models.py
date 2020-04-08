from django.db import models
from django.contrib.auth.models import AbstractUser


class Custom_User_Model(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Opinion(models.Model):
    username=models.ForeignKey(Custom_User_Model,on_delete=models.CASCADE)
    code_id=models.CharField(max_length=100)
    Yes=models.BooleanField(default=False)
    No=models.BooleanField(default=False)
    Do_Not_Know=models.BooleanField(default=False)
    Comment=models.TextField()

    def __str__(self):
        return self.code_id



class UserVote(models.Model):
    username=models.ForeignKey(Custom_User_Model,on_delete=models.CASCADE)
    code_id=models.ForeignKey(Opinion,on_delete=models.CASCADE)
    Yes = models.BooleanField(default=False)
    No = models.BooleanField(default=False)
    Do_Not_Know = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username) + "  " + str(self.code_id) + "  Vote"




class CodeVote(models.Model):
    code_id=models.CharField(max_length=100)
    yes=models.IntegerField(default=0)
    no=models.IntegerField(default=0)
    do_not_know=models.IntegerField(default=0)

    def __str__(self):
        return self.code_id + "  " + "Vote  Count"




