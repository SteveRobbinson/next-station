data "terraform_remote_state" "core" {
  backend = "s3"

  config = {
    bucket = "next-station-terraform"
    key    = "core/terraform.tfstate"
    region = "eu-central-1"
  }
}
