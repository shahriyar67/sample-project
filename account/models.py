from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    is_author = models.BooleanField(default=False, verbose_name="وضعیت نویسندگی")
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    def __str__(self):
        # return self.first_name+""+self.last_name
       return self.username