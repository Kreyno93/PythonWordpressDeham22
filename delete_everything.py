import boto3
import time
from ec2_instances import delete_ec2_instances
from vpc import delete_vpc


def delete_all_resources():
    ec2 = boto3.client("ec2")

    # Get all VPCs
    vpcs = ec2.describe_vpcs()["Vpcs"]

    for vpc in vpcs:
        vpc_id = vpc["VpcId"]
        print(f"Deleting resources in VPC: {vpc_id}")

        # 1. Delete EC2 instances in the VPC
        delete_ec2_instances(ec2, vpc_id)

        # 2. Delete RDS instances (if any)
        rds = boto3.client("rds")
        try:
            db_instances = rds.describe_db_instances()["DBInstances"]
            for db in db_instances:
                if db["DBSubnetGroup"]["VpcId"] == vpc_id:
                    rds.delete_db_instance(
                        DBInstanceIdentifier=db["DBInstanceIdentifier"],
                        SkipFinalSnapshot=True,
                    )
                    print(f"Deleted RDS instance: {db['DBInstanceIdentifier']}")
        except Exception as e:
            print(f"Failed to delete RDS instances: {e}")

        # 3. Wait for RDS instances to be deleted
        print("Waiting for RDS instances to be deleted...")
        while True:
            db_instances = rds.describe_db_instances()["DBInstances"]
            if not any(db["DBSubnetGroup"]["VpcId"] == vpc_id for db in db_instances):
                break
            print("RDS instances still deleting...")
            time.sleep(10)

        # 4. Wait for EC2 instances to be terminated
        print("Waiting for EC2 instances to terminate...")
        while True:
            instances = ec2.describe_instances(
                Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
            )["Reservations"]
            if not any(instance["Instances"] for instance in instances):
                break
            print("EC2 instances still terminating...")
            time.sleep(10)

        # 5. Delete Subnet Groups
        try:
            db_subnet_groups = rds.describe_db_subnet_groups()["DBSubnetGroups"]
            for group in db_subnet_groups:
                if group["VpcId"] == vpc_id:
                    rds.delete_db_subnet_group(
                        DBSubnetGroupName=group["DBSubnetGroupName"]
                    )
                    print(f"Deleted DB Subnet Group: {group['DBSubnetGroupName']}")
        except Exception as e:
            print(f"Failed to delete DB Subnet Groups: {e}")

        # 6. Delete the VPC
        delete_vpc(ec2, vpc_id)


print("All resources deleted successfully.")
