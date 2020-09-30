import os
import json
from django.apps import apps
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from djproject.settings import BASE_DIR


class MenuList(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        """
        #获取后台列表菜单
        :param request:
        :return:
        """
        APPS_PATH = os.path.join(BASE_DIR, 'apps')
        apps_list = os.listdir(APPS_PATH)
        meunlist = []
        for i in range(1,len(apps_list)+1):
            tmp = {}
            name = apps.get_app_config(apps_list[i-1]).verbose_name
            tmp['id'] = i
            tmp['menu'] = name
            tmp['submenus'] = []
            models = list(apps.get_app_config(apps_list[i-1]).get_models())
            for j in range(1,len(models)+1):
                mtmp = {}
                mtmp['id'] = j
                mtmp['name'] = models[j-1]._meta.verbose_name
                mtmp['path'] = models[j-1].__url__
                tmp['submenus'].append(mtmp)
            meunlist.append(tmp)
        return Response({"data":meunlist,"status":200})
