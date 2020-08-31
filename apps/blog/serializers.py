# @Time  :  2020/8/28 11:32
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  serializers

from rest_framework import serializers
from blog.models import Article, Category, Tag
from users.serializers import UserInfoModelSerializer


class CategoryModelSerializer(serializers.ModelSerializer):
    '''
    分类序列化器
    '''

    # token = serializers.CharField(max_length=11,min_length=11,label='验证码') #额外添加字段，model中没有的字段

    class Meta:
        model = Category  # 绑定模型类
        fields = "__all__"  # 默认列出所有字段


class TagModelSerializer(serializers.ModelSerializer):
    '''
    标签序列化器
    '''


    class Meta:
        model = Tag  # 绑定模型类
        fields = "__all__"  # 默认列出所有字段


class ArticleModelSerializer(serializers.ModelSerializer):
    '''
    文章序列化器
    '''
    # token = serializers.CharField(max_length=11,min_length=11,label='验证码') #额外添加字段，model中没有的字段

    tag = TagModelSerializer(many=True)  # 子序列化，多对多情况
    category = CategoryModelSerializer()  # 子序列话，article 一对多 category
    author = UserInfoModelSerializer()

    class Meta:
        model = Article  # 绑定模型类
        fields = "__all__"  # 默认列出所有字段
        extra_kwargs = {  # 默认不满足要求的字段处理,比如整型字段read，阅读量不可能为负数
            "read": {
                "max_value": 999999,
                "min_value": 0
            },
            "like": {
                "max_value": 999999,
                "min_value": 0
            }
        }
