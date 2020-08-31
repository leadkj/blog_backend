from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserInfo(AbstractUser):
    '''Userinfo Molde

    '''
    nick_name = models.CharField(max_length=20, verbose_name='昵称', default='小脑斧')
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), max_length=5, default='female',
                              verbose_name='性别')
    brithday = models.DateField(verbose_name='生日', default='1900-01-01')
    headimg = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        # ordering = ['pk']

    def __str__(self):
        return '{}({})'.format(self.username, self.nick_name)
