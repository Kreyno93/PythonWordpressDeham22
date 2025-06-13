# subnets.py
import ipaddress
import math


def create_subnets(ec2, vpc_id, cidr_block):
    print("Creating Subnets...")
    vpc_network = ipaddress.IPv4Network(cidr_block)

    # Calculate the maximum prefix length that allows at least 4 subnets
    possible_new_prefix = vpc_network.prefixlen
    max_subnets = 2 ** (32 - possible_new_prefix)

    for additional_bits in range(1, 8):
        new_prefix = possible_new_prefix + additional_bits
        num_subnets = 2**additional_bits
        if num_subnets >= 4:
            break

    if new_prefix > 30:
        raise ValueError(
            "CIDR block too small to create 2 public and 2 private subnets."
        )

    subnets = list(vpc_network.subnets(new_prefix=new_prefix))

    public_subnets = []
    private_subnets = []

    for i in range(2):
        public = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=str(subnets[i]),
            AvailabilityZone=f"us-west-2{chr(97 + i)}",
            TagSpecifications=[
                {
                    "ResourceType": "subnet",
                    "Tags": [{"Key": "Name", "Value": f"PublicSubnet{i + 1}"}],
                }
            ],
        )
        private = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=str(subnets[i + 2]),
            AvailabilityZone=f"us-west-2{chr(97 + i)}",
            TagSpecifications=[
                {
                    "ResourceType": "subnet",
                    "Tags": [{"Key": "Name", "Value": f"PrivateSubnet{i + 1}"}],
                }
            ],
        )
        public_subnets.append(public["Subnet"]["SubnetId"])
        private_subnets.append(private["Subnet"]["SubnetId"])

    return {"public": public_subnets, "private": private_subnets}
