# ec2_instances.py
def launch_bastion_and_web(ec2, vpc_id, subnet_ids, sg_ids):
    print("Launching EC2 Instances...")
    # Bastion Host in public subnet with public IP
    print("Launching Bastion Host in public subnet...")
    ec2.run_instances(
        ImageId="ami-01502f23a8ee77afc",
        InstanceType="t2.micro",
        MaxCount=1,
        MinCount=1,
        KeyName="vockey",
        NetworkInterfaces=[
            {
                "DeviceIndex": 0,
                "SubnetId": subnet_ids["public"][0],
                "Groups": [sg_ids["bastion"]],
                "AssociatePublicIpAddress": True,
            }
        ],
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": "BastionHost"}],
            }
        ],
    )
    # WordPress Host in public subnet with Public IP
    print("Launching WordPress Host in public subnet...")
    ec2.run_instances(
        ImageId="ami-01502f23a8ee77afc",
        InstanceType="t2.micro",
        MaxCount=1,
        MinCount=1,
        KeyName="vockey",
        UserData=open("userdata.sh").read(),
        NetworkInterfaces=[
            {
                "SubnetId": subnet_ids["public"][0],
                "Groups": [sg_ids["wordpress"]],
                "DeviceIndex": 0,
                "AssociatePublicIpAddress": True,
            }
        ],
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": "WordPressHost"}],
            }
        ],
    )


def delete_ec2_instances(ec2, vpc_id):
    print("Deleting EC2 Instances...")
    try:
        instances = ec2.describe_instances(
            Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
        )["Reservations"]
        instance_ids = []
        for reservation in instances:
            for instance in reservation["Instances"]:
                instance_ids.append(instance["InstanceId"])
        if instance_ids:
            ec2.terminate_instances(InstanceIds=instance_ids)
        print("EC2 Instances deleted successfully.")
    except Exception as e:
        print(f"Failed to delete EC2 Instances: {e}")
    finally:
        print("Cleanup complete.")
