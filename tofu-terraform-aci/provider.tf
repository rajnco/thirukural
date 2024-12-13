
terraform {
  required_providers {
    azurerm = {
        source = "opentofu/azurerm"
    }
  }
}

provider "azurerm" {
  features {   
  }
  subscription_id = "--YOUR-SUBSCRIPTION-ID--"
}
