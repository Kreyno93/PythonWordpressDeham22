def create_routes(ec2, vpc_id, route_table_ids, subnet_ids, igw_id):
    print("Associating Route Tables and Creating Routes...")

    # Associate public subnets with public route table
    for subnet_id in subnet_ids["public"]:
        ec2.associate_route_table(
            RouteTableId=route_table_ids["public"], SubnetId=subnet_id
        )

    # Create a route to the Internet Gateway in the public route table
    ec2.create_route(
        RouteTableId=route_table_ids["public"],
        DestinationCidrBlock="0.0.0.0/0",
        GatewayId=igw_id,
    )
    for subnet_id in subnet_ids["private"]:
        ec2.associate_route_table(
            RouteTableId=route_table_ids["private"], SubnetId=subnet_id
        )
    # Note: You would also attach an Internet Gateway and NAT Gateway here in production
