from datetime import datetime

from django.db import models

# Create your models here.

class JenkinsModel(models.Model):
    __url__ = 'jenkins'
    name = models.CharField(max_length=20,verbose_name='Job名称')
    color = models.CharField(max_length=10,verbose_name="状态颜色")
    description = models.CharField(max_length=50,verbose_name="描述",default='')
    buildable = models.BooleanField(verbose_name='是否可用')
    healthReport = models.IntegerField(blank=True,null=True,verbose_name='整体构建评分')
    inQueue = models.BooleanField(verbose_name="是否在队列中")
    keepDependencies = models.BooleanField()
    firstBuild = models.IntegerField(blank=True,null=True,verbose_name="第一次构建")
    lastBuild = models.IntegerField(blank=True,null=True,verbose_name="最后一次稳定构建")
    lastCompletedBuild = models.IntegerField(blank=True,null=True,verbose_name="最后一次完整构建")
    lastFailedBuild = models.IntegerField(blank=True,null=True,verbose_name="最后一次失败构建")
    lastStableBuild = models.IntegerField(blank=True,null=True,verbose_name="最后一次稳定构建")
    lastSuccessfulBuild = models.IntegerField(blank=True,null=True,verbose_name="最后一次成功构建")
    lastUnstableBuild = models.IntegerField(blank=True,null=True,verbose_name="最后一次不稳定构建")
    lastUnsuccessfulBuild = models.IntegerField(blank=True,null=True,verbose_name="最后一次不成功构建")
    nextBuildNumber = models.IntegerField(blank=True,null=True,verbose_name="下一次构建号")
    params = models.CharField(blank=True,null=True,max_length=500,verbose_name="Job参数")
    jenkinsfile_url = models.CharField(blank=True,null=True,max_length=100,verbose_name="JenkinsfileURL")
    credid = models.CharField(blank=True,null=True,max_length=100,verbose_name='凭据ID')
    jenkinsfilename = models.CharField(blank=True,null=True,max_length=20,verbose_name="JenkinsfileName")
    ctime = models.DateTimeField(verbose_name='创建时间',default=datetime.now)
    class Meta:
        verbose_name = "持续集成"
        verbose_name_plural = verbose_name  # verbose_name_plural是复数形式，会在verbose_name 后加s

    def __str__(self):
        return self.name

class JobHistoryModel(models.Model):
    __url__ = 'jobhistory'
    jobname = models.CharField(max_length=20,verbose_name="job名称")
    building = models.BooleanField(verbose_name="是否正在构建")
    description = models.CharField(blank=True,null=True,max_length=50, verbose_name="描述")
    displayName = models.CharField(max_length=20,verbose_name="名称")
    duration = models.BigIntegerField(verbose_name="构建持续时间")
    fullDisplayName = models.CharField(max_length=20,verbose_name="全名")
    jid = models.IntegerField(verbose_name="jid")
    number = models.IntegerField(verbose_name="构建号")
    queueId = models.IntegerField(verbose_name="队列中的ID")
    result = models.CharField(max_length=20,verbose_name="构建结果")
    timestamp = models.BigIntegerField(verbose_name="构建开始时间")
    nextBuild = models.IntegerField(blank=True,null=True,verbose_name="下一个构建版本号")
    previousBuild = models.IntegerField(blank=True,null=True,verbose_name="上一个构建版本号")


    class Meta:
        verbose_name="构建历史"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.number