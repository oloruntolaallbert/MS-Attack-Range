import json
import os
import subprocess
import yaml
import requests
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient

class AzureAttackRangeCore:
    """Core infrastructure management for Azure Attack Range"""
    
    def __init__(self, config, credential):
        self.config = config
        self.credential = credential
        self.network_client = NetworkManagementClient(credential, config['subscription_id'])
        self.compute_client = ComputeManagementClient(credential, config['subscription_id'])
    
    def update_ip_config(self):
        """Automatically update IP configuration in terraform files"""
        try:
            # Get current public IP
            response = requests.get('https://api.ipify.org?format=json')
            current_ip = f"{response.json()['ip']}/32"
            
            # Update terraform.tfvars
            tfvars_path = 'terraform/terraform.tfvars'
            
            # Check if allowed_ip variable exists in tfvars file
            if os.path.exists(tfvars_path):
                lines = []
                ip_config_found = False
                
                with open(tfvars_path, 'r') as f:
                    lines = f.readlines()
                
                with open(tfvars_path, 'w') as f:
                    for line in lines:
                        if 'allowed_ip' in line:
                            f.write(f'allowed_ip = "{current_ip}"\n')
                            ip_config_found = True
                        else:
                            f.write(line)
                    
                    # If allowed_ip wasn't found, add it
                    if not ip_config_found:
                        f.write(f'\nallowed_ip = "{current_ip}"\n')
            
            print(f"[+] Updated allowed IP to: {current_ip}")
            
            # Also ensure the variable exists in variables.tf
            variables_tf = 'terraform/variables.tf'
            if os.path.exists(variables_tf):
                with open(variables_tf, 'r') as f:
                    content = f.read()
                
                if 'allowed_ip' not in content:
                    with open(variables_tf, 'a') as f:
                        f.write('\n\nvariable "allowed_ip" {\n')
                        f.write('  description = "IP address allowed to connect to the Attack Range"\n')
                        f.write('  type        = string\n')
                        f.write('  default     = "0.0.0.0/0"\n')
                        f.write('}\n')
            
        except Exception as e:
            print(f"Warning: Could not update IP configuration: {e}")
            print("Continuing with existing configuration...")

    def build(self):
        """Build the complete attack range infrastructure"""
        print("[+] Building Azure Attack Range infrastructure...")
        
        # Update IP configuration before building
        self.update_ip_config()
        
        try:
            os.system(f"terraform -chdir=terraform init")
            result = os.system(f"terraform -chdir=terraform apply -auto-approve")
            if result != 0:
                print("Error: Terraform apply failed")
                return False
            print("[+] Infrastructure built successfully")

            if not self.create_ansible_inventory():
                print("Error: Failed to create Ansible inventory for post-build deployment")
                return False

            if not self.deploy_post_build_script():
                print("Error: Post-build PowerShell deployment failed")
                return False

            print("[+] Post-build configuration completed successfully")
            return True
        except Exception as e:
            print(f"Error building infrastructure: {e}")
            return False

    def destroy(self):
        """Destroy the complete attack range infrastructure"""
        print("[+] Destroying Azure Attack Range infrastructure...")
        try:
            result = os.system(f"terraform -chdir=terraform destroy -auto-approve")
            if result != 0:
                print("Error: Terraform destroy failed")
                return False
            print("[+] Infrastructure destroyed successfully")
            return True
        except Exception as e:
            print(f"Error destroying infrastructure: {e}")
            return False

    def update(self):
        """Update the infrastructure with new resources"""
        print("[+] Updating Azure Attack Range infrastructure...")

        # Update IP configuration before updating
        self.update_ip_config()

        try:
            result = os.system(f"terraform -chdir=terraform apply -auto-approve")
            if result != 0:
                print("Error: Terraform apply failed")
                return False
            print("[+] Infrastructure updated successfully")
            return True
        except Exception as e:
            print(f"Error updating infrastructure: {e}")
            return False

    def deploy_post_build_script(self):
        """Deploy the WinRM configuration script to new Windows VMs using Ansible"""

        playbook_path = 'playbooks/deploy_post_build_script.yml'
        inventory_path = 'playbooks/inventory.yml'

        if not os.path.exists(playbook_path):
            print(f"Error: Ansible playbook not found at {playbook_path}")
            return False

        if not os.path.exists(inventory_path):
            print("Error: Ansible inventory not found. Cannot run post-build deployment")
            return False

        print("[+] Deploying post-build PowerShell script to Windows VMs via Ansible...")

        extra_vars = {}

        post_build_config = self.config.get('post_build', {})

        winrm_port = post_build_config.get('winrm_port')
        if winrm_port is not None:
            try:
                winrm_port = int(winrm_port)
                extra_vars['winrm_port'] = winrm_port
            except (TypeError, ValueError):
                print('Error: post_build.winrm_port must be an integer value.')
                return False

        defender_config = post_build_config.get('defender_for_endpoint', {})
        enable_defender = defender_config.get('enable_onboarding', False)
        if enable_defender:
            script_path = defender_config.get('onboarding_script_path')
            if not script_path:
                print('Error: defender_for_endpoint.onboarding_script_path must be provided when enable_onboarding is true.')
                return False

            script_path = os.path.expanduser(script_path)
            if not os.path.isfile(script_path):
                print(f"Error: Defender for Endpoint onboarding script not found at {script_path}")
                return False

            extra_vars['defender_onboarding_enable'] = True
            extra_vars['defender_onboarding_script'] = script_path

            onboarding_arguments = defender_config.get('onboarding_arguments', [])
            if onboarding_arguments:
                if not isinstance(onboarding_arguments, list):
                    print('Error: defender_for_endpoint.onboarding_arguments must be a list of strings.')
                    return False

                extra_vars['defender_onboarding_arguments'] = onboarding_arguments
        else:
            if defender_config.get('onboarding_script_path'):
                print('Warning: Defender onboarding script path provided but enable_onboarding is false. Skipping Defender onboarding.')

        try:
            command = ['ansible-playbook', '-i', inventory_path, playbook_path]
            if extra_vars:
                command.extend(['-e', json.dumps(extra_vars)])

            subprocess.run(
                command,
                check=True
            )
            print("[+] Post-build PowerShell script deployed successfully")
            return True
        except FileNotFoundError:
            print("Error: ansible-playbook command not found. Please install Ansible.")
        except subprocess.CalledProcessError as exc:
            print(f"Error: Ansible playbook execution failed with exit code {exc.returncode}")

        return False

    def create_ansible_inventory(self):
        """Create Ansible inventory file with VM information"""
        print("[+] Creating Ansible inventory file...")
        
        admin_username = self.config.get('admin_username', 'azureuser')
        admin_password = self.config.get('admin_password')
        rg_name = self.config.get('resource_group', 'attack-range-rg')

        if not admin_password:
            print("Error: admin_password not found in configuration")
            return False

        inventory = {
            'all': {
                'children': {
                    'windows': {
                        'hosts': {},
                        'vars': {
                            'ansible_user': admin_username,
                            'ansible_password': admin_password,
                            'ansible_connection': 'winrm',
                            'ansible_winrm_server_cert_validation': 'ignore',
                            'ansible_port': '5985',
                            'ansible_winrm_scheme': 'http',
                            'ansible_winrm_transport': 'ntlm'
                        }
                    },
                    'linux': {
                        'hosts': {},
                        'vars': {
                            'ansible_user': 'kali',
                            'ansible_ssh_private_key_file': '~/.ssh/id_rsa',
                            'ansible_connection': 'ssh'
                        }
                    }
                }
            }
        }

        try:
            vms = self.compute_client.virtual_machines.list(rg_name)
            
            for vm in vms:
                try:
                    vm_name = vm.name
                    print(f"Processing VM: {vm_name}")

                    # Get network interface
                    network_interfaces = vm.network_profile.network_interfaces
                    if not network_interfaces:
                        continue

                    primary_nic_id = network_interfaces[0].id
                    nic_name = primary_nic_id.split('/')[-1]
                    nic = self.network_client.network_interfaces.get(rg_name, nic_name)
                    
                    if not nic.ip_configurations[0].public_ip_address:
                        continue

                    pip_id = nic.ip_configurations[0].public_ip_address.id
                    pip_name = pip_id.split('/')[-1]
                    pip = self.network_client.public_ip_addresses.get(rg_name, pip_name)
                    public_ip = pip.ip_address

                    print(f"Found IP {public_ip} for VM {vm_name}")

                    # Explicitly check for DC or workstation in the name
                    if "dc" in vm_name.lower() or "workstation" in vm_name.lower():
                        inventory['all']['children']['windows']['hosts'][vm_name] = {
                            'ansible_host': public_ip,
                            'ansible_winrm_operation_timeout_sec': 60,
                            'ansible_winrm_read_timeout_sec': 70,
                            'post_build_target': True
                        }
                    elif "kali" in vm_name.lower():
                        inventory['all']['children']['linux']['hosts'][vm_name] = {
                            'ansible_host': public_ip
                        }
                    
                except Exception as e:
                    print(f"Warning: Error processing VM {vm_name}: {str(e)}")
                    continue

            os.makedirs('playbooks', exist_ok=True)
            with open('playbooks/inventory.yml', 'w') as f:
                yaml.dump(inventory, f, default_flow_style=False)
            
            print("\nGenerated Inventory:")
            print(yaml.dump(inventory))
            
            return True

        except Exception as e:
            print(f"Error creating Ansible inventory: {str(e)}")
            return False

