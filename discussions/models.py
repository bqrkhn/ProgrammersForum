from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=1055, default="")
    date = models.DateTimeField(default=datetime.now, blank=True)
    username = models.ForeignKey(User, on_delete=None)
    votes = models.IntegerField(default=0)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Answer(models.Model):
    QID = models.ForeignKey(Question, on_delete=None)
    description = models.CharField(max_length=1055, default="")
    date = models.DateTimeField(default=datetime.now, blank=True)
    username = models.ForeignKey(User, on_delete=None)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.username.username


class Vote(models.Model):
    username = models.ForeignKey(User, on_delete=None)
    QID = models.ForeignKey(Question, on_delete=None, null=True, blank=True)
    AID = models.ForeignKey(Answer, on_delete=None, null=True, blank=True)
    vote = models.BooleanField(default=True)

    class Meta:
        ordering = ['-QID', '-AID']

    def __str__(self):
        if self.QID is not None:
            return str(self.QID.id) + '_' + self.username.username + '_' + str(self.vote)
        else:
            return str(self.AID.id) + '_' + self.username.username + '_' + str(self.vote)
