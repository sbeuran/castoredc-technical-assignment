# Variables
variable "location" {
  description = "Azure region"
  type        = string
  default     = "westeurope"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "fruits-api-rg"
  location = var.location
  
  tags = {
    Environment = var.environment
    Project     = "fruits-api"
  }
}

# Virtual Network
resource "azurerm_virtual_network" "vnet" {
  name                = "fruits-api-vnet"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  address_space       = ["10.0.0.0/16"]

  tags = {
    Environment = var.environment
    Project     = "fruits-api"
  }
}

# Subnet
resource "azurerm_subnet" "subnet" {
  name                 = "fruits-api-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
  service_endpoints    = ["Microsoft.Sql"]

  delegation {
    name = "fs"
    service_delegation {
      name = "Microsoft.DBforMySQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

# Private DNS Zone
resource "azurerm_private_dns_zone" "dns" {
  name                = "fruits-api.mysql.database.azure.com"
  resource_group_name = azurerm_resource_group.rg.name

  tags = {
    Environment = var.environment
    Project     = "fruits-api"
  }
}

# Private DNS Zone VNet Link
resource "azurerm_private_dns_zone_virtual_network_link" "dns_link" {
  name                  = "fruits-api-vnet-link"
  resource_group_name   = azurerm_resource_group.rg.name
  private_dns_zone_name = azurerm_private_dns_zone.dns.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
}

# MySQL Flexible Server
resource "azurerm_mysql_flexible_server" "mysql" {
  name                = "fruits-api-db"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  zone                = "2"
  
  administrator_login    = "mysqladmin"
  administrator_password = "P@ssw0rd123!" # Change this in production!

  sku_name = "B_Standard_B1ms"
  version  = "8.0.21"

  delegated_subnet_id = azurerm_subnet.subnet.id
  private_dns_zone_id = azurerm_private_dns_zone.dns.id

  depends_on = [
    azurerm_private_dns_zone_virtual_network_link.dns_link
  ]

  storage {
    size_gb = 20
  }

  tags = {
    Environment = var.environment
    Project     = "fruits-api"
  }
}

# MySQL Database
resource "azurerm_mysql_flexible_database" "database" {
  name                = "fruits"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_mysql_flexible_server.mysql.name
  charset             = "utf8mb4"
  collation          = "utf8mb4_unicode_ci"
}

# App Service Plan
resource "azurerm_service_plan" "app_plan" {
  name                = "fruits-api-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "B1"

  tags = {
    Environment = var.environment
    Project     = "fruits-api"
  }
}

# App Service
resource "azurerm_linux_web_app" "app" {
  name                = "fruits-api-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.app_plan.id

  site_config {
    application_stack {
      python_version = "3.11"
    }
    always_on = true
  }

  app_settings = {
    "MYSQL_USER"     = azurerm_mysql_flexible_server.mysql.administrator_login
    "MYSQL_PASSWORD" = azurerm_mysql_flexible_server.mysql.administrator_password
    "MYSQL_HOST"     = azurerm_mysql_flexible_server.mysql.fqdn
    "MYSQL_DATABASE" = azurerm_mysql_flexible_database.database.name
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "PYTHON_VERSION" = "3.11"
    "WEBSITES_PORT" = "8000"
    "STARTUP_COMMAND" = "sh startup.sh"
  }

  tags = {
    Environment = var.environment
    Project     = "fruits-api"
  }
} 