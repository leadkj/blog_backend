import json
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.playbook.play import Play
from ansible import context
from optparse import Values


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """Print a json representation of the result.

        Also, store the result in an instance attribute for retrieval later
        """
        host = result._host
        self.host_ok[host.get_name()] = result
        # print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result


class AnsibleApi(object):
    def __init__(self):
        self.options = {'verbosity': 0, 'ask_pass': False, 'private_key_file': None, 'remote_user': None,
                        'connection': 'smart', 'timeout': 10, 'ssh_common_args': '', 'sftp_extra_args': '',
                        'scp_extra_args': '', 'ssh_extra_args': '', 'force_handlers': False, 'flush_cache': None,
                        'become': False, 'become_method': 'sudo', 'become_user': None, 'become_ask_pass': False,
                        'tags': ['all'], 'skip_tags': [], 'check': False, 'syntax': None, 'diff': False,
                        'inventory': '/etc/ansible/hosts',
                        'listhosts': None, 'subset': None, 'extra_vars': [], 'ask_vault_pass': False,
                        'vault_password_files': [], 'vault_ids': [], 'forks': 5, 'module_path': None, 'listtasks': None,
                        'listtags': None, 'step': None, 'start_at_task': None, 'args': ['fake']}
        self.ops = Values(self.options)

        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources=[self.options['inventory']])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        context._init_global_context(self.ops)
    def runansible(self, host_list, module_name,module_args): #host_list 是一个列表，列表中可以是主机，也可以是组名

        tqm = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            passwords=self.passwords,
            stdout_callback=self.results_callback,
            # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
        )

        # create data structure that represents our play, including tasks, this is basically what our YAML loader does internally.
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))]

        )

        # Create play object, playbook objects use .load instead of init or new methods,
        # this will also automatically create the task objects from the info provided in play_source
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        # Actually run it
        try:
            result = tqm.run(play)  # most interesting data for a play is actually sent to the callback's methods
        finally:
            # we always need to cleanup child procs and the structures we use to communicate with them
            tqm.cleanup()
            if self.loader:
                self.loader.cleanup_all_tmp_files()

        # Remove ansible tmpdir
        # shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)



        results_raw = {}
        results_raw['success'] = self.results_callback.host_ok
        results_raw['failed'] = self.results_callback.host_failed
        results_raw['unreachable'] = self.results_callback.host_unreachable
        return results_raw

    def playbookrun(self, playbook_path, host_list):#host_list 是一个列表，列表中可以是主机，也可以是组名
        self.variable_manager.extra_vars.update({'hosts': host_list})


        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, passwords=self.passwords)
        playbook._tqm._stdout_callback = self.results_callback
        playbook.run()

        results_raw = {}
        results_raw['success'] = self.results_callback.host_ok
        results_raw['failed'] = self.results_callback.host_failed
        results_raw['unreachable'] = self.results_callback.host_unreachable

        return results_raw


if __name__ == "__main__":
    a = AnsibleApi()
    host_list = ['192.168.10.100']

    res = a.runansible(host_list, 'shell','touch /tmp/a.txt')
    print(res)
    result = a.playbookrun(playbook_path=['f1.yml'], host_list=host_list)
    print(result)
    result_success = result.get("success")
    result_failed = result.get("failed")
    result_unreachable = result.get("unreachable")
    if result_success:
        for item in result_success:
            print(item)
