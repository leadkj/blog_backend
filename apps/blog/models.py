from datetime import datetime

from django.db import models
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import UserInfo


# Create your models here.

# 博文分类
class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='文章类别')
    desc = models.CharField(max_length=50, verbose_name='类别描述', null=True, blank=True)
    ctime = models.DateTimeField(verbose_name='创建时间', default=datetime.now)

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name  # verbose_name_plural是复数形式，会在verbose_name 后加s

    def __str__(self):
        return self.name


class Article(models.Model):
    '''
    博文
    '''
    name = models.CharField(max_length=20, verbose_name='文章名称')
    desc = models.CharField(max_length=30, verbose_name='描述', null=True, blank=True)
    publish = models.DateField(verbose_name='出版时间')
    content = RichTextUploadingField(verbose_name='文章内容')
    read = models.IntegerField(verbose_name='浏览量', default=0)
    like = models.IntegerField(verbose_name="点赞", default=0)
    original = models.BooleanField(verbose_name="是否原创")
    author = models.ForeignKey(UserInfo, verbose_name='作者', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, verbose_name='文章分类', null=True, blank=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(to="Tag", verbose_name='标签')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name  # verbose_name_plural 名称复数形式

        ordering = ['-publish']  # 排序

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''
    标签
    '''
    name = models.CharField(max_length=20, verbose_name="标签名称")

    # article = models.ForeignKey(Article,verbose_name="文章",on_delete=models.CASCADE)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name
