# @Time  :  2020/8/28 23:33
# @Auth  :  weijx
# @Email :  wjx010107@163.com
# @File  :  middlerwares

from django.utils.deprecation import MiddlewareMixin

class MyTest(MiddlewareMixin):

    def process_response(self, request, response):

        response['Access-Control-Allow-Origin']= "*"

        return response
