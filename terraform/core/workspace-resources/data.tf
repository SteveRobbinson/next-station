data "terraform_remote_state" "workspace" {
  backend = "s3"

  config = {
    bucket = "next-station-terraform"
    key    = "core/workspace/terraform.tfstate"
    region = "eu-central-1"
  }
}
