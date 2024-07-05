import sys
from cli_client import ApiClient
from rpipe_utils import pipestr
from scripts.render_cli import show_cli_output

def show_vlan_interface(path, template):
    resp = ApiClient().get(path)
    if not resp.ok():
        print(resp.error_message())
        return 1
    if "sonic-vlan:sonic-vlan" in resp.content:
        data = resp.content["sonic-vlan:sonic-vlan"].get("VLAN", {}).get("VLAN_LIST", [])
    else:
        data = []
    show_cli_output(template, data)
    return 0

class Handlers:
    @staticmethod
    def get_sonic_vlan_sonic_vlan(template, *args):
        vlan_path = "/restconf/data/sonic-vlan:sonic-vlan"
        return show_vlan_interface(vlan_path, template)

def run(func, args):
    return getattr(Handlers, func)(*args)

if __name__ == '__main__':
    pipestr().write(sys.argv)
    func = sys.argv[1]
    run(func, sys.argv[2:])
