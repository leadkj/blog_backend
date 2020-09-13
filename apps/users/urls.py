# @Time  :  2020/8/28 14:56
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  urls


from django.urls import path

from users import views
from rest_framework.routers import SimpleRouter, DefaultRouter

# 1创建路由对象
router = DefaultRouter()


urlpatterns = [

]



# 2注册视图集
router.register('users', views.UserModelViewSet, basename='users')  # users 是路由开头
urlpatterns += router.urls


print(urlpatterns)