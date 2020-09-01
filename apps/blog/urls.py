# @Time  :  2020/8/28 14:56
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  urls


from django.urls import path

from blog import views

urlpatterns = [
    # path('article/gt/', views.ArticleModelViewSets.as_view({'get': 'readGten'})),
    # # path('api/v1/article/<pk>/',views.ArticleModelViewSets.as_view({'put':'updateLike'})),
    # # # ReadOnlyModelViewSet
    # # path(r'api/v1/article/', blogViews.ArticleModelViewSets.as_view({'get': 'list'})),
    # # path('api/v1/article/<pk>/', blogViews.ArticleModelViewSets.as_view({'get': 'retrieve'})),
    #
    # # ModelViewSet
    # path('article/', views.ArticleModelViewSets.as_view({'get': 'list', 'post': 'create'})),
    # path('article/<pk>/',
    #      views.ArticleModelViewSets.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]

from rest_framework.routers import SimpleRouter, DefaultRouter

# 1创建路由对象
router = DefaultRouter()

# 2注册视图集
router.register('articles', views.ArticleModelViewSets, basename='article')  # articles 是路由开头
router.register('tags',views.TagModelViewSets,basename='tags')
router.register('categorys',views.CategoryModelViewSets,basename='categorys')
urlpatterns += router.urls

# 测试
# print(urlpatterns)
