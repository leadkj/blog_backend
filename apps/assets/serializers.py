# @Time  :  2020/8/28 11:32
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  serializers

from rest_framework import serializers
from assets.models import Instance


class InstanceModelSerializer(serializers.ModelSerializer):
    '''
    主机实例序列化器
    '''

    # token = serializers.CharField(max_length=11,min_length=11,label='验证码') #额外添加字段，model中没有的字段

    class Meta:
        model = Instance  # 绑定模型类
        fields = "__all__"  # 默认列出所有字段


