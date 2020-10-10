# @Time  :  2020/8/28 14:56
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  urls


from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter

from assets import views

urlpatterns = [

]



# 1创建路由对象
router = DefaultRouter()

# 2注册视图集
router.register('instances', views.InstanceModelViewSets, basename='instances')  # articles 是路由开头

urlpatterns += router.urls

# 测试
print(urlpatterns)
