from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
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