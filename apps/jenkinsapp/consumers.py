import time

from channels.generic.websocket import WebsocketConsumer
import json
from jenkinsapp.models import JenkinsModel
from utils.config import Jenkins_HOST, Jenkins_USER, Jenkins_PASS
from utils.jenkins_api import JenkinsJob
jenkinsobj = JenkinsJob("http://" + Jenkins_HOST, Jenkins_USER, Jenkins_PASS)

class BuildConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        jobname = text_data_json['jobname']
        number = jenkinsobj.get_job(jobname)['nextBuildNumber']-1
        building = True
        while building:
            try:
                job = jenkinsobj.jserver.get_build_info(jobname, number)
                building = job['building']
            except Exception as e:
                continue
            res = jenkinsobj.get_build_log(jobname,number)
            print(res)
            time.sleep(3)
            print(building)
            self.send(text_data=json.dumps({
                'output': res,
                'status':building
            }))