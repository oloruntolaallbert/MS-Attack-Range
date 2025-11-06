# terraform/outputs.tf

output "dc_public_ip" {
  value = azurerm_public_ip.dc_pip.ip_address
  description = "Public IP of the Domain Controller"
  depends_on = [azurerm_windows_virtual_machine.dc]  # Wait for VM to be created
}

output "workstation_public_ip" {
  value = azurerm_public_ip.workstation_pip.ip_address
  description = "Public IP of the Workstation"
  depends_on = [azurerm_windows_virtual_machine.workstation]  # Wait for VM to be created
}

output "windows11_public_ip" {
  value       = azurerm_public_ip.windows11_pip.ip_address
  description = "Public IP of the Windows 11 workstation"
  depends_on  = [azurerm_windows_virtual_machine.windows11]
}

output "windows2025_public_ip" {
  value       = azurerm_public_ip.windows2025_pip.ip_address
  description = "Public IP of the Windows Server 2025 machine"
  depends_on  = [azurerm_windows_virtual_machine.windows2025]
}

output "kali_public_ip" {
  value = azurerm_public_ip.kali_pip.ip_address
  description = "Public IP of the Kali Linux machine"
  depends_on = [azurerm_linux_virtual_machine.kali]  # Wait for VM to be created
}

output "sentinel_workspace_id" {
  value = azurerm_log_analytics_workspace.law.workspace_id
  description = "Workspace ID for Azure Sentinel"
}
