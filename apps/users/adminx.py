# @Time  :  2020/8/22 11:35
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  adminx.py

import xadmin
from xadmin import views
# from .models import  UserInfo
#
# class UserInfoAdmin(object):
#     list_display = ['nick_name','gender','brithday']
#

class BaseSetting(object):
    enable_themes = True #打开主题功能
    use_bootswatch = True #

class GlobalSetting(object):
    site_title = "我的博客系统" #站点标题
    site_footer = "我的博客系统" #站点底部信息
    menu_style = "accordion" #左边菜单导航折叠

# xadmin.site.register(UserInfo,UserInfoAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)