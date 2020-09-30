import time

from jenkins import Jenkins
from utils.config import Jenkins_HOST,Jenkins_USER,Jenkins_PASS,Jenkins_USER_TOKEN
import os
import xml.etree.ElementTree as ET
import requests




class JenkinsCredentials:
    '''python-jenkins 模块无法管理Credentials，只能通过requests模块通过抓包数据进行管理，
    这个地方认证不能只用密码，只能使用api-token，获取账号的token'''

    def __init__(self, host, jenkinsUserName, jenkinsToken):
        self.session = requests.Session()
        self.host = host
        self.session.auth = (jenkinsUserName, jenkinsToken)

    def createEOSCredentials(self, userName, password, id, desc):
        url = self.host + "/credentials/store/system/domain/_/createCredentials"
        jsondata = {"": "0", "credentials": {"scope": "GLOBAL", "username": userName, "password": password, \
                                             "$redact": "password", "id": id, "description": desc, \
                                             "stapler-class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl", \
                                             "$class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"}}
        data = {}
        data["json"] = str(jsondata)
        result = self.session.post(url, data=data)

    # 传入值请使用双引号
    def deleteEOSCredentials(self, id):
        url = self.host + "/credentials/store/system/domain/_/credential/" + id + "/doDelete"
        res = self.session.post(url)

    # 传入值请使用双引号
    def updateEOSCredentials(self, userName, passworld, id, des):
        url = self.host + "/credentials/store/system/domain/_/credential/" + id + "/updateSubmit"
        json = {"stapler-class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl",
                "scope": "GLOBAL", "username": userName, "password": passworld, "$redact": "password",
                "id": id, "description": des}
        data = {}
        data["json"] = str(json)
        result = self.session.post(url, data=data)
        print(result.text)

    def searchEOSCredentials(self, id):
        url = self.host + "/credentials/store/system/domain/_/credential/" + id + "/"
        result = self.session.post(url)
        error_top = "The requested resource is not available."
        if error_top in result.text:
            return False
        else:
            return True

    def getAllCredentials(self):
        credentials = []
        url = self.host + "/credentials/store/system/domain/_/"
        result = self.session.get(url)
        from lxml import etree
        htmltree = etree.HTML(result.text)
        trs = htmltree.xpath('//*[@id="main-panel"]/table[1]//tr')
        for i in range(1, len(trs)):
            tmpcds = {}
            id = trs[i].xpath('./td[2]/a/text()')[0]
            name = trs[i].xpath('./td[3]/text()')[0]
            tmpcds['id'] = id
            tmpcds['name'] = name
            credentials.append(tmpcds)
        return credentials


