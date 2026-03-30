import os
import sys
import time

class AttackExecutor:
    """Attack execution management for Azure Attack Range"""
    
    # Add attack scenarios and sequences
    ATTACK_SCENARIOS = {
        # Discovery Attacks
        "process_discovery": "T1057",
        "network_discovery": "T1046",
        "account_discovery": "T1087",
        "system_info_discovery": "T1082",
        
        # Credential Access
        "credential_dump": "T1003.001",
        "brute_force": "T1110",
        "credential_mimikatz": "T1003.002",
        "credential_vault_access": "T1003",  # Enhanced
        
        # Execution
        "powershell_exec": "T1059.001",
        "command_shell": "T1059.003",
        "scheduled_task": "T1053.005",
        
        # Persistence
        "registry_run_keys": "T1547.001",
        "scheduled_task_persist": "T1053.005",
        "startup_folder": "T1547.001",
        "multi_persistence": "T1547",  # Enhanced
        
        # Defense Evasion
        "timestomp": "T1070.006",
        "clear_logs": "T1070.001",
        "disable_defender": "T1562.001",
        "defense_evasion_chain": "T1562",  # Enhanced
        
        # Network Attacks
        "network_scan": "network_scan",
        "port_scan": "port_scan",
        "smb_scan": "smb_scan",
        "advanced_network_discovery": "T1046",  # Enhanced
        
        # Lateral Movement
        "lateral_movement_scan": "T1021",  # Enhanced
        
        # Exfiltration
        "data_staging": "T1074",  # Enhanced
        "exfiltration_attempt": "T1041",  # Enhanced
        
        # Impact
        "impact_simulation": "T1486",  # Enhanced
        
        # Advanced Memory Attacks
        "lsass_memory_dump": "advanced_memory_attacks",
        "process_hollowing": "advanced_memory_attacks", 
        "reflective_dll_injection": "advanced_memory_attacks",
        "advanced_memory_chain": "advanced_memory_attacks",
        
        # Modern Evasion Techniques
        "amsi_bypass": "modern_evasion",
        "etw_bypass": "modern_evasion",
        "lolbin_abuse": "modern_evasion",
        "dll_hijacking": "modern_evasion",
        "process_doppelganging": "modern_evasion",
        "modern_evasion_chain": "modern_evasion",

        # Ransomware Simulation (no real encryption - telemetry only)
        "ransomware_vss_delete": "ransomware_simulation",
        "ransomware_disable_recovery": "ransomware_simulation",
        "ransomware_stop_services": "ransomware_simulation",
        "ransomware_mass_rename": "ransomware_simulation",
        "ransomware_drop_note": "ransomware_simulation",
        "ransomware_share_enum": "ransomware_simulation",
        "ransomware_clear_logs": "ransomware_simulation",
        "ransomware_disable_defender": "ransomware_simulation",
        "ransomware_encoded_powershell": "ransomware_simulation",
    }

    ATTACK_SEQUENCES = {
        "recon": [
            "process_discovery",
            "network_discovery",
            "system_info_discovery"
        ],
        "credential_theft": [
            "account_discovery",
            "credential_dump",
            "credential_mimikatz"
        ],
        "persistence": [
            "registry_run_keys",
            "scheduled_task_persist",
            "startup_folder"
        ],
        # 🔥 ENHANCED ATTACK SEQUENCES WITH ULTIMATE COVERAGE
        "full_attack_simulation": [
            # Phase 1: Discovery & Reconnaissance
            "advanced_network_discovery", "process_discovery", "account_discovery", "system_info_discovery",
            
            # Phase 2: Initial Access & Credential Theft
            "brute_force", "credential_dump", "lsass_memory_dump", "credential_vault_access",
            
            # Phase 3: Execution & Advanced Evasion
            "powershell_exec", "command_shell", "amsi_bypass", "etw_bypass", "lolbin_abuse",
            
            # Phase 4: Advanced Memory Attacks
            "process_hollowing", "reflective_dll_injection", "process_doppelganging", "dll_hijacking",
            
            # Phase 5: Persistence Mechanisms
            "registry_run_keys", "scheduled_task_persist", "startup_folder", "multi_persistence",
            
            # Phase 6: Defense Evasion
            "timestomp", "clear_logs", "disable_defender", "defense_evasion_chain",
            
            # Phase 7: Lateral Movement & Network
            "lateral_movement_scan", "network_scan", "port_scan", "smb_scan",
            
            # Phase 8: Collection & Exfiltration
            "data_staging", "exfiltration_attempt",
            
            # Phase 9: Impact
            "impact_simulation"
        ],
        "full_chain": [
            # EVERY SINGLE ATTACK AVAILABLE - Complete coverage
            "advanced_network_discovery", "network_discovery", "process_discovery", "account_discovery", "system_info_discovery",
            "credential_dump", "brute_force", "credential_mimikatz", "credential_vault_access", "lsass_memory_dump",
            "powershell_exec", "command_shell", "scheduled_task",
            "registry_run_keys", "scheduled_task_persist", "startup_folder", "multi_persistence", 
            "timestomp", "clear_logs", "disable_defender", "defense_evasion_chain",
            "network_scan", "port_scan", "smb_scan", "lateral_movement_scan",
            "data_staging", "exfiltration_attempt", "impact_simulation",
            "process_hollowing", "reflective_dll_injection", "advanced_memory_chain",
            "amsi_bypass", "etw_bypass", "lolbin_abuse", "dll_hijacking", "process_doppelganging", "modern_evasion_chain"
        ],
        "cross_platform": [
            "network_discovery",
            "system_info_discovery",
            "account_discovery",
            "process_discovery",
            "command_shell",
            "powershell_exec",
            "brute_force",
            "credential_dump",
            "scheduled_task",
            "startup_folder",
            "clear_logs",
            "timestomp",
            "port_scan",
            "smb_scan"
        ],
        # Enhanced sequences from the new guide
        "enhanced_recon": [
            "advanced_network_discovery",
            "process_discovery",
            "system_info_discovery",
            "account_discovery"
        ],
        "advanced_persistence": [
            "multi_persistence",
            "registry_run_keys",
            "scheduled_task",
            "startup_folder"
        ],
        # Advanced sequences
        "apt_simulation": [
            "network_discovery", "account_discovery", "lsass_memory_dump", 
            "amsi_bypass", "dll_hijacking", "data_staging", "impact_simulation"
        ],
        "memory_exploitation": [
            "lsass_memory_dump", "process_hollowing", "reflective_dll_injection"
        ],
        "stealth_operations": [
            "amsi_bypass", "etw_bypass", "lolbin_abuse", "dll_hijacking"
        ],
        "red_team_chain": [
            "process_discovery", "lolbin_abuse", "process_doppelganging", 
            "dll_hijacking", "clear_logs"
        ],
        # Ransomware Simulation Sequences (no real encryption)
        "ransomware_simulation": [
            # Phase 1: Pre-encryption prep
            "ransomware_vss_delete",
            "ransomware_disable_recovery",
            "ransomware_stop_services",
            "ransomware_disable_defender",
            # Phase 2: Simulated encryption + ransom notes
            "ransomware_mass_rename",
            "ransomware_drop_note",
            # Phase 3: Lateral spread indicators
            "ransomware_share_enum",
            # Phase 4: Anti-forensics
            "ransomware_clear_logs",
            "ransomware_encoded_powershell",
        ],
        "ransomware_pre_encryption": [
            "ransomware_vss_delete",
            "ransomware_disable_recovery",
            "ransomware_stop_services",
            "ransomware_disable_defender",
        ],
        "ransomware_impact": [
            "ransomware_mass_rename",
            "ransomware_drop_note",
            "ransomware_clear_logs",
        ],
    }
    
    def __init__(self, config):
        self.config = config
    
    def get_playbook_path(self, attack_type):
        """Determine the correct playbook path for an attack type"""
        # Check if it's an enhanced attack that has its own playbook
        enhanced_attacks = {
            "advanced_network_discovery": "enhanced/network_discovery.yml",
            "credential_vault_access": "enhanced/credential_access.yml",
            "multi_persistence": "enhanced/persistence.yml",
            "defense_evasion_chain": "enhanced/defense_evasion.yml",
            "lateral_movement_scan": "enhanced/lateral_movement.yml",
            "data_staging": "enhanced/exfiltration.yml",
            "exfiltration_attempt": "enhanced/exfiltration.yml",
            "impact_simulation": "enhanced/impact.yml",
            # Advanced memory attacks
            "lsass_memory_dump": "enhanced/advanced_memory_attacks.yml",
            "process_hollowing": "enhanced/advanced_memory_attacks.yml",
            "reflective_dll_injection": "enhanced/advanced_memory_attacks.yml",
            "advanced_memory_chain": "enhanced/advanced_memory_attacks.yml",
            # Modern evasion techniques
            "amsi_bypass": "enhanced/modern_evasion.yml",
            "etw_bypass": "enhanced/modern_evasion.yml",
            "lolbin_abuse": "enhanced/modern_evasion.yml",
            "dll_hijacking": "enhanced/modern_evasion.yml",
            "process_doppelganging": "enhanced/modern_evasion.yml",
            "modern_evasion_chain": "enhanced/modern_evasion.yml",
            # Ransomware simulation
            "ransomware_vss_delete": "ransomware_simulation.yml",
            "ransomware_disable_recovery": "ransomware_simulation.yml",
            "ransomware_stop_services": "ransomware_simulation.yml",
            "ransomware_mass_rename": "ransomware_simulation.yml",
            "ransomware_drop_note": "ransomware_simulation.yml",
            "ransomware_share_enum": "ransomware_simulation.yml",
            "ransomware_clear_logs": "ransomware_simulation.yml",
            "ransomware_disable_defender": "ransomware_simulation.yml",
            "ransomware_encoded_powershell": "ransomware_simulation.yml",
        }
        
        if attack_type in enhanced_attacks:
            return enhanced_attacks[attack_type]
        
        # Default behavior for standard attacks
        technique_id = self.ATTACK_SCENARIOS.get(attack_type)
        if technique_id and technique_id.startswith("T"):
            return "install_atomic.yml"
        else:
            return "attack_simulation.yml"
    
    def run_attack(self, attack_type, target=None):
        """Run individual attack"""
        print(f"[+] Running {attack_type} attack simulation...")

        technique_id = self.ATTACK_SCENARIOS.get(attack_type)
        if not technique_id:
            print(f"Unknown attack type: {attack_type}")
            return False

        # Get the appropriate playbook
        playbook = self.get_playbook_path(attack_type)
        
        # Build the command based on attack type
        if attack_type in ["advanced_network_discovery", "credential_vault_access", "multi_persistence", 
                          "defense_evasion_chain", "lateral_movement_scan", "data_staging", 
                          "exfiltration_attempt", "impact_simulation", "lsass_memory_dump",
                          "process_hollowing", "reflective_dll_injection", "advanced_memory_chain",
                          "amsi_bypass", "etw_bypass", "lolbin_abuse", "dll_hijacking",
                          "process_doppelganging", "modern_evasion_chain"]:
            # Enhanced attacks with their own playbooks
            cmd = f"ansible-playbook -i playbooks/inventory.yml playbooks/{playbook} -e target_ip={target} -vv"
        elif attack_type.startswith("ransomware_"):
            # Ransomware simulation - runs the full playbook (phases are sequential)
            cmd = f"ansible-playbook -i playbooks/inventory.yml playbooks/{playbook} -vv"
        elif technique_id.startswith("T"):
            # It's an Atomic Red Team test
            cmd = f"ansible-playbook -i playbooks/inventory.yml playbooks/install_atomic.yml -e technique_id={technique_id} -vv"
        else:
            # It's a network-based attack from the standard attack_simulation.yml
            cmd = f"ansible-playbook -i playbooks/inventory.yml playbooks/attack_simulation.yml -e simulation_type={attack_type} -e target_ip={target} -vv"

        try:
            print(f"Executing command: {cmd}")
            result = os.system(cmd)
            if result != 0:
                print(f"Warning: Attack {attack_type} completed with warnings (return code {result})")
                return True
            print(f"[+] Attack {attack_type} completed successfully")
            return True
        except Exception as e:
            print(f"Error running {attack_type}: {e}")
            return False

    def run_attack_sequence(self, sequence_name):
        """Run a predefined attack sequence"""
        if sequence_name not in self.ATTACK_SEQUENCES:
            print(f"Unknown attack sequence: {sequence_name}")
            return

        print(f"[+] Starting attack sequence: {sequence_name}")
        attacks = self.ATTACK_SEQUENCES[sequence_name]
        
        successful = 0
        failed = 0
        
        for attack in attacks:
            print(f"\n[+] Running attack: {attack}")
            if self.run_attack(attack):
                successful += 1
            else:
                failed += 1
            time.sleep(30)  # Wait between attacks

        print(f"\n[+] Attack sequence {sequence_name} complete")
        print(f"Successful attacks: {successful}")
        print(f"Failed attacks: {failed}")
