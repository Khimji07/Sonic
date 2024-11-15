import sys
from cli_client import ApiClient
from rpipe_utils import pipestr
from scripts.render_cli import show_cli_output
from natsort import natsorted

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
    
    @staticmethod
    def put_sonic_vlan_sonic_vlan(vlan_id, *args):
        vlan_path = "/restconf/data/sonic-vlan:sonic-vlan"
        vlan_name = f"Vlan{vlan_id}"  # Construct VLAN name as "Vlan10" if vlan_id is 10
        payload = {
          "sonic-vlan:sonic-vlan": {
                             "VLAN": {
                                "VLAN_LIST": [
                                              {
                                                 "name": vlan_name,
                                                 "vlanid": vlan_id
                                              }
                                             ]
                                     }
                                    }
                                }

        return ApiClient().put(vlan_path, payload)

def run(func, args):
    if func == "get_sonic_vlan_sonic_vlan":
        if len(args) < 1:
            print("Usage: python3 sonic-cli-vlan.py get_sonic_vlan_sonic_vlan <template>")
            return 1
        return Handlers.get_sonic_vlan_sonic_vlan(args[0])
    
    elif func == "put_sonic_vlan_sonic_vlan":
        if len(args) < 1:
            print("Usage: python3 sonic-cli-vlan.py put_sonic_vlan_sonic_vlan <vlan_id>")
            return 1
        try:
            vlan_id = int(args[0])
        except ValueError:
            print("Invalid VLAN ID. VLAN ID must be an integer.")
            return 1
        return Handlers.put_sonic_vlan_sonic_vlan(vlan_id)

    else:
        print(f"Unknown function: {func}")
        return 1

if __name__ == '__main__':
    pipestr().write(sys.argv)
    if len(sys.argv) < 2:
        print("Usage: python3 sonic-cli-vlan.py <function> <args>")
        sys.exit(1)
    
    func = sys.argv[1]
    args = sys.argv[2:]
    run(func, args)

