import subprocess
import time

from django.http import HttpResponse
from django.shortcuts import render
from dwebsocket.websocket import WebSocket
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
import json
import uuid

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action  # 给自定义方法生成路由信息的装饰器
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from dwebsocket import require_websocket

from .filters import ArticleFilters
from .models import Article, Category, Tag
from .serializers import ArticleModelSerializer, CategoryModelSerializer, TagModelSerializer
from utils import nginx_log
clients = {}


# Create your views here.

# 自定义分页
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


# 文章类视图
class ArticleModelViewSets(CacheResponseMixin, ReadOnlyModelViewSet):
    '''文章类试图
      如果只是前端使用前后端分离方式开发，最好使用ReadOnlyModelViewSet ，我这里后台管理是xadmin,后端不是前后端分离技术
    '''
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer

    # 局部过滤配置
    # filterset_fields = ['category', 'tag']
    # 自定义过滤器
    filter_class = ArticleFilters
    search_fields = ['name', 'read', 'content']

    # 排序 加上之后好像自定的过滤器有问题
    # filter_backends = [OrderingFilter]
    # ordering_fields = ['read','like']
    # 自定义分页
    pagination_class = StandardResultsSetPagination

    # 自定义数据请求 ，比如获取阅读量大于10的文章
    @action(methods=['GET'], detail=False)  # 该方法支持get请求，并且没有参数
    def readGten(self, request):
        # 获取符合条件的数据
        articles = Article.objects.filter(read__gt=10)

        # 创建序列化器对象
        serializer = self.get_serializer(instance=articles, many=True)

        # 返回相应
        return Response(serializer.data)

    # 自定义put方法，修改点赞个数为1000
    @action(methods=['PUT'], detail=True)  # 该方法支持PUT请求，默认有参数
    def updateLike(self, request, pk):
        # 获取文章对象
        # article = Article.objects.get(pk=pk)
        article = self.get_object()
        ldata = request.data.copy()
        like = int(article.like) + int(ldata.get("like"))
        ldata['like'] = like

        # 创建序列化器
        serializer = self.get_serializer(instance=article, data=ldata, partial=True)  # partial为True的时候，put数据不用是所有的字段

        # 校验，入库
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 返回响应
        return Response(ldata, status=201)

    # 自定义put方法，修改阅读量为1000
    @action(methods=['PUT'], detail=True)  # 该方法支持PUT请求，默认有参数
    def updateRead(self, request, pk):
        # 获取文章对象
        # article = Article.objects.get(pk=pk)
        article = self.get_object()
        rdata = request.data.copy()
        read = int(article.read) + int(rdata.get("read"))
        rdata['read'] = read

        # 创建序列化器
        serializer = self.get_serializer(instance=article, data=rdata,
                                         partial=True)  # partial为True的时候，put数据不用是所有的字段

        # 校验，入库
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 返回响应
        return Response(rdata, status=201)


class CategoryModelViewSets(CacheResponseMixin, ReadOnlyModelViewSet):
    '''文章分类视图
    '''
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    # 自定义分页
    pagination_class = StandardResultsSetPagination


class TagModelViewSets(CacheResponseMixin, ReadOnlyModelViewSet):
    '''标签类视图
    '''
    queryset = Tag.objects.all()
    serializer_class = TagModelSerializer
    # 自定义分页
    pagination_class = StandardResultsSetPagination


# 监控所有的socket连接
@require_websocket
def once_echo(request):
    if request.is_websocket():
        userid = str(uuid.uuid1())
        while 1:
            message = request.websocket.wait()
            if message:
                clients[userid] = request.websocket


# 消息发送和推送
def sendmsg(request):
    body = json.loads(request.body)
    msg = body['msg']
    for client in clients:
        data = {'id': '__--__', 'data': msg}
        clients[client].send(json.dumps(data))
    return HttpResponse("ok")


#nginx 访问日志推送
@require_websocket
def push_attack_log(request):
    if request.is_websocket():
        cmd = "/usr/bin/tailf %s" %nginx_log
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while 1:
            # if request.websocket.wait():
            line = popen.stdout.readline()
            time.sleep(3)
            if line:
                request.websocket.send(line)


