from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Account(models.Model):
    phone_num = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=128, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class InvalidatedToken(models.Model):
    token = models.CharField(max_length=512, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, 
                                      help_text='주기적으로 삭제 필요 or redis exp 사용')

