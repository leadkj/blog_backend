from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.Pagination import StandardResultsSetPagination
from .models import  UserInfo
from .serializers import UserInfoModelSerializer


class UserModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoModelSerializer

    filterset_fields = ['username','nick_name']
    pagination_class = StandardResultsSetPagination
    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action == 'list' or self.action == 'retrieve':
    #         permission_classes = [AllowAny]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    @action(methods=['PUT'],detail=True)
    def modifyPass(self,request,pk):
        print(request.data)
        user = UserInfo.objects.get(id=pk)
        user.set_password(request.data['password'])
        user.save()
        return Response({"status":200,"message":"修改成功"})