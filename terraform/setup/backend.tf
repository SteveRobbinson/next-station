terraform {
  backend "s3" {
    bucket       = "next-station-terraform"
    key          = "setup/terraform.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true
  }
}
