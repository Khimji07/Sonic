## Accessing Linux and Docker Container

### SSH into Linux Machine
```bash
ssh username@hostname
```
Replace `username` with your Linux username and `hostname` with the IP address or hostname of your Linux machine.

### Access Docker Container
```bash
docker exec -it mgmt-framework bash
```
This command enters an interactive bash session within the `mgmt-framework` Docker container.

## File Operations

### Replace `rest_server`
```bash
cd /usr/sbin/
mv rest_server rest_server_old   # Backup existing
mv rest_server_new rest_server   # Replace with new version
```
Navigate to `/usr/sbin/`, rename `rest_server` to `rest_server_old` for backup, and replace it with your new version (`rest_server_new`).

### Add Files to `/usr/sbin/cli/`
```bash
 cp vlan.xml /usr/sbin/cli/command-tree/
 cp sonic-cli-vlan.py /usr/sbin/cli/
 cp vlan.j2 /usr/sbin/cli/render-templates/
```
Copy `vlan.xml` to `command-tree/`, `sonic-cli-vlan.py` to `/usr/sbin/cli/`, and `vlan.j2` to `/usr/sbin/cli/render-templates/` inside the `mgmt-framework` Docker container.

