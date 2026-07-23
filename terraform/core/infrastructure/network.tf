data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc" "databricks_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name    = "${var.workspace_name}-vpc"
    Project = "next-station"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.databricks_vpc.id
  cidr_block        = var.public_subnet_cidr
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name    = "${var.workspace_name}-public-subnet"
    Project = "next-station"
  }
}

resource "aws_subnet" "private_subnet_a" {
  vpc_id            = aws_vpc.databricks_vpc.id
  cidr_block        = var.private_subnet_a_cidr
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name                              = "${var.workspace_name}-private-subnet-a"
    Project                           = "next-station"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

resource "aws_subnet" "private_subnet_b" {
  vpc_id            = aws_vpc.databricks_vpc.id
  cidr_block        = var.private_subnet_b_cidr
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name                              = "${var.workspace_name}-private-subnet-b"
    Project                           = "next-station"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.databricks_vpc.id

  tags = {
    Name    = "${var.workspace_name}-igw"
    Project = "next-station"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.databricks_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name    = "${var.workspace_name}-public-rt"
    Project = "next-station"
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.databricks_vpc.id

  tags = {
    Name    = "${var.workspace_name}-private-rt"
    Project = "next-station"
  }
}

resource "aws_route_table_association" "private_assoc_a" {
  subnet_id      = aws_subnet.private_subnet_a.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_route_table_association" "private_assoc_b" {
  subnet_id      = aws_subnet.private_subnet_b.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_security_group" "databricks_sg" {
  name   = "${var.workspace_name}-sg"
  vpc_id = aws_vpc.databricks_vpc.id

  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    self      = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${var.workspace_name}-sg"
    Project = "next-station"
  }
}
