# @Time  :  2020/8/22 11:56
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  xadmin

import xadmin

from .models import Category, Article, Tag


class CategoryAdmin(object):
    list_display = ['name', 'desc', 'ctime']
    search_fields = ['name']
    list_filter = ['name', 'desc', 'ctime']


class ArticleAdmin(object):
    list_display = ['name', 'category', 'author', 'desc', 'publish']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'publish', 'category', 'author']


class TagAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Tag, TagAdmin)
