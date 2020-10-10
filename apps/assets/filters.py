# @Time  :  2020/8/29 12:27
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  filters


import django_filters

from .models import Instance

class InstanceFilters(django_filters.FilterSet):
#    name = django_filters.CharFilter(lookup_expr='iexact')  # iexact表示精确匹配, 并且忽略大小写
    hostname = django_filters.CharFilter(lookup_expr='icontains')
    ipaddr = django_filters.NumberFilter(lookup_expr='exact')

    # price__lte = django_filters.NumberFilter('price', lookup_expr='lte') #lte表示小于
    # price__gte = django_filters.NumberFilter('price', look_expr='gte')  # gte表示大于
    class Meta:
        model = Instance  # 模型
        fields = ['hostname','ipaddr']