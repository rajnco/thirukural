variable "resource_group_location" {
  type = string
  default = "centralindia"
  description = "Location of all the resources"
}

variable "resource_group_name" {
  type = string
  default = "tofu-thirukural-auto"
  description = "resource group name"
}

variable "container_image" {
  type = string
  default = "rajnco/thirukural:latest"
  description = "image pulled from docker hub"
}

variable "container_name" {
  type = string
  default = "thirukural"
  description = "container name"
}

variable "port-svc1" {
  type = number
  default = 9090
  description = "application exposed port for service one"
}

variable "port-svc2" {
  type = number
  default = 9100
  description = "application exposed port for service two"
}

variable "port" {
  type        = number
  description = "Port to open on the container and the public IP address."
  default     = 80
}

variable "cpu_cores" {
  type        = number
  description = "The number of CPU cores to allocate to the container."
  default     = 1
}

variable "memory_in_gb" {
  type        = number
  description = "The amount of memory to allocate to the container in gigabytes."
  default     = 0.5
}

variable "restart_policy" {
  type        = string
  description = "The behavior of Azure runtime if container has stopped."
  default     = "Always"
}
