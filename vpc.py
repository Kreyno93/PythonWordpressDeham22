# vpc.py
def create_vpc(ec2, cidr_block):
    print(f"Creating VPC with CIDR: {cidr_block}")
    vpc = ec2.create_vpc(CidrBlock=cidr_block)
    vpc_id = vpc["Vpc"]["VpcId"]
    # Tag the VPC
    ec2.create_tags(
        Resources=[vpc_id],
        Tags=[{"Key": "Name", "Value": "MyVPC"}],
    )
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={"Value": True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={"Value": True})
    print(f"VPC Created with ID: {vpc_id}")
    return vpc_id


def delete_vpc(ec2, vpc_id):
    print(f"Deleting VPC: {vpc_id}")
    try:
        ec2.delete_vpc(VpcId=vpc_id)
        print("VPC deleted.")
    except Exception as e:
        print(f"Failed to delete VPC: {e}")
