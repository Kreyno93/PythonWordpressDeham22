# main.py
from vpc import create_vpc, delete_vpc
from subnets import create_subnets
from igw import create_internet_gateway
from routetables import create_route_tables
from routes import create_routes
from ec2_instances import launch_bastion_and_web, delete_ec2_instances
from rds import create_rds_instance
from delete_everything import delete_all_resources
from sg import create_security_groups
import boto3
import ipaddress
import sys
import time


def main():
    print("Welcome to the AWS Infrastructure Setup Script.")
    print(
        "We will set up: VPC, Subnets, Route Tables, EC2 Instances, Security Groups, and RDS."
    )

    while True:
        cidr_block = input(
            "Please enter the CIDR block for your VPC (e.g., 10.0.0.0/16): "
        )
        try:
            vpc_network = ipaddress.IPv4Network(cidr_block)
            if vpc_network.prefixlen > 28:
                print(
                    "CIDR block too small. Please choose a block with more available IPs."
                )
            else:
                break
        except ValueError:
            print("Invalid CIDR block. Please try again.")

    ec2 = boto3.client("ec2")
    rds_client = boto3.client("rds")

    vpc_id = None

    # Fail-safe mechanism to ensure VPC deletion and ec2 instance cleanup. First EC2 then VPC in case of deletion.
    print("Starting the setup process...")
    try:
        vpc_id = create_vpc(ec2, cidr_block)
        subnet_ids = create_subnets(ec2, vpc_id, cidr_block)
        igw_id = create_internet_gateway(ec2, vpc_id)
        route_table_ids = create_route_tables(ec2, vpc_id)
        create_routes(ec2, vpc_id, route_table_ids, subnet_ids, igw_id)
        sg_ids = create_security_groups(ec2, vpc_id)
        launch_bastion_and_web(ec2, vpc_id, subnet_ids, sg_ids)
        create_rds_instance(rds_client, subnet_ids)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Cleaning up resources...")
        delete_all_resources()


if __name__ == "__main__":
    main()
