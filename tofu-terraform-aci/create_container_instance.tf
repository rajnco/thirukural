resource "azurerm_container_group" "container" {
  name = "thirukrual-tofu"
  resource_group_name = azurerm_resource_group.tofu-thirukural.name
  location = azurerm_resource_group.tofu-thirukural.location
  os_type = "Linux"
  restart_policy = var.restart_policy
  #priority = "Spot"
  #ip_address_type = "None"

  container {
    name = var.container_name
    image = var.container_image
    cpu = var.cpu_cores
    memory = var.memory_in_gb

    ports {
      port = var.port
      protocol = "TCP"
    }

    ports {
      port = var.port-svc1
      protocol = "TCP"
    }

    ports {
      port = var.port-svc2
      protocol = "TCP"
    }

  }
}