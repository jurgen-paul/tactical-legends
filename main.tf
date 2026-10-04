terraform {
  required_version = ">= 1.5.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4.0"
    }
  }
}

variable "app_name" {
  description = "Application identifier"
  type        = string
  default     = "tactical-legends"
}

variable "environment" {
  description = "Target deployment environment"
  type        = string
  default     = "production"
}

variable "version_tag" {
  description = "Release version"
  type        = string
  default     = "1.0.0"
}

# Provision deployment manifest for build verification
resource "local_file" "deployment_manifest" {
  filename = "${path.module}/dist/deploy-manifest.json"
  content = jsonencode({
    application = var.app_name
    title       = "Tactical Legends: Rise of OISTARIAN"
    environment = var.environment
    version     = var.version_tag
    build_type  = "web-static"
  })
}

output "application_name" {
  description = "The name of the application"
  value       = var.app_name
}

output "environment" {
  description = "The deployment environment"
  value       = var.environment
}
