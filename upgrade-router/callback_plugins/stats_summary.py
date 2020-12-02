from ansible.plugins.callback import CallbackBase
from subprocess import call
from platform import system as get_system_name

class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'stats_summary'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):

        # make sure the expected objects are present, calling the base's __init__
        super(CallbackModule, self).__init__()

    def v2_playbook_on_play_start(self, play):
        self.vm = play.get_variable_manager()


    def v2_runner_on_ok(self, result):
        print(result._host)
        print(result._task)
        print(result._task_fields)
        print(result._task.vars)
        print(self.vm.get_vars())
        #print(self._dump_results(result))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        print(result._host)
        print(result._task)
        print(result._task_fields)
        print(result._task.vars)
        print(self.vm.get_vars())
        #print(self._dump_results(result))


    def v2_playbook_on_stats(self, stats):

        def notify(msg,is_error=False):        
            #sys_name = get_system_name()
            #if sys_name == 'Darwin':
            #    sound = "Basso" if is_error else "default"
            #    call(["osascript", "-e",
            #        'display notification "{}" with title "Ansible" sound name "{}"'.
            #        format(msg,sound)])
            #elif sys_name == 'Linux':
            #    icon = "dialog-warning" if is_error else "dialog-info"
            #    rc = call(["notify-send", "-i", icon, "Ansible", msg])
            #    print("error code {}".format(rc))
            pass

            

        hosts = stats.processed.keys()

        failed_hosts = []
        upgraded_hosts = []
        not_upgraded_hosts = []


        for h in hosts:
            t = stats.summarize(h)
            print(t)
            if t['unreachable'] + t['failures'] > 0:
                failed_hosts.append(h)

        if len(failed_hosts) > 0:
            notify("Failed hosts: {}".format(" ".join(failed_hosts)),True)
        else:
            notify("Job's done!")

        print("------------->>>> YESSSSS")
        print(hosts)
        print(stats.custom)
        print(self.vm.get_vars())


