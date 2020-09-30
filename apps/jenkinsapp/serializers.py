# @Time  :  2020/8/28 11:32
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  serializers

from rest_framework import serializers
from jenkinsapp.models import JenkinsModel,JobHistoryModel


class JenkinsModelSerializer(serializers.ModelSerializer):
    '''
    Job序列化器
    '''
    #自定义序列化字段，定义方法返回字段输出结果，返回字段是方法名get_后面的字符，具体可以查看SerializerMethodField源码
    last_success = serializers.SerializerMethodField(label='最后构建成功时间')
    last_faild = serializers.SerializerMethodField(label='最后构建失败时间')
    last_build_duration = serializers.SerializerMethodField(label='最后构建持续时间')

    class Meta:
        model = JenkinsModel  # 绑定模型类
        fields = "__all__"  # 默认列出所有字段

    def get_last_success(self,obj):
        jh = JobHistoryModel.objects.filter(jobname=obj.name,jid=obj.lastSuccessfulBuild).first()
        if jh:
            return jh.timestamp
        else:
            return None

    def get_last_faild(self,obj):
        jh = JobHistoryModel.objects.filter(jobname=obj.name, jid=obj.lastFailedBuild).first()
        if jh:
            return jh.timestamp
        else:
            return None

    def get_last_build_duration(self,obj):
        jh = JobHistoryModel.objects.filter(jobname=obj.name, jid=obj.lastBuild).first()
        if jh:
            return jh.duration
        else:
            return None
class JobHistoryModelSerializer(serializers.ModelSerializer):
    '''
    构建历史序列化器
    '''

    class Meta:
        model = JobHistoryModel  # 绑定模型类
        fields = "__all__"  # 默认列出所有字段

