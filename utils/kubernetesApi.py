
from kubernetes import config ,client
# from app.config import K8S_TOKEN,K8S_APISERVER

K8S_TOKEN = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImlBZWwxUU5zVkhMMHg2TGs2NXZ4SHZmbXp2NHFOOUJ5TVRLWVEyalFNa2MifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi05anFwcSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijc5NjY2ZDRhLWQ3YWUtNDVhMC04ZGMyLWVkY2FlMDVhZmY2MCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTphZG1pbiJ9.gbUrxp8EwCqFtXywQjZcko8lw_sePRqPY9dfcA12Ro-AVZ8V92wXn4-AsH-WeFlG3JqkhNPMmY4EtRuRv2Pb93gFJoOi4gAogEYMwNyy_CWBI8zSOEa2py0d8oF6gtZsIdCXVMuPFYYce1Kpx-pDmP4A6MjnOki9v9DvgupQwzP-XParyeaB65FeP-JW04UVhBFxNp2ShBH6_cxH_Qy06u2Y5AkEABYct3XBnV14Z15SJZkPiz8oueCseZLWIEYDil9D5syKJrpGymJhz8gEBzy2bOtqDdD4y6ZAUGeH2hj5g4WX27dutUhpCyf0zf8JoREqUCisfNRqLH3_X4opVA'
K8S_APISERVER = 'https://192.168.128.110:8443'
#config.kube_config.load_kube_config(config_file='adm')

class K8SAPI():
    def __init__(self,k8s_token,k8s_apiserver):
        self.configuration = client.Configuration()
        self.configuration.host = K8S_APISERVER
        self.configuration.verify_ssl = False
        self.configuration.assert_hostname = False
        # self.configuration.ssl_ca_cert = 'ca.crt'
        self.configuration.api_key = {"authorization": "Bearer " + K8S_TOKEN}
        # self.configuration.assert_hostname = "k8s-master.novalocal"
        client.Configuration.set_default(self.configuration)
        self.App = client.AppsV1Api()  # 获取namespaced_daemon_set，namespaced_deployment_set,namespaced_stateful_set,namespaced_replica_set
        self.Core = client.CoreV1Api()  # 获取namespace,node,PV,namespace_pod,namespace_service,namespace_config_map,namespace_secret,namespace_pvc,namespaced_replication_controller
        self.Rbac = client.RbacAuthorizationV1Api()  # 获取cluster_role
        self.Storage = client.StorageV1Api()  # 获取storage_class，
        self.Batch = client.BatchV1Api()  # 获取namespace_job
        self.Batchbeta = client.BatchV1beta1Api()  # 获取namespace_cron_job
        self.Extension = client.ExtensionsV1beta1Api()  # 获取namespace_ingress
        self.response_data = {}
        self.data_dict ={}

    # k8s的node节点
    def NodeHandler(self, *args, **kwargs):
        for obj in self.Core.list_node().items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'node'
            self.data_dict['status'] = obj.status.conditions[-1].status
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    # k8s的persistent_volume
    def PVHandler(self, *args, **kwargs):
        for obj in self.Core.list_persistent_volume().items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'pv'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    # cluster Role
    def RoleHandler(self, *args, **kwargs):
        for obj in self.Rbac.list_cluster_role().items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'role'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    # storageclass
    def StorageClassHandler(self, *args, **kwargs):
        for obj in self.Storage.list_storage_class().items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'sc'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data


    #resource of namespace
    # daemonset
    def DaemonSetHandler(self, namespace, *args, **kwargs):
        for obj in self.App.list_namespaced_daemon_set(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'ds'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    #deployment
    def DeploymentHandler(self, namespace, *args, **kwargs):
        for obj in self.App.list_namespaced_deployment(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'dp'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    #pods
    def PodHandler(self, namespace, *args, **kwargs):
        for obj in self.Core.list_namespaced_pod(namespace=namespace).items:
            # pod_dict = {}
            # pod_dict['name'] = pd.metadata.name
            # pod_dict['status'] = 'Running' if (pd.status.container_statuses[0].state.running if pd.status.container_statuses else None) else 'Stoped'
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'pod'
            self.data_dict['pod_ip'] = obj.status.pod_ip
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    #statefulset
    def StatefulSetHandler(self, namespace, *args, **kwargs):
        for obj in self.App.list_namespaced_stateful_set(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'ss'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    #replicaset
    def ReplicaSetHandler(self, namespace, *args, **kwargs):
        for obj in self.App.list_namespaced_replica_set(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'rs'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    #service
    def ServiceHandler(self, namespace, *args, **kwargs):
        for obj in self.Core.list_namespaced_service(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'srv'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    #config_map
    def ConfigMapHandler(self, namespace, *args, **kwargs):
        for obj in self.Core.list_namespaced_config_map(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'cm'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    #secret
    def SecretHandler(self, namespace, *args, **kwargs):
        for obj in self.Core.list_namespaced_secret(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'sec'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    # persistent valume claim
    def PVCHandler(self, namespace, *args, **kwargs):
        for obj in self.Core.list_namespaced_persistent_volume_claim(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'pvc'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    # jobs
    def JobHandler(self, namespace, *args, **kwargs):
        for obj in self.Batch.list_namespaced_job(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'job'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    # jobs
    def CronJobHandler(self, namespace, *args, **kwargs):
        for obj in self.Batchbeta.list_namespaced_cron_job(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'cjob'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    # replaction controller
    def RCHandler(self, namespace, *args, **kwargs):
        for obj in self.Core.list_namespaced_replication_controller(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'rc'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data

    # ingress
    def IngressHandler(self, namespace, *args, **kwargs):
        for obj in self.Extension.list_namespaced_ingress(namespace=namespace).items:
            self.data_dict['name'] = obj.metadata.name
            self.data_dict['type'] = 'ing'
            self.response_data['data'].append(self.data_dict.copy())
        self.response_data['code'] = 200
        return self.response_data