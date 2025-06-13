# Create Security Groups for Bastion and Web Servers
def create_security_groups(ec2, vpc_id):
    print("Creating Security Groups...")

    # Create Security Group for Bastion Host
    bastion_sg = ec2.create_security_group(
        GroupName="BastionSG",
        Description="Security Group for Bastion Host",
        VpcId=vpc_id,
    )
    bastion_sg_id = bastion_sg["GroupId"]

    # Allow SSH access to Bastion Host
    ec2.authorize_security_group_ingress(
        GroupId=bastion_sg_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            }
        ],
    )
    print(f"Bastion Security Group created: {bastion_sg_id}")

    # Create Security Group for WordPress Host

    wordpress_sg = ec2.create_security_group(
        GroupName="WordPressSG",
        Description="Security Group for WordPress Host",
        VpcId=vpc_id,
    )
    wordpress_sg_id = wordpress_sg["GroupId"]
    print(f"WordPress Security Group created: {wordpress_sg_id}")

    # Allow HTTP and HTTPS access to WordPress Host
    ec2.authorize_security_group_ingress(
        GroupId=wordpress_sg_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 80,
                "ToPort": 80,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 443,
                "ToPort": 443,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            },
        ],
    )
    print(f"WordPress Security Group rules updated: {wordpress_sg_id}")
    return {"bastion": bastion_sg_id, "wordpress": wordpress_sg_id}
