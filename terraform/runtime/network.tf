resource "aws_eip" "nat_eip" {
  domain = "vpc"

  tags = {
    Name    = "${data.terraform_remote_state.infrastructure.outputs.workspace_name}-nat-eip"
    Project = "next-station"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = data.terraform_remote_state.infrastructure.outputs.public_subnet_id

  tags = {
    Name    = "${data.terraform_remote_state.infrastructure.outputs.workspace_name}-nat-gateway"
    Project = "next-station"
  }
}

resource "aws_route" "private_nat_route" {
  route_table_id         = data.terraform_remote_state.infrastructure.outputs.private_rt_id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
}
