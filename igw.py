# Create Internet Gateway
def create_internet_gateway(ec2, vpc_id):
    print("Creating Internet Gateway...")
    igw = ec2.create_internet_gateway()
    igw_id = igw["InternetGateway"]["InternetGatewayId"]
    ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    print(f"Internet Gateway created and attached: {igw_id}")
    return igw_id
