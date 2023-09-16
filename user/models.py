from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, verbose_name="用户名")
    user_password = models.CharField(max_length=50, verbose_name="密码")
