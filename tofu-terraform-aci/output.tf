output "container_ipv4_address" {
  value = azurerm_container_group.container.ip_address
}

#output "container_url" {
#  value = azurerm_container_group.container.ports
#}

output "container_address" {
  value = azurerm_container_group.container.dns_config
}