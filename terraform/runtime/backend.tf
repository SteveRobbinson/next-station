terraform {
  backend "s3" {
    bucket       = "next-station-terraform"
    key          = "runtime/terraform.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true
  }
}
