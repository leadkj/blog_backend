from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    # url(r'^ws/get_build_output/(?P<job_name>[^/]+)/$', consumers.BuildConsumer),
    url(r'^ws/get_console_output/(?P<ipaddr>.+)/$', consumers.ConsoleConsumer),
]
