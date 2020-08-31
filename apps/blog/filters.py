# @Time  :  2020/8/29 12:27
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  filters


import django_filters

from .models import Article

class ArticleFilters(django_filters.FilterSet):
#    name = django_filters.CharFilter(lookup_expr='iexact')  # iexact表示精确匹配, 并且忽略大小写
    name = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.NumberFilter(lookup_expr='exact')
    tag = django_filters.NumberFilter(lookup_expr='exact')
    # author = django_filters.CharFilter(lookup_expr='icontains')  # icontains表示模糊查询（包含），并且忽略大小写
    read__lte = django_filters.NumberFilter(field_name="read",lookup_expr='lte')
    read__gte = django_filters.NumberFilter(field_name="read",lookup_expr='gte')

    # price__lte = django_filters.NumberFilter('price', lookup_expr='lte') #lte表示小于
    # price__gte = django_filters.NumberFilter('price', look_expr='gte')  # gte表示大于
    class Meta:
        model = Article  # 模型
        fields = ['name','category','content','read__lte',"read__gte"]