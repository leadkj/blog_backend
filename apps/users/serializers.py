# @Time  :  2020/8/28 11:32
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  serializers

from rest_framework import serializers
from users.models import UserInfo


class UserInfoModelSerializer(serializers.ModelSerializer):
    '''
    Userinfo 序列化器
    '''

    # token = serializers.CharField(max_length=11,min_length=11,label='验证码') #额外添加字段，model中没有的字段

    class Meta:
        model = UserInfo  # 绑定模型类
        # fields = "__all__" #默认列出所有字段
        fields = ['id', 'username', 'nick_name']
