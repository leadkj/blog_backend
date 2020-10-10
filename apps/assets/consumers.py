import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json, base64, os
import paramiko
from threading import Thread
from django.utils.six import StringIO
from django.conf import settings
from django.http.request import QueryDict
from .models import Instance


class ConsoleConsumer(WebsocketConsumer):

    def connect(self):
        self.ipaddr = self.scope['url_route']['kwargs'].get('ipaddr')
        self.accept()
        # 建立SSH连接
        self.ssh = SSHBridge(websocket=self, simpleuser='test')
        # pri00nt('【WS  --SSHBridge-->  SSH】连接SSH参数：', ssh_connect_dict)
        account = Instance.objects.get(ipaddr=self.ipaddr).instanceaccount_set.first()
        self.ssh.connect(**{
            'host': self.ipaddr,
            'user': account.username,
            'pwd': account.password
        })

    def disconnect(self, close_code):
        self.ssh.close()

    def receive(self, text_data=None,bytes_data=None):
        # 从WebSocket中接收消息
        text_data = json.loads(text_data)  # json字符串转字典
        # pri00nt('\n\n【Web  --websocket-->  WS】Web终端按键内容通过WebSocket传到后端：', text_data)
        if type(text_data) == dict:
            if text_data.get('Op') == 'stdin':
                data = text_data.get('Data', '')  # 获取前端传过来输入的按键值，并传递给shell
                # pri00nt('【WS  --SSHBridge-->  Func】WebSocket转发SSHBridge：', text_data)
                self.ssh.shell(data=data)
            else:
                cols = text_data['Cols']
                rows = text_data['Rows']
                # 改变通道中终端大小
                self.ssh.resize_pty(cols=cols, rows=rows)
        else:
            # pri00nt('【！！！】收到的数据不是dict类型')
            pass

    def send_message_or_team(self, message):
        self.send(message)


def get_key_obj(pkeyobj, pkey_file=None, pkey_obj=None, password=None):
    if pkey_file:
        with open(pkey_file) as fo:
            try:
                pkey = pkeyobj.from_private_key(fo, password=password)
                return pkey
            except:
                pass
    else:
        try:
            pkey = pkeyobj.from_private_key(pkey_obj, password=password)
            return pkey
        except:
            pkey_obj.seek(0)


class SSHBridge(object):
    """
    桥接WebSocket和ssh
    参考：https://blog.51cto.com/hongchen99/2336087
    """

    def __init__(self, websocket, simpleuser):
        self.websocket = websocket
        self.simpleuser = simpleuser

    def connect(self, host, user, pwd=None, key=None, port=22, timeout=6, term='xterm', pty_width=80, pty_height=24):
        """
        建立SSH连接，放在 self.ssh_channel 通道中，之后直接在通道中交互数据
        :param host:
        :param user:
        :param pwd:
        :param key:
        :param port:
        :param timeout:
        :param term:
        :param pty_width:
        :param pty_height:
        :return:
        """
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if key:
                # 密钥方式认证
                pkey = get_key_obj(paramiko.RSAKey, pkey_obj=key, password=pwd) or \
                       get_key_obj(paramiko.DSSKey, pkey_obj=key, password=pwd) or \
                       get_key_obj(paramiko.ECDSAKey, pkey_obj=key, password=pwd) or \
                       get_key_obj(paramiko.Ed25519Key, pkey_obj=key, password=pwd)
                ssh_client.connect(username=user, hostname=host, port=port, pkey=pkey, timeout=timeout)
            else:
                ssh_client.connect(hostname=host, port=port, username=user, password=pwd, timeout=timeout)
        except Exception as e:
            # pri00nt(e)
            message = json.dumps({'flag': 'fail', 'message': str(e)})
            self.websocket.send_message_or_team(message)
            return

        transport = ssh_client.get_transport()
        # 打开一个通道
        self.ssh_channel = transport.open_session()
        # 获取一个终端
        self.ssh_channel.get_pty(term=term, width=pty_width, height=pty_height)
        # 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
        self.ssh_channel.invoke_shell()

        # 获取ssh连接主机后的返回内容，例如Linux，会显示上次登录等信息，把这些信息通过WebSocket显示到Web终端。
        # 连接建立一次，之后交互数据不会再进入该方法
        for i in range(2):
            recv = self.ssh_channel.recv(1024).decode('utf-8')
            message = json.dumps({'flag': 'msg', 'message': recv})
            # pri00nt('【WS  --websocket-->  Web】建立SSH通道后，返回欢迎信息：', message)
            self.websocket.send_message_or_team(message)

    def close(self):
        message = {'flag': 0, 'message': '关闭WebSocket和SSH连接'}
        # 向WebSocket发送一个关闭消息
        self.websocket.send_message_or_team(json.dumps(message))

        try:
            # 关闭ssh通道
            self.ssh_channel.close()
            # 关闭WebSocket连接
            self.websocket.close()
        except BaseException as e:
            # pri00nt('关闭WebSocket和SSH连接产生异常：', e)
            pass

    def _ws_to_ssh(self, data):
        """
        尝试发送数据到ssh通道，产生异常则关闭所有连接
        """
        try:
            # pri00nt('【Func  --paramiko-->  SSH】WebSocket中的数据发送数据到ssh通道：', data)
            self.ssh_channel.send(data)
        except OSError as e:
            # pri00nt(e)
            self.close()

    def _ssh_to_ws(self):
        try:
            # while True:
            while not self.ssh_channel.exit_status_ready():
                data = self.ssh_channel.recv(1024).decode('utf-8')
                print(data)
                # pri00nt('【SSH  --paramiko-->  Func】获取ssh通道返回的数据：', data)
                if len(data) != 0:
                    message = {'flag': 'msg', 'message': data}
                    # pri00nt('【WS --websocket-->  Web】通过WebSocket把信息发回前端，显示到Web终端：', message)
                    self.websocket.send_message_or_team(json.dumps(message))
                else:
                    break

        except:
            self.close()

    def shell(self, data):
        Thread(target=self._ws_to_ssh, args=(data,)).start()
        Thread(target=self._ssh_to_ws).start()

    def resize_pty(self, cols, rows):
        self.ssh_channel.resize_pty(width=cols, height=rows)
