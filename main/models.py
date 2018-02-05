from django.db import models
from django.contrib.auth.models import User
from discussions.models import Question, Answer
from datetime import datetime


# Create your models here.


class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=None, primary_key=True)
    image = models.CharField(max_length=255, default="")
    points = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    hacker_earth_username = models.CharField(max_length=255, default="", blank=True)
    spoj_username = models.CharField(max_length=255, default="", blank=True)
    codechef_username = models.CharField(max_length=255, default="", blank=True)
    hacker_earth_rating = models.IntegerField(default=0)
    spoj_rating = models.IntegerField(default=0)
    codechef_rating = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)


    def __str__(self):
        return self.username.username

class View(models.Model):
    ip = models.CharField(max_length=30, default="")
    time = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=None)

    def __str__(self):
        return self.user.username + " " + self.ip


class Activity(models.Model):
    by_username = models.ForeignKey(User, on_delete=None, related_name='by')
    QID = models.ForeignKey(Question, on_delete=None, null=True, blank=True)
    AID = models.ForeignKey(Answer, on_delete=None, null=True, blank=True)
    vote = models.BooleanField(default=True, blank=True)
    type = models.BooleanField(default=False)
    on_username = models.ForeignKey(User, on_delete=None, null=True, blank=True, related_name='on')
    datetime = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.datetime) + " by " + self.by_username.username

    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ['-datetime']


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=None)
    title = models.CharField(max_length=500, default="")
    description = models.TextField(max_length=5000, default="")
    datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title + " " + self.username.username

    class Meta:
        ordering = ['-datetime']




