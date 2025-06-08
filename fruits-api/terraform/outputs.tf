output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "mysql_server_name" {
  value = azurerm_mysql_flexible_server.mysql.name
}

output "mysql_database_name" {
  value = azurerm_mysql_flexible_database.database.name
}

output "mysql_server_fqdn" {
  value = azurerm_mysql_flexible_server.mysql.fqdn
}

output "vnet_name" {
  value = azurerm_virtual_network.vnet.name
}

output "subnet_name" {
  value = azurerm_subnet.subnet.name
}

output "app_service_url" {
  value = "https://${azurerm_linux_web_app.app.default_hostname}"
}

output "app_service_name" {
  value = azurerm_linux_web_app.app.name
} 