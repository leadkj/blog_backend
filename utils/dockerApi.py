import docker
DOCKER_SERVICE = 'tcp://192.168.10.103:2375' #docker服务所在主机要开启tcp端口，默认是socket连接

class DockerAPI():
    '''
    API 常用方法
    pull,remove_image,push,get_image,search,images,create_*,start
    '''


    def __init__(self,docker_service):
        self.client = docker.APIClient(base_url=docker_service,timeout=20)

    #pull images
    def pull_image(self,image):#传值的时候如果没有指定版本号，默认是latest
        if len(image.split(":"))>1:
            self.client.pull(image,stream=True,decode=True)
        else:
            self.client.pull(image+":latest", stream=True, decode=True)

    def rm_iamge(self,image):
        try:
            if len(image.split(":"))>1:
                self.client.remove_image(image)
            else:
                self.client.remove_image(image+":latest")
            return {"code":0}
        except Exception as e:
            print(e)
            return {"code":1}

    #get_image
    def get_image(self,image):
        try:
            image = self.client.get_image(image)
            with open('image.tgz','wb') as f:
                for chunk in image:
                    f.write(chunk)
        except Exception as e:
            print(e)
            print('image not found')

    #创建容器
    def create_container(self,image,hport,cport):
        c = self.client.create_container(image,
                                         ports=[cport],#容器端口
                                         volumes=['/mnt/data'],#容器路径
                                         host_config=self.client.create_host_config(
                                             port_bindings={cport: ('0.0.0.0', hport)},#cport容器端口，hport主机端口
                                             binds=['/opt/data:/mnt/data',]),#主机路径:容器路径映射
                                         )
        self.client.start(c)

if __name__ == "__main__":
    client = docker.APIClient(base_url=DOCKER_SERVICE, timeout=20)
    print(client.containers(all=True, quiet=False, ))
    ctr = client.create_container('nginx:latest', ports=[80], volumes=['/mnt/data'],
                                  host_config=client.create_host_config(port_bindings={80: ('0.0.0.0', 8004)},
                                                                        binds=['/opt/data:/mnt/data', ]))
    client.start(ctr)
    # client.stop('5b81d41c756f3a1e7acff9b972164b8cbfba240644959fd3d00588a8d04b37ef') #{'Id': '5b81d41c756f3a1e7acff9b972164b8cbfba240644959fd3d00588a8d04b37ef',....
    # client.pull('nginx:latest')
    # client.pull('busybox:latest')
    # res = client.search('busybox')
    # ims = client.images()
    # for im in ims:
    #     for i in im['RepoTags']:
    #         print(i)
    #         client.remove_image(i)
    # client.remove_image('busybox:1-musl')