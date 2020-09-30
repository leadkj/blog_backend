import json
import os

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from dwebsocket import require_websocket
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from jenkinsapp.models import JenkinsModel, JobHistoryModel
from jenkinsapp.serializers import JenkinsModelSerializer, JobHistoryModelSerializer
from utils.jenkins_api import JenkinsJob, JenkinsCredentials
from utils.config import Jenkins_USER, Jenkins_HOST, Jenkins_PASS, Jenkins_USER_TOKEN
from utils.Pagination import StandardResultsSetPagination
from djproject.settings import STATIC_URL, BASE_DIR

jenkinsobj = JenkinsJob("http://" + Jenkins_HOST, Jenkins_USER, Jenkins_PASS)
jenkinscrdis = JenkinsCredentials("http://" + Jenkins_HOST, Jenkins_USER, Jenkins_USER_TOKEN)
clinets={}

class JobModelViewSet(ModelViewSet):
    queryset = JenkinsModel.objects.all()
    serializer_class = JenkinsModelSerializer
    pagination_class = StandardResultsSetPagination

    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        job_template = os.path.join(BASE_DIR, 'job_template.xml')
        data = request.data
        print(data['params'])
        try:
            jenkinsobj.create_job(data['name'], data['jenkinsfile_url'], data['credid'], data['jenkinsfilename'],
                                  job_template)
            ###添加参数
            for param in data['params']:
                jenkinsobj.job_add_params(data['name'], param)
            data['params'] = json.dumps(data['params'])
            job_dict = jenkinsobj.get_job(data['name'])
            job_dict.pop('builds')
            job_dict.update(data)
            jm = JenkinsModel.objects.create(**job_dict)
            jm.save()
        except Exception as e:
            print(e)
        return Response(data)

    def update(self, request, *args, **kwargs):
        job = JenkinsModel.objects.get(id=request.data['id'])
        jobparams = json.loads(job.params.replace("'",'"'))
        delparams, addparams = [], []
        if request.data['params'] != jobparams:
            delparams = [p1 for p1 in jobparams if p1 not in request.data['params']]
            addparams = [p2 for p2 in request.data['params'] if p2 not in jobparams]
            job.params = request.data['params']
            job.jenkinsfilename = request.data['jenkinsfilename']
            job.jenkinsfile_url = request.data['jenkinsfile_url']
            job.credid = request.data['credid']
            job.save()

        print(delparams,addparams)
        try:
            if delparams:
                for param1 in delparams:
                    jenkinsobj.job_remove_params(request.data['name'], param1['name'])
            if addparams:
                for param2 in addparams:
                    jenkinsobj.job_add_params(request.data['name'], param2)
            jenkinsobj.update_job(request.data['name'], request.data['jenkinsfile_url'], request.data['credid'],
                                  request.data['jenkinsfilename'])
        except Exception as e:
            print(e)
        return Response(request.data)

    #获取凭据列表
    @action(methods=['GET'], detail=False)
    def get_credentials(self, request):
        credentials = jenkinscrdis.getAllCredentials()
        return Response(credentials)

    #构建项目
    @action(methods=['POST'],detail=False)
    def build_job(self,request):
        jobname = request.data['name']
        job = JenkinsModel.objects.get(name=jobname)
        if request.data['params']:
            params = [ (p['name'],p['defaultValue']) for p in request.data['params']]
        else:
            params = None
        try:
            jenkinsobj.build_job(jobname,params,token=Jenkins_USER_TOKEN)
            jobinfo = jenkinsobj.get_job(jobname)
            job.__dict__.update(**jobinfo)
            job.save()
        except Exception as e:
            print(e)
        return Response(data=None)


class JobHistoryModelViewSet(ModelViewSet):
    queryset = JobHistoryModel.objects.all()
    serializer_class = JobHistoryModelSerializer

    permission_classes = [AllowAny]

