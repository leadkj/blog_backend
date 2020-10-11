from django.db import models

# Create your models here.


class Instance(models.Model):
    __url__ = 'instance'
    hostname = models.CharField(max_length=20,verbose_name='主机名称')
    ipaddr = models.CharField(max_length=15,verbose_name='IP地址')
    status = models.BooleanField(verbose_name='是否停用',default=True)
    origin = models.CharField(max_length=11,verbose_name='主机来源',default='其他')
    group = models.CharField(max_length=11,verbose_name='主机组',default='默认')


    class Meta:
        verbose_name = '主机实例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hostname

class InstanceAccount(models.Model):
    __url__ = 'account'
    accounttype = models.CharField(max_length=20,verbose_name='账户类型')
    username = models.CharField(max_length=20,verbose_name='用户名')
    password = models.CharField(max_length=50,verbose_name='密码',blank=True,null=True)
    keyfile = models.CharField(max_length=500,verbose_name='sshkey',blank=True,null=True)
    instance = models.ForeignKey(Instance,verbose_name='主机',null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '主机账户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Service(models.Model):
    __url__ = 'service'
    name = models.CharField(max_length=20,verbose_name='服务名称')
    instance = models.ManyToManyField(to="Instance", verbose_name='主机')

    class Meta:
        verbose_name = '软件服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return  self.name
