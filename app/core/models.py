"""
Database Models
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """ Manager for Users """
    def create_user(self, email, password=None, **extra_fields):
        """ Create, save and return a new User """
        user = self.model(email=self.normalize_email(email), **extra_fields)

        if not email:
            raise ValueError('User must have a valid email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Create, save and return a new superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User in the System """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Question(models.Model):
    """ Model for Questions """
    text = models.TextField()
    possible_answers = models.JSONField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    """ Model for Answers """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.value


class Report(models.Model):
    """ Model for Reports """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        return f"Report for {self.user.email}"

    def add_answer(self, answer):
        """ Add an answer to the report """
        self.answers.add(answer)