def create_route_tables(ec2, vpc_id):
    print("Creating Route Tables...")
    public_rt = ec2.create_route_table(VpcId=vpc_id)["RouteTable"]["RouteTableId"]
    private_rt = ec2.create_route_table(VpcId=vpc_id)["RouteTable"]["RouteTableId"]
    return {"public": public_rt, "private": private_rt}
