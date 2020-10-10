from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from assets.filters import InstanceFilters
from assets.models import Instance
from assets.serializers import InstanceModelSerializer
from utils.Pagination import StandardResultsSetPagination


class InstanceModelViewSets(ModelViewSet):
    queryset = Instance.objects.all()
    serializer_class = InstanceModelSerializer

    # 自定义过滤器
    filter_class = InstanceFilters
    search_fields = ['name', 'read', 'content']

    #分页
    pagination_class = StandardResultsSetPagination