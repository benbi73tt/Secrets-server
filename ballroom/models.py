from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    sur_name = models.CharField(max_length=150, blank=True)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s %s" % (self.last_name, self.first_name, self.sur_name)
        return full_name.strip()


# Create your models here.
class Trainer(models.Model):
    full_name = models.CharField(max_length=255)


class TypeBallroomDancing(models.Model):
    title = models.CharField(max_length=255)
    program = models.CharField(max_length=255)


class Team(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(TypeBallroomDancing, on_delete=models.SET_NULL, null=True)
    founding_date = models.DateField()


class Member(models.Model):
    # TODO можно расширить до User
    lastname = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    image = models.ImageField()
    city = models.CharField(max_length=255)
    level = models.CharField(max_length=255)


class Competition(models.Model):
    title = models.CharField(max_length=255)


class CompetitionProgram(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True)


class Point(models.Model):
    user = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey(CompetitionProgram, on_delete=models.SET_NULL, null=True)
    user_point = models.IntegerField()


class Entry(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