class JenkinsJob():

    def __init__(self,Jenkins_HOST,Jenkins_USER,Jenkins_PASS):
        self.jserver = Jenkins(Jenkins_HOST, username=Jenkins_USER, password=Jenkins_PASS)

    def get_job(self, jobname):
        info = self.jserver.get_job_info(jobname)
        build_pop_keys = ["_class", "actions", "displayName", "displayNameOrNull", "fullDisplayName", "fullName",
                          'url', "property", "queueItem", "concurrentBuild", "resumeBlocked"]
        for bk in build_pop_keys:
            info.pop(bk)
        info['builds'] = [build['number'] for build in info.pop('builds')]
        info['lastBuild'] = info['lastBuild']['number'] if info['lastBuild'] else None
        info['lastCompletedBuild'] = info['lastCompletedBuild']['number'] if info['lastCompletedBuild'] else None
        info['lastFailedBuild'] = info['lastFailedBuild']['number'] if info['lastFailedBuild'] else None
        info['lastStableBuild'] = info['lastStableBuild']['number'] if info['lastStableBuild'] else None
        info['lastSuccessfulBuild'] = info['lastSuccessfulBuild']['number'] if info['lastSuccessfulBuild'] else None
        info['lastUnstableBuild'] = info['lastUnstableBuild']['number'] if info['lastUnstableBuild'] else None
        info['lastUnsuccessfulBuild'] = info['lastUnsuccessfulBuild']['number'] if info[
            'lastUnsuccessfulBuild'] else None
        info['lastUnstableBuild'] = info['lastUnstableBuild']['number'] if info['lastUnstableBuild'] else None
        info['firstBuild'] = info['firstBuild']['number'] if info['firstBuild'] else None
        info['healthReport'] = info['healthReport'][0]['score'] if info['healthReport'] else None
        return info

    def get_job_build(self, jobname, number):
        '''self.get_job 返回的job信息里有builds 包含所有的构建版本号，可用循环调用这个方法获取所有的构建历史'''
        build_info = self.jserver.get_build_info(jobname, number)
        pop_keys = ["_class", "actions", "artifacts", "estimatedDuration", "executor", "keepLog", "url", "changeSets",
                    "culprits"]
        for k in pop_keys:
            build_info.pop(k)
        build_info['jobname'] = jobname
        build_info['jid'] = build_info.pop('id')
        build_info["nextBuild"] = build_info["nextBuild"]['number'] if build_info["nextBuild"] else None
        build_info["previousBuild"] = build_info["previousBuild"]['number'] if build_info["previousBuild"] else None
        # build_info['log'] = jserver.get_build_console_output(job['name'],build_info['number'])
        return build_info

    def create_job(self, name, jenkinsfile_url, credid, jenkinsfilename,job_template):
        # job_template = 'job_template.xml'
        template = ET.parse(job_template)
        root = template.getroot()
        url = next(root.iter('url'))
        url.text = jenkinsfile_url
        credentialsId = next(root.iter('credentialsId'))
        credentialsId.text = credid
        Jenkinsfile = next(root.iter('scriptPath'))
        Jenkinsfile.text = jenkinsfilename
        config_xml = ET.tostring(root,encoding='utf-8')
        res = self.jserver.create_job(name,config_xml.decode('utf-8'))
        print(res)

    def update_job(self, name, jenkinsfile_url, credid, jenkinsfilename):
        # job_template = 'job_template.xml'
        config = self.jserver.get_job_config(name)
        root = ET.fromstring(config)
        url = next(root.iter('url'))
        url.text = jenkinsfile_url
        credentialsId = next(root.iter('credentialsId'))
        credentialsId.text = credid
        Jenkinsfile = next(root.iter('scriptPath'))
        Jenkinsfile.text = jenkinsfilename
        config_xml = ET.tostring(root,encoding='utf-8')
        res = self.jserver.reconfig_job(name,config_xml.decode('utf-8'))
        print(res)

    def job_add_params(self,jobname, params):
        """
            给job增加参数
            :param jobname: job名称
            :param params: 添加参数的信息,字典格式
            :return:
            """
        config = self.jserver.get_job_config(jobname)
        config_xml = ET.fromstring(config)
        ele_iter = config_xml.iter('parameterDefinitions')
        try:
            params_root = next(ele_iter)
            ele_node = '<hudson.model.StringParameterDefinition>' \
                       '<name>%s</name><description>%s</description><defaultValue>%s</defaultValue><trim>false</trim>' \
                       '</hudson.model.StringParameterDefinition>' % (
                           params['name'], params['description'], params['defaultValue'])

            params_ele = ET.fromstring(ele_node)
        except StopIteration as e:
            params_root = config_xml.find('properties')
            ele_node = '<hudson.model.ParametersDefinitionProperty><parameterDefinitions>' \
                       '<hudson.model.StringParameterDefinition><name>%s</name><description>%s</description><defaultValue>%s</defaultValue><trim>false</trim>' \
                       '</hudson.model.StringParameterDefinition></parameterDefinitions>' \
                       '</hudson.model.ParametersDefinitionProperty>' % (
                           params['name'], params['description'], params['defaultValue'])
            params_ele = ET.fromstring(ele_node)
        params_root.append(params_ele)
        new_config = str(ET.tostring(config_xml, 'utf-8'), encoding='utf-8')
        self.jserver.reconfig_job(jobname, new_config)

    def job_remove_params(self,jobname, paramname):
        """
        删除job的某个参数
        :param jobname: job名称
        :param paramname: 要删除的参数name值
        :return:
        """
        config = self.jserver.get_job_config(jobname)
        config_xml = ET.fromstring(config)
        params_root = next(config_xml.iter('parameterDefinitions'))
        ele_iter = config_xml.iter('hudson.model.StringParameterDefinition')
        drop_ele = None
        for param in ele_iter:
            if param.find('name').text == paramname:
                drop_ele = param
                break
        params_root.remove(drop_ele)
        new_config = str(ET.tostring(config_xml, 'utf-8'), encoding='utf-8')
        self.jserver.reconfig_job(jobname, new_config)

    def build_job(self,jobname,params,token):
        self.jserver.build_job(jobname,params,token)

    def delete_job(self,jobname):
        self.jserver.delete_job(name=jobname)

    def job_rename(self,jobname,newname):
        self.jserver.rename_job(jobname,newname)

    def disable_job(self,jobname):
        self.jserver.disable_job(jobname)

    def enable_job(self,jobname):
        self.jserver.enable_job(jobname)

    def get_build_log(self,jobname,number):
        res = self.jserver.get_build_console_output(jobname,number)
        return res

jc = JenkinsCredentials("http://" + Jenkins_HOST, Jenkins_USER, Jenkins_USER_TOKEN)
# jc.createEOSCredentials('jjjj','picanoc1119','','desc')
# cds = jc.getAllCredentials()
# print(cds)
# jc.deleteEOSCredentials('f5d8c615-a667-4264-a775-cc9f9aaf63f1')

# from jenkinsapp.models import JenkinsModel,JobHistoryModel
# jobj = JenkinsJob("http://" +Jenkins_HOST,Jenkins_USER,Jenkins_PASS)
# number = 9
#
# building = True
# while building:
#     res = jobj.jserver.get_build_console_output('aaaaaaaaaaa',number)
#     print(res)
#     time.sleep(3)
#     job = jobj.jserver.get_build_info('aaaaaaaaaaa', number)
#     building = job['building']


# jobj.jserver.build_job()
#
# jobs = jobj.jserver.get_jobs()
# print(jobs)
# for job in jobs:
#     jobdict = jobj.get_job(job['name'])
#     j = Jenkins.objects.create(**jobdict)
#     j.save()

# jobj.create_job('a1233','https://gitee.com/leadkj/Pic_view_app.git','9da17123-3b12-4c17-8542-3b4ab650b6af','hehe')
# res = jobj.get_job('blog_front')
# build = jobj.get_job_build('blog_front',2)
# print(build)
# jobj.job_rename('abcd','abcd1234')
# print(res)
params = {
    'name': 'delete',
    'description': 'hahadesc',
    'defaultValue': 'hehe',
}
# jobj.job_add_params('abcd1234',params)
# jobj.job_remove_params('abcd1234','delete')
# jobj.disable_job('abcd1234')
# jobj.delete_job('abcd1234')