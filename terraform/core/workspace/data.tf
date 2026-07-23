data "terraform_remote_state" "infrastructure" {
  backend = "s3"

  config = {
    bucket = "next-station-terraform"
    key    = "core/infrastructure/terraform.tfstate"
    region = "eu-central-1"
  }
}
