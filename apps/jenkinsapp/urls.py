# @Time  :  2020/8/28 14:56
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  urls


from django.urls import path
from jenkinsapp import views
from rest_framework.routers import SimpleRouter, DefaultRouter

# 1创建路由对象
router = DefaultRouter()

urlpatterns = [
    # path('url/',views.func),
]



# 2注册视图集
router.register('jobs', views.JobModelViewSet, basename='jobs')  # articles 是路由开头
router.register('jobhistorys',views.JobHistoryModelViewSet,basename='jobhistorys')
urlpatterns += router.urls

# 测试
print(urlpatterns)
